"""
UNSW-NB15 Real-Time Streaming Service
Simulates live intrusion detection by streaming test dataset
"""
import asyncio
import pandas as pd
import numpy as np
from datetime import datetime
import joblib
from pathlib import Path
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datasets.unsw_loader import UNSWDatasetLoader

class UNSWStreamService:
    """Stream UNSW-NB15 test data for real-time detection"""
    
    def __init__(self, model_path='backend/ml/models/unsw_best_model.pkl'):
        self.loader = UNSWDatasetLoader()
        self.model = None
        self.model_path = model_path
        self.test_data = None
        self.current_index = 0
        self.is_running = False
        self.stream_interval = 1.5  # seconds between events
        
    def load_model(self):
        """Load trained ML model"""
        try:
            self.model = joblib.load(self.model_path)
            self.loader.load_preprocessor()
            print(f"✅ Loaded model from {self.model_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            return False
    
    def load_test_data(self):
        """Load and preprocess test dataset"""
        try:
            print("📂 Loading UNSW-NB15 test dataset...")
            df = self.loader.load_dataset('UNSW_NB15_testing-set.csv')
            df = self.loader.preprocess_data(df, fit_encoders=False)
            
            # Shuffle for realistic streaming
            self.test_data = df.sample(frac=1, random_state=42).reset_index(drop=True)
            print(f"✅ Loaded {len(self.test_data)} test samples")
            return True
        except Exception as e:
            print(f"❌ Failed to load test data: {e}")
            return False
    
    def calculate_risk_score(self, prediction, confidence, attack_type, source_ip):
        """Calculate risk score (0-100) based on multiple factors"""
        base_score = confidence * 100
        
        # Attack type severity multiplier
        severity_multipliers = {
            'Exploit': 1.3,
            'DoS': 1.3,
            'Backdoor': 1.4,
            'Shellcode': 1.4,
            'Worm': 1.3,
            'Reconnaissance': 1.1,
            'Analysis': 1.1,
            'Fuzzer': 1.2,
            'Generic Attack': 1.1,
            'Normal': 0.5
        }
        
        multiplier = severity_multipliers.get(attack_type, 1.0)
        risk_score = min(base_score * multiplier, 100)
        
        # Add randomness for realism (±5%)
        risk_score = risk_score + np.random.uniform(-5, 5)
        risk_score = max(0, min(100, risk_score))
        
        return round(risk_score, 2)
    
    def get_next_event(self):
        """Get next event from test dataset"""
        if self.test_data is None or len(self.test_data) == 0:
            return None
        
        # Loop back to start if we reach the end
        if self.current_index >= len(self.test_data):
            self.current_index = 0
            print("🔄 Restarting test dataset stream...")
        
        row = self.test_data.iloc[self.current_index]
        self.current_index += 1
        
        return row
    
    def predict_event(self, row):
        """Run ML prediction on event"""
        try:
            # Prepare features
            X = row[self.loader.feature_columns].values.reshape(1, -1)
            X = self.loader.scaler.transform(X)
            
            # Predict
            prediction = self.model.predict(X)[0]
            confidence = self.model.predict_proba(X)[0][1]  # Probability of attack
            
            # Get actual attack type
            attack_type = row.get('attack_cat', 'Unknown')
            if pd.isna(attack_type) or attack_type == '':
                attack_type = 'Normal' if prediction == 0 else 'Generic Attack'
            
            return prediction, confidence, attack_type
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return 0, 0.5, 'Unknown'
    
    def format_detection_alert(self, row, prediction, confidence, attack_type):
        """Format detection result as alert"""
        source_ip = row.get('srcip', 'Unknown')
        dest_ip = row.get('dstip', 'Unknown')
        
        # Calculate risk score
        risk_score = self.calculate_risk_score(prediction, confidence, attack_type, source_ip)
        
        # Determine severity
        severity = self.loader.get_attack_severity(attack_type)
        
        # Create human-readable message
        if prediction == 1:  # Attack detected
            if confidence > 0.8:
                conf_level = "High confidence"
            elif confidence > 0.6:
                conf_level = "Medium confidence"
            else:
                conf_level = "Low confidence"
            
            message = f"{conf_level} {attack_type} detected from {source_ip}"
        else:
            message = f"Normal traffic from {source_ip}"
            severity = 'LOW'
        
        # Build alert object
        alert = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': 'intrusion_detection',
            'threat_type': attack_type.lower().replace(' ', '_'),
            'severity': severity,
            'risk_score': risk_score,
            'message': message,
            'source_ip': str(source_ip),
            'dest_ip': str(dest_ip),
            'source_port': int(row.get('sport', 0)),
            'dest_port': int(row.get('dsport', 0)),
            'protocol': str(row.get('proto', 'unknown')),
            'ml_confidence': float(confidence),
            'ml_prediction': int(prediction),
            'detected_by': 'UNSW-NB15 ML Model',
            'detection_method': 'machine_learning',
            'attack_category': attack_type,
            'bytes_sent': int(row.get('sbytes', 0)),
            'bytes_received': int(row.get('dbytes', 0)),
            'duration': float(row.get('dur', 0)),
            'risk_factors': self.get_risk_factors(row, attack_type, confidence)
        }
        
        return alert
    
    def get_risk_factors(self, row, attack_type, confidence):
        """Generate risk factors for alert"""
        factors = []
        
        if confidence > 0.8:
            factors.append(f"High ML confidence: {confidence*100:.1f}%")
        
        if attack_type != 'Normal':
            factors.append(f"Attack type: {attack_type}")
        
        # Check for suspicious patterns
        if row.get('sbytes', 0) > 10000:
            factors.append("High data volume sent")
        
        if row.get('dbytes', 0) > 10000:
            factors.append("High data volume received")
        
        if row.get('Spkts', 0) > 100:
            factors.append("High packet count")
        
        if len(factors) == 0:
            factors.append("Normal traffic pattern")
        
        return factors
    
    async def start_streaming(self, callback):
        """Start streaming events to callback function"""
        if not self.load_model():
            print("❌ Cannot start streaming: Model not loaded")
            return
        
        if not self.load_test_data():
            print("❌ Cannot start streaming: Test data not loaded")
            return
        
        self.is_running = True
        print(f"🚀 Started UNSW-NB15 streaming (interval: {self.stream_interval}s)")
        
        while self.is_running:
            try:
                # Get next event
                row = self.get_next_event()
                if row is None:
                    break
                
                # Run prediction
                prediction, confidence, attack_type = self.predict_event(row)
                
                # Format alert
                alert = self.format_detection_alert(row, prediction, confidence, attack_type)
                
                # Send to callback
                await callback(alert)
                
                # Wait before next event
                await asyncio.sleep(self.stream_interval)
                
            except Exception as e:
                print(f"❌ Streaming error: {e}")
                await asyncio.sleep(1)
    
    def stop_streaming(self):
        """Stop streaming"""
        self.is_running = False
        print("⏹️ Stopped UNSW-NB15 streaming")
    
    def get_status(self):
        """Get streaming status"""
        return {
            'is_running': self.is_running,
            'current_index': self.current_index,
            'total_samples': len(self.test_data) if self.test_data is not None else 0,
            'progress': f"{self.current_index}/{len(self.test_data)}" if self.test_data is not None else "0/0",
            'stream_interval': self.stream_interval
        }
