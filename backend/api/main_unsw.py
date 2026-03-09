"""
FastAPI Backend for UNSW-NB15 Real-Time Intrusion Detection System
Enterprise SIEM with ML-based threat detection
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.mongo import get_database
from api.websocket_manager import WebSocketManager
from runtime.unsw_stream_service import UNSWStreamService
from runtime.email_service import EmailService

# Global instances
ws_manager = WebSocketManager()
stream_service = UNSWStreamService()
email_service = EmailService()
db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global db
    
    print("\n" + "="*60)
    print("🚀 STARTING UNSW-NB15 INTRUSION DETECTION SYSTEM")
    print("="*60)
    
    # Connect to MongoDB
    try:
        db = get_database()
        print("✅ Connected to MongoDB Atlas")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        db = None
    
    # Start streaming service
    asyncio.create_task(start_stream_service())
    
    print("="*60)
    print("✅ SYSTEM READY")
    print("="*60 + "\n")
    
    yield
    
    # Shutdown
    print("\n⏹️ Shutting down...")
    stream_service.stop_streaming()

app = FastAPI(
    title="UNSW-NB15 Intrusion Detection System",
    description="Real-time ML-based network intrusion detection using UNSW-NB15 dataset",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def process_alert(alert: Dict):
    """Process incoming alert from stream service"""
    try:
        # Store in MongoDB
        if db is not None:
            collection = db['alerts']
            result = collection.insert_one(alert)
            alert['_id'] = str(result.inserted_id)
        
        # Broadcast via WebSocket
        await ws_manager.broadcast({
            'type': 'alert',
            'data': alert
        })
        
        # Send email for high-risk alerts
        if alert['risk_score'] > 70:
            try:
                email_service.send_alert_email(alert)
            except Exception as e:
                print(f"⚠️ Email notification failed: {e}")
        
        # Check for IP blocking
        if alert['severity'] == 'HIGH' and db is not None:
            await check_and_block_ip(alert['source_ip'])
        
        # Update statistics
        await broadcast_statistics()
        
    except Exception as e:
        print(f"❌ Error processing alert: {e}")

async def check_and_block_ip(ip_address: str):
    """Block IP if multiple HIGH severity violations"""
    try:
        if db is None:
            return
        
        # Count HIGH severity alerts from this IP
        alerts_collection = db['alerts']
        high_count = alerts_collection.count_documents({
            'source_ip': ip_address,
            'severity': 'HIGH'
        })
        
        if high_count >= 2:
            # Check if already blocked
            blocked_collection = db['blocked_ips']
            existing = blocked_collection.find_one({'ip_address': ip_address})
            
            if not existing:
                # Block the IP
                blocked_collection.insert_one({
                    'ip_address': ip_address,
                    'blocked_at': datetime.utcnow().isoformat(),
                    'reason': f'Multiple HIGH severity violations ({high_count})',
                    'block_count': high_count
                })
                
                print(f"🚫 Blocked IP: {ip_address} ({high_count} violations)")
                
                # Broadcast IP block event
                await ws_manager.broadcast({
                    'type': 'ip_blocked',
                    'data': {
                        'ip_address': ip_address,
                        'reason': f'{high_count} HIGH severity violations'
                    }
                })
    except Exception as e:
        print(f"❌ Error checking IP block: {e}")

async def broadcast_statistics():
    """Calculate and broadcast current statistics"""
    try:
        if db is None:
            return
        
        collection = db['alerts']
        
        # Total alerts
        total = collection.count_documents({})
        
        # By severity
        high = collection.count_documents({'severity': 'HIGH'})
        medium = collection.count_documents({'severity': 'MEDIUM'})
        low = collection.count_documents({'severity': 'LOW'})
        
        # Threat distribution
        pipeline = [
            {'$group': {'_id': '$attack_category', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ]
        threat_dist = list(collection.aggregate(pipeline))
        
        # Top source IPs
        pipeline = [
            {'$match': {'severity': {'$in': ['HIGH', 'MEDIUM']}}},
            {'$group': {'_id': '$source_ip', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ]
        top_ips = list(collection.aggregate(pipeline))
        
        stats = {
            'total_alerts': total,
            'by_severity': {
                'HIGH': high,
                'MEDIUM': medium,
                'LOW': low
            },
            'threat_distribution': threat_dist,
            'top_source_ips': top_ips,
            'active_connections': ws_manager.get_connection_count()
        }
        
        await ws_manager.broadcast({
            'type': 'statistics',
            'data': stats
        })
        
    except Exception as e:
        print(f"❌ Error broadcasting statistics: {e}")

async def start_stream_service():
    """Start the UNSW-NB15 streaming service"""
    await asyncio.sleep(2)  # Wait for system initialization
    print("🌊 Starting UNSW-NB15 data stream...")
    await stream_service.start_streaming(process_alert)

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "UNSW-NB15 Intrusion Detection System",
        "version": "2.0.0",
        "status": "operational",
        "features": [
            "Real-time ML-based intrusion detection",
            "Multiple ML models (Random Forest, XGBoost, Logistic Regression)",
            "WebSocket live alerts",
            "Automatic IP blocking",
            "Email notifications",
            "MongoDB Atlas storage"
        ]
    }

@app.get("/alerts")
async def get_alerts(limit: int = 100, severity: str = None):
    """Get recent alerts"""
    if db is None:
        return []
    
    try:
        collection = db['alerts']
        query = {}
        
        if severity:
            query['severity'] = severity.upper()
        
        alerts = list(collection.find(query).sort('timestamp', -1).limit(limit))
        
        # Convert ObjectId to string
        for alert in alerts:
            alert['_id'] = str(alert['_id'])
        
        return alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/alerts/stats")
async def get_statistics():
    """Get alert statistics"""
    if db is None:
        return {
            'total_alerts': 0,
            'by_severity': {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0},
            'threat_distribution': [],
            'top_source_ips': []
        }
    
    try:
        collection = db['alerts']
        
        # Total alerts
        total = collection.count_documents({})
        
        # By severity
        high = collection.count_documents({'severity': 'HIGH'})
        medium = collection.count_documents({'severity': 'MEDIUM'})
        low = collection.count_documents({'severity': 'LOW'})
        
        # Threat distribution
        pipeline = [
            {'$group': {'_id': '$attack_category', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ]
        threat_dist = list(collection.aggregate(pipeline))
        
        # Top source IPs
        pipeline = [
            {'$match': {'severity': {'$in': ['HIGH', 'MEDIUM']}}},
            {'$group': {'_id': '$source_ip', 'count': {'$sum': 1}, 
                       'avg_risk': {'$avg': '$risk_score'}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ]
        top_ips = list(collection.aggregate(pipeline))
        
        return {
            'total_alerts': total,
            'by_severity': {
                'HIGH': high,
                'MEDIUM': medium,
                'LOW': low
            },
            'threat_distribution': threat_dist,
            'top_source_ips': top_ips
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/alerts/timeline")
async def get_timeline(hours: int = 24):
    """Get alert timeline"""
    if db is None:
        return []
    
    try:
        collection = db['alerts']
        since = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
        
        pipeline = [
            {'$match': {'timestamp': {'$gte': since}}},
            {'$group': {
                '_id': {
                    '$dateToString': {
                        'format': '%Y-%m-%d %H:00',
                        'date': {'$dateFromString': {'dateString': '$timestamp'}}
                    }
                },
                'count': {'$sum': 1},
                'high': {'$sum': {'$cond': [{'$eq': ['$severity', 'HIGH']}, 1, 0]}},
                'medium': {'$sum': {'$cond': [{'$eq': ['$severity', 'MEDIUM']}, 1, 0]}},
                'low': {'$sum': {'$cond': [{'$eq': ['$severity', 'LOW']}, 1, 0]}}
            }},
            {'$sort': {'_id': 1}}
        ]
        
        timeline = list(collection.aggregate(pipeline))
        return timeline
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/security/blocked-ips")
async def get_blocked_ips():
    """Get list of blocked IPs"""
    if db is None:
        return []
    
    try:
        collection = db['blocked_ips']
        blocked = list(collection.find().sort('blocked_at', -1))
        
        for item in blocked:
            item['_id'] = str(item['_id'])
        
        return blocked
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system/status")
async def get_system_status():
    """Get system status"""
    stream_status = stream_service.get_status()
    
    return {
        'status': 'operational',
        'mode': 'real-time',
        'stream_service': stream_status,
        'websocket_connections': ws_manager.get_connection_count(),
        'database_connected': db is not None,
        'timestamp': datetime.utcnow().isoformat()
    }

@app.get("/models/info")
async def get_model_info():
    """Get ML model information"""
    try:
        import joblib
        metadata = joblib.load('backend/ml/models/unsw_model_metadata.pkl')
        return metadata
    except Exception as e:
        return {'error': str(e)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time alerts"""
    await ws_manager.connect(websocket)
    
    try:
        # Send welcome message
        await websocket.send_json({
            'type': 'connected',
            'message': 'Connected to UNSW-NB15 Intrusion Detection System'
        })
        
        # Keep connection alive
        while True:
            try:
                # Wait for client messages (ping/pong)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
            except asyncio.TimeoutError:
                # Send heartbeat
                await websocket.send_json({'type': 'heartbeat'})
            except WebSocketDisconnect:
                break
                
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        ws_manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
