"""
Threat Intelligence & GeoIP Enrichment Module
Enriches alerts with geolocation, IP reputation, and threat intelligence
"""
import requests
from typing import Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ThreatEnrichment:
    def __init__(self):
        self.blacklist = self._load_blacklist()
        self.high_risk_countries = ['CN', 'RU', 'KP', 'IR']
        self.malicious_asns = [
            'AS4134',  # Chinanet
            'AS4837',  # China Unicom
            'AS9009',  # M247
        ]
    
    def _load_blacklist(self) -> set:
        """Load known malicious IPs"""
        return {
            '192.168.100.50',
            '10.0.0.66',
            '172.16.0.99',
            '203.0.113.0',
            '198.51.100.0',
        }
    
    def enrich_ip(self, ip_address: str) -> Dict:
        """
        Enrich IP with geolocation and threat intelligence
        """
        enrichment = {
            'ip_address': ip_address,
            'country': None,
            'city': None,
            'asn': None,
            'is_blacklisted': False,
            'is_high_risk_country': False,
            'is_malicious_asn': False,
            'reputation_score': 100,  # 0-100, lower is worse
            'threat_level': 'clean',
            'enriched_at': datetime.utcnow().isoformat()
        }
        
        try:
            # Check blacklist first
            if ip_address in self.blacklist:
                enrichment['is_blacklisted'] = True
                enrichment['reputation_score'] = 0
                enrichment['threat_level'] = 'critical'
                logger.warning(f"IP {ip_address} found in blacklist")
            
            # Get GeoIP data (using free ip-api.com)
            geo_data = self._get_geoip(ip_address)
            if geo_data:
                enrichment['country'] = geo_data.get('countryCode')
                enrichment['city'] = geo_data.get('city')
                enrichment['asn'] = geo_data.get('as', '').split()[0] if geo_data.get('as') else None
                
                # Check high-risk country
                if enrichment['country'] in self.high_risk_countries:
                    enrichment['is_high_risk_country'] = True
                    enrichment['reputation_score'] -= 30
                    enrichment['threat_level'] = 'high'
                
                # Check malicious ASN
                if enrichment['asn'] in self.malicious_asns:
                    enrichment['is_malicious_asn'] = True
                    enrichment['reputation_score'] -= 40
                    enrichment['threat_level'] = 'high'
            
            # Determine final threat level
            if enrichment['reputation_score'] < 30:
                enrichment['threat_level'] = 'critical'
            elif enrichment['reputation_score'] < 60:
                enrichment['threat_level'] = 'high'
            elif enrichment['reputation_score'] < 80:
                enrichment['threat_level'] = 'medium'
            else:
                enrichment['threat_level'] = 'clean'
                
        except Exception as e:
            logger.error(f"Error enriching IP {ip_address}: {e}")
        
        return enrichment
    
    def _get_geoip(self, ip_address: str) -> Optional[Dict]:
        """
        Get GeoIP data from ip-api.com (free tier)
        """
        try:
            # Skip private IPs
            if self._is_private_ip(ip_address):
                return {
                    'countryCode': 'US',
                    'city': 'Local Network',
                    'as': 'AS0 Private Network'
                }
            
            response = requests.get(
                f'http://ip-api.com/json/{ip_address}',
                timeout=2
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"GeoIP lookup failed for {ip_address}: {e}")
        
        return None
    
    def _is_private_ip(self, ip: str) -> bool:
        """Check if IP is private/local"""
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        
        first = int(parts[0])
        second = int(parts[1])
        
        # Private ranges
        if first == 10:
            return True
        if first == 172 and 16 <= second <= 31:
            return True
        if first == 192 and second == 168:
            return True
        if first == 127:
            return True
        
        return False
    
    def add_to_blacklist(self, ip_address: str):
        """Add IP to blacklist"""
        self.blacklist.add(ip_address)
        logger.info(f"Added {ip_address} to blacklist")
    
    def calculate_threat_score(self, enrichment: Dict) -> int:
        """
        Calculate threat intelligence score (0-100)
        Higher score = more dangerous
        """
        score = 0
        
        if enrichment.get('is_blacklisted'):
            score += 50
        if enrichment.get('is_high_risk_country'):
            score += 20
        if enrichment.get('is_malicious_asn'):
            score += 20
        
        # Reputation score (inverted)
        reputation = enrichment.get('reputation_score', 100)
        score += (100 - reputation) * 0.1
        
        return min(int(score), 100)


# Global instance
threat_enrichment = ThreatEnrichment()
