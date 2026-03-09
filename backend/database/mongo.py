import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI not found in .env file")

# Synchronous client (for backward compatibility)
client = MongoClient(MONGO_URI)
db = client["security_risk_detection"]
alerts_collection = db["alerts"]

# Async client (for enterprise features) - import only when needed
async_client = None
async_db = None

async def get_database():
    """Get async database instance for enterprise features"""
    global async_client, async_db
    
    if async_db is None:
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            async_client = AsyncIOMotorClient(MONGO_URI)
            async_db = async_client["security_risk_detection"]
        except ImportError:
            raise ImportError("motor package required for async database operations. Install with: pip install motor")
    
    return async_db

# ✅ ADD THIS FUNCTION
def save_alert(alert):
    result = alerts_collection.insert_one(alert)
    return result
