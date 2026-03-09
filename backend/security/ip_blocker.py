"""
IP Blocking Mechanism for Mini SIEM
Tracks and blocks malicious IP addresses
"""

from datetime import datetime
from backend.database.mongo import db

# Collections
blocked_ips_collection = db["blocked_ips"]
ip_violations_collection = db["ip_violations"]


# ============================================
# IP VIOLATION TRACKING
# ============================================

def record_ip_violation(ip_address: str, threat_type: str, risk_score: int, details: dict):
    """Record a security violation for an IP address"""
    
    violation = {
        "ip_address": ip_address,
        "threat_type": threat_type,
        "risk_score": risk_score,
        "details": details,
        "timestamp": datetime.utcnow()
    }
    
    ip_violations_collection.insert_one(violation)
    
    # Check if IP should be blocked
    check_and_block_ip(ip_address)


# ============================================
# IP BLOCKING LOGIC
# ============================================

def check_and_block_ip(ip_address: str):
    """Check if IP should be blocked based on violation history"""
    
    # Count HIGH severity violations in last hour
    from datetime import timedelta
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    
    high_violations = ip_violations_collection.count_documents({
        "ip_address": ip_address,
        "risk_score": {"$gte": 71},
        "timestamp": {"$gte": one_hour_ago}
    })
    
    # Block if 2 or more HIGH violations
    if high_violations >= 2:
        block_ip(ip_address, "Multiple HIGH severity violations detected")


def block_ip(ip_address: str, reason: str):
    """Add IP to blocked list"""
    
    # Check if already blocked
    existing = blocked_ips_collection.find_one({"ip_address": ip_address})
    
    if existing:
        # Update block count
        blocked_ips_collection.update_one(
            {"ip_address": ip_address},
            {
                "$inc": {"block_count": 1},
                "$set": {"last_blocked": datetime.utcnow()}
            }
        )
    else:
        # Add new block
        block_record = {
            "ip_address": ip_address,
            "reason": reason,
            "blocked_at": datetime.utcnow(),
            "last_blocked": datetime.utcnow(),
            "block_count": 1,
            "status": "blocked"
        }
        blocked_ips_collection.insert_one(block_record)
    
    print(f"🚫 IP {ip_address} has been blocked: {reason}")


# ============================================
# IP CHECK
# ============================================

def is_ip_blocked(ip_address: str) -> bool:
    """Check if an IP is currently blocked"""
    
    blocked = blocked_ips_collection.find_one({
        "ip_address": ip_address,
        "status": "blocked"
    })
    
    return blocked is not None


# ============================================
# IP UNBLOCKING
# ============================================

def unblock_ip(ip_address: str):
    """Remove IP from blocked list"""
    
    blocked_ips_collection.update_one(
        {"ip_address": ip_address},
        {"$set": {"status": "unblocked", "unblocked_at": datetime.utcnow()}}
    )
    
    print(f"✅ IP {ip_address} has been unblocked")


# ============================================
# GET BLOCKED IPS
# ============================================

def get_blocked_ips():
    """Get all currently blocked IPs"""
    
    blocked = blocked_ips_collection.find({"status": "blocked"}).sort("blocked_at", -1)
    
    return [{
        "ip_address": ip["ip_address"],
        "reason": ip["reason"],
        "blocked_at": ip["blocked_at"],
        "block_count": ip["block_count"]
    } for ip in blocked]


# ============================================
# GET IP HISTORY
# ============================================

def get_ip_history(ip_address: str):
    """Get violation history for an IP"""
    
    violations = ip_violations_collection.find(
        {"ip_address": ip_address}
    ).sort("timestamp", -1).limit(50)
    
    return list(violations)
