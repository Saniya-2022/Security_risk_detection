"""
MITRE ATT&CK Framework Mapping Module
Maps detected threats to MITRE ATT&CK tactics and techniques
"""
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class MITREMapper:
    def __init__(self):
        self.attack_mapping = {
            # Network attacks
            'dos': {
                'tactic': 'Impact',
                'technique_id': 'T1499',
                'technique_name': 'Endpoint Denial of Service',
                'description': 'Adversary attempting to make system unavailable'
            },
            'ddos': {
                'tactic': 'Impact',
                'technique_id': 'T1498',
                'technique_name': 'Network Denial of Service',
                'description': 'Distributed denial of service attack'
            },
            'probe': {
                'tactic': 'Discovery',
                'technique_id': 'T1046',
                'technique_name': 'Network Service Scanning',
                'description': 'Adversary scanning for network services'
            },
            'reconnaissance': {
                'tactic': 'Reconnaissance',
                'technique_id': 'T1595',
                'technique_name': 'Active Scanning',
                'description': 'Adversary actively probing infrastructure'
            },
            
            # Login/Authentication attacks
            'brute_force': {
                'tactic': 'Credential Access',
                'technique_id': 'T1110',
                'technique_name': 'Brute Force',
                'description': 'Adversary attempting to guess credentials'
            },
            'credential_stuffing': {
                'tactic': 'Credential Access',
                'technique_id': 'T1110.004',
                'technique_name': 'Credential Stuffing',
                'description': 'Using breached credentials from other services'
            },
            'password_spray': {
                'tactic': 'Credential Access',
                'technique_id': 'T1110.003',
                'technique_name': 'Password Spraying',
                'description': 'Trying common passwords across many accounts'
            },
            
            # Email attacks
            'phishing': {
                'tactic': 'Initial Access',
                'technique_id': 'T1566',
                'technique_name': 'Phishing',
                'description': 'Adversary sending phishing messages'
            },
            'spear_phishing': {
                'tactic': 'Initial Access',
                'technique_id': 'T1566.001',
                'technique_name': 'Spearphishing Attachment',
                'description': 'Targeted phishing with malicious attachment'
            },
            
            # Malware attacks
            'malware': {
                'tactic': 'Execution',
                'technique_id': 'T1204',
                'technique_name': 'User Execution',
                'description': 'Malicious file executed by user'
            },
            'trojan': {
                'tactic': 'Execution',
                'technique_id': 'T1204.002',
                'technique_name': 'Malicious File',
                'description': 'User opened malicious file'
            },
            'ransomware': {
                'tactic': 'Impact',
                'technique_id': 'T1486',
                'technique_name': 'Data Encrypted for Impact',
                'description': 'Adversary encrypting data for ransom'
            },
            
            # Exploitation
            'exploit': {
                'tactic': 'Initial Access',
                'technique_id': 'T1190',
                'technique_name': 'Exploit Public-Facing Application',
                'description': 'Adversary exploiting vulnerability'
            },
            'shellcode': {
                'tactic': 'Execution',
                'technique_id': 'T1059',
                'technique_name': 'Command and Scripting Interpreter',
                'description': 'Executing malicious commands'
            },
            
            # Data exfiltration
            'exfiltration': {
                'tactic': 'Exfiltration',
                'technique_id': 'T1041',
                'technique_name': 'Exfiltration Over C2 Channel',
                'description': 'Data being stolen via command channel'
            },
            
            # Backdoor
            'backdoor': {
                'tactic': 'Persistence',
                'technique_id': 'T1543',
                'technique_name': 'Create or Modify System Process',
                'description': 'Adversary establishing persistence'
            },
            
            # Generic/Analysis
            'generic': {
                'tactic': 'Unknown',
                'technique_id': 'T1001',
                'technique_name': 'Data Obfuscation',
                'description': 'Suspicious activity detected'
            },
            'analysis': {
                'tactic': 'Discovery',
                'technique_id': 'T1087',
                'technique_name': 'Account Discovery',
                'description': 'Adversary enumerating accounts'
            },
            'worms': {
                'tactic': 'Lateral Movement',
                'technique_id': 'T1210',
                'technique_name': 'Exploitation of Remote Services',
                'description': 'Self-replicating malware spreading'
            },
            'fuzzers': {
                'tactic': 'Discovery',
                'technique_id': 'T1595.002',
                'technique_name': 'Vulnerability Scanning',
                'description': 'Automated vulnerability discovery'
            }
        }
    
    def map_threat(self, threat_type: str) -> Optional[Dict]:
        """
        Map threat type to MITRE ATT&CK framework
        """
        threat_lower = threat_type.lower().replace(' ', '_')
        
        # Direct mapping
        if threat_lower in self.attack_mapping:
            return self.attack_mapping[threat_lower]
        
        # Fuzzy matching
        for key in self.attack_mapping.keys():
            if key in threat_lower or threat_lower in key:
                return self.attack_mapping[key]
        
        # Default to generic
        logger.warning(f"No MITRE mapping found for: {threat_type}")
        return self.attack_mapping['generic']
    
    def get_all_tactics(self) -> list:
        """Get list of all MITRE tactics"""
        tactics = set()
        for mapping in self.attack_mapping.values():
            tactics.add(mapping['tactic'])
        return sorted(list(tactics))
    
    def get_techniques_by_tactic(self, tactic: str) -> list:
        """Get all techniques for a specific tactic"""
        techniques = []
        for threat_type, mapping in self.attack_mapping.items():
            if mapping['tactic'] == tactic:
                techniques.append({
                    'threat_type': threat_type,
                    'technique_id': mapping['technique_id'],
                    'technique_name': mapping['technique_name']
                })
        return techniques


# Global instance
mitre_mapper = MITREMapper()
