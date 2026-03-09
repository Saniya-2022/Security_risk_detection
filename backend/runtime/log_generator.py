import random
from datetime import datetime, timezone

USERS = ["admin", "user1", "user2"]
IPS = ["192.168.1.10", "10.0.0.5", "203.0.113.45"]

def generate_log():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user": random.choice(USERS),
        "ip": random.choice(IPS),
        "event": "login",
        "status": random.choice(["success", "failed"])
    }

def generate_multiple_logs(count=20):
    return [generate_log() for _ in range(count)]
