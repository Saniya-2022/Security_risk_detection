"""
UNSW-NB15 Dataset Loader and Preprocessor
Handles loading, cleaning, and preparing the dataset for ML training
"""
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

class UNSWDatasetLoader:
    """Load and preprocess UNSW-NB15 dataset"""
    
    # UNSW-NB15 column names
    COLUMNS = [
        'srcip', 'sport', 'dstip', 'dsport', 'proto', 'state', 'dur', 'sbytes', 
        'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'service', 'Sload', 'Dload',
        'Spkts', 'Dpkts', 'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz', 'dmeansz',
        'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt',
        'Dintpkt', 'tcprtt', 'synack', 'ackdat', 'is_sm_ips_ports', 'ct_state_ttl',
        'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst',
        'ct_dst_ltm', 'ct_src_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 
        'ct_dst_src_ltm', 'attack_cat', 'Label'
    ]
    
    # Attack category mapping
    ATTACK_MAPPING = {
        'Normal': 'Normal',
        'Generic': 'Generic Attack',
        'Exploits': 'Exploit',
        'Fuzzers': 'Fuzzer',
        'DoS': 'DoS',
        'Reconnaissance': 'Reconnaissance',
        'Analysis': 'Analysis',
        'Backdoor': 'Backdoor',
        'Shellcode': 'Shellcode',
        'Worms': 'Worm'
    }
    
    def __init__(self, dataset_dir='backend/datasets'):
        self.dataset_dir = Path(dataset_dir)
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = []
        
    def load_dataset(self, filename, has_header=False):
        """Load UNSW-NB15 CSV file"""
        filepath = self.dataset_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(
                f"Dataset not found: {filepath}\n"
                f"Please download UNSW-NB15 dataset and place in {self.dataset_dir}"
            )
        
        # Load with or without header
        if has_header:
            df = pd.read_csv(filepath)
        else:
            df = pd.read_csv(filepath, names=self.COLUMNS, header=None)
        
        print(f"✅ Loaded {filename}: {len(df)} rows, {len(df.columns)} columns")
        return df
    
    def preprocess_data(self, df, fit_encoders=False):
        """Preprocess dataset for ML training"""
        df = df.copy()
        
        # Handle missing values
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(0)
        
        # Clean attack_cat column
        if 'attack_cat' in df.columns:
            df['attack_cat'] = df['attack_cat'].fillna('Normal')
            df['attack_cat'] = df['attack_cat'].str.strip()
            # Map to standardized names
            df['attack_cat'] = df['attack_cat'].map(
                lambda x: self.ATTACK_MAPPING.get(x, x)
            )
        
        # Select features for ML (exclude IPs, timestamps, labels)
        exclude_cols = ['srcip', 'dstip', 'Stime', 'Ltime', 'attack_cat', 'Label']
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        # Encode categorical features
        categorical_cols = ['proto', 'state', 'service']
        for col in categorical_cols:
            if col in df.columns:
                if fit_encoders:
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col].astype(str))
                    self.label_encoders[col] = le
                else:
                    if col in self.label_encoders:
                        le = self.label_encoders[col]
                        df[col] = df[col].map(lambda x: le.transform([str(x)])[0] 
                                              if str(x) in le.classes_ else -1)
                    else:
                        df[col] = 0
        
        # Store feature columns
        if fit_encoders:
            self.feature_columns = feature_cols
        
        return df
    
    def prepare_training_data(self, df):
        """Prepare features and labels for training"""
        X = df[self.feature_columns].values
        y = df['Label'].values  # Binary: 0=Normal, 1=Attack
        attack_types = df['attack_cat'].values
        
        # Scale features
        X = self.scaler.fit_transform(X)
        
        return X, y, attack_types
    
    def prepare_test_data(self, df):
        """Prepare test data using fitted scaler"""
        X = df[self.feature_columns].values
        y = df['Label'].values
        attack_types = df['attack_cat'].values
        
        # Scale using fitted scaler
        X = self.scaler.transform(X)
        
        return X, y, attack_types
    
    def save_preprocessor(self, filepath='backend/ml/models/unsw_preprocessor.pkl'):
        """Save label encoders and scaler"""
        preprocessor = {
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }
        joblib.dump(preprocessor, filepath)
        print(f"✅ Saved preprocessor to {filepath}")
    
    def load_preprocessor(self, filepath='backend/ml/models/unsw_preprocessor.pkl'):
        """Load saved preprocessor"""
        preprocessor = joblib.load(filepath)
        self.label_encoders = preprocessor['label_encoders']
        self.scaler = preprocessor['scaler']
        self.feature_columns = preprocessor['feature_columns']
        print(f"✅ Loaded preprocessor from {filepath}")
    
    def get_attack_severity(self, attack_type):
        """Map attack type to severity level"""
        high_severity = ['Exploit', 'DoS', 'Backdoor', 'Shellcode', 'Worm']
        medium_severity = ['Reconnaissance', 'Analysis', 'Fuzzer', 'Generic Attack']
        
        if attack_type in high_severity:
            return 'HIGH'
        elif attack_type in medium_severity:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def format_alert(self, row, prediction, confidence, attack_type):
        """Convert ML output to human-readable alert"""
        severity = self.get_attack_severity(attack_type)
        
        # Extract source IP
        source_ip = row.get('srcip', 'Unknown')
        dest_ip = row.get('dstip', 'Unknown')
        
        # Create alert message
        if prediction == 1:  # Attack detected
            message = f"{severity} confidence {attack_type} detected from {source_ip}"
        else:
            message = f"Normal traffic from {source_ip}"
        
        return {
            'message': message,
            'severity': severity,
            'attack_type': attack_type,
            'source_ip': source_ip,
            'dest_ip': dest_ip,
            'confidence': float(confidence),
            'prediction': int(prediction)
        }
