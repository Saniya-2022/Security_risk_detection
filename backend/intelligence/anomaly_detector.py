"""
Behavioral Anomaly Detection Module
Detects anomalies using Isolation Forest and behavioral analysis
"""
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class AnomalyDetector:
    def __init__(self):
        # Isolation Forest model
        self.model = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        
        # Behavioral baselines
        self.user_login_history = defaultdict(list)
        self.ip_activity_history = defaultdict(list)
        self.user_ip_mapping = defaultdict(set)
        
        # Thresholds
        self.anomaly_threshold = -0.5  # Isolation Forest threshold
        self.rare_hour_threshold = 0.1  # 10% of logins
        
    def detect_anomaly(self, event: Dict) -> Dict:
        """
        Detect anomalies in event
        Returns anomaly score and details
        """
        anomaly_result = {
            'is_anomaly': False,
            'anomaly_score': 0.0,
            'anomaly_type': [],
            'anomaly_details': []
        }
        
        event_type = event.get('event_type', '')
        source_ip = event.get('source_ip')
        target_user = event.get('target_user')
        timestamp = event.get('timestamp', datetime.utcnow())
        
        # Login time anomaly
        if 'login' in event_type.lower():
            login_anomaly = self._detect_login_time_anomaly(target_user, timestamp)
            if login_anomaly['is_anomaly']:
                anomaly_result['is_anomaly'] = True
                anomaly_result['anomaly_type'].append('unusual_login_time')
                anomaly_result['anomaly_details'].append(login_anomaly['detail'])
                anomaly_result['anomaly_score'] = max(
                    anomaly_result['anomaly_score'],
                    login_anomaly['score']
                )
        
        # Rare IP for user
        if target_user and source_ip:
            ip_anomaly = self._detect_rare_ip_for_user(target_user, source_ip)
            if ip_anomaly['is_anomaly']:
                anomaly_result['is_anomaly'] = True
                anomaly_result['anomaly_type'].append('rare_ip_for_user')
                anomaly_result['anomaly_details'].append(ip_anomaly['detail'])
                anomaly_result['anomaly_score'] = max(
                    anomaly_result['anomaly_score'],
                    ip_anomaly['score']
                )
        
        # Activity spike from IP
        if source_ip:
            spike_anomaly = self._detect_activity_spike(source_ip)
            if spike_anomaly['is_anomaly']:
                anomaly_result['is_anomaly'] = True
                anomaly_result['anomaly_type'].append('activity_spike')
                anomaly_result['anomaly_details'].append(spike_anomaly['detail'])
                anomaly_result['anomaly_score'] = max(
                    anomaly_result['anomaly_score'],
                    spike_anomaly['score']
                )
        
        # Impossible travel (geo-location based)
        if target_user and source_ip:
            travel_anomaly = self._detect_impossible_travel(target_user, source_ip, timestamp)
            if travel_anomaly['is_anomaly']:
                anomaly_result['is_anomaly'] = True
                anomaly_result['anomaly_type'].append('impossible_travel')
                anomaly_result['anomaly_details'].append(travel_anomaly['detail'])
                anomaly_result['anomaly_score'] = max(
                    anomaly_result['anomaly_score'],
                    travel_anomaly['score']
                )
        
        # Update history
        self._update_history(event)
        
        return anomaly_result
    
    def _detect_login_time_anomaly(self, user: str, timestamp: datetime) -> Dict:
        """Detect unusual login time for user"""
        if not user:
            return {'is_anomaly': False, 'score': 0.0, 'detail': ''}
        
        hour = timestamp.hour
        
        # Get user's login history
        history = self.user_login_history.get(user, [])
        
        if len(history) < 5:
            # Not enough data
            return {'is_anomaly': False, 'score': 0.0, 'detail': ''}
        
        # Calculate hour frequency
        hour_counts = defaultdict(int)
        for hist_time in history:
            hour_counts[hist_time.hour] += 1
        
        total_logins = len(history)
        current_hour_freq = hour_counts.get(hour, 0) / total_logins
        
        # Anomaly if this hour is rare
        if current_hour_freq < self.rare_hour_threshold:
            return {
                'is_anomaly': True,
                'score': 0.7,
                'detail': f'Login at unusual hour {hour}:00 (only {current_hour_freq*100:.1f}% of logins)'
            }
        
        return {'is_anomaly': False, 'score': 0.0, 'detail': ''}
    
    def _detect_rare_ip_for_user(self, user: str, ip: str) -> Dict:
        """Detect if IP is rare for this user"""
        if not user or not ip:
            return {'is_anomaly': False, 'score': 0.0, 'detail': ''}
        
        known_ips = self.user_ip_mapping.get(user, set())
        
        if len(known_ips) >= 3 and ip not in known_ips:
            return {
                'is_anomaly': True,
                'score': 0.8,
                'detail': f'User {user} accessing from new IP {ip} (known IPs: {len(known_ips)})'
            }
        
        return {'is_anomaly': False, 'score': 0.0, 'detail': ''}
    
    def _detect_activity_spike(self, ip: str) -> Dict:
        """Detect sudden spike in activity from IP"""
        if not ip:
            return {'is_anomaly': False, 'score': 0.0, 'detail': ''}
        
        history = self.ip_activity_history.get(ip, [])
        
        # Count recent activity (last 5 minutes)
        now = datetime.utcnow()
        recent_count = sum(1 for t in history if (now - t).total_seconds() < 300)
        
        # Spike if more than 10 events in 5 minutes
        if recent_count > 10:
            return {
                'is_anomaly': True,
                'score': min(recent_count / 20, 1.0),
                'detail': f'Activity spike from {ip}: {recent_count} events in 5 minutes'
            }
        
        return {'is_anomaly': False, 'score': 0.0, 'detail': ''}
    
    def _detect_impossible_travel(self, user: str, ip: str, timestamp: datetime) -> Dict:
        """Detect impossible travel (same user, different locations, short time)"""
        # Simplified: Check if user accessed from different IP very recently
        if not user or not ip:
            return {'is_anomaly': False, 'score': 0.0, 'detail': ''}
        
        history = self.user_login_history.get(user, [])
        
        if len(history) < 2:
            return {'is_anomaly': False, 'score': 0.0, 'detail': ''}
        
        # Check last login
        last_login = history[-1]
        time_diff = (timestamp - last_login).total_seconds() / 60  # minutes
        
        # If login within 30 minutes from different IP
        known_ips = self.user_ip_mapping.get(user, set())
        if time_diff < 30 and len(known_ips) > 1 and ip not in known_ips:
            return {
                'is_anomaly': True,
                'score': 0.9,
                'detail': f'Impossible travel: User {user} accessed from {ip} only {time_diff:.1f} min after previous login'
            }
        
        return {'is_anomaly': False, 'score': 0.0, 'detail': ''}
    
    def _update_history(self, event: Dict):
        """Update behavioral history"""
        timestamp = event.get('timestamp', datetime.utcnow())
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        
        user = event.get('target_user')
        ip = event.get('source_ip')
        
        if user:
            self.user_login_history[user].append(timestamp)
            # Keep only last 100 entries
            if len(self.user_login_history[user]) > 100:
                self.user_login_history[user] = self.user_login_history[user][-100:]
        
        if ip:
            self.ip_activity_history[ip].append(timestamp)
            if len(self.ip_activity_history[ip]) > 100:
                self.ip_activity_history[ip] = self.ip_activity_history[ip][-100:]
        
        if user and ip:
            self.user_ip_mapping[user].add(ip)
            # Keep only last 10 IPs per user
            if len(self.user_ip_mapping[user]) > 10:
                self.user_ip_mapping[user] = set(list(self.user_ip_mapping[user])[-10:])
    
    def get_user_baseline(self, user: str) -> Dict:
        """Get behavioral baseline for user"""
        return {
            'login_count': len(self.user_login_history.get(user, [])),
            'known_ips': list(self.user_ip_mapping.get(user, set())),
            'last_login': self.user_login_history.get(user, [])[-1] if self.user_login_history.get(user) else None
        }


# Global instance
anomaly_detector = AnomalyDetector()
