"""
Enterprise SIEM API
Main FastAPI application with all enterprise features
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from datetime import datetime
import logging

from backend.database.mongo import get_database
from backend.api.websocket_manager import WebSocketManager
from backend.runtime.email_service import EmailService
from backend.event_generator import EventGenerator
from backend.alert_service_enterprise import EnterpriseAlertService
from backend.api.incident_routes import router as incident_router, set_database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global instances
websocket_manager = WebSocketManager()
email_service = None
alert_service = None
event_generator = None
db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global db, email_service, alert_service, event_generator
    
    # Startup
    logger.info("🚀 Starting Enterprise SIEM...")
    
    # Initialize database
    db = await get_database()
    logger.info("✅ Database connected")
    
    # Set database for incident routes
    set_database(db)
    
    # Initialize email service
    try:
        email_service = EmailService()
        logger.info("✅ Email service initialized")
    except Exception as e:
        logger.warning(f"⚠️ Email service not available: {e}")
    
    # Initialize alert service
    alert_service = EnterpriseAlertService(db, websocket_manager, email_service)
    logger.info("✅ Enterprise alert service initialized")
    
    # Initialize and start event generator
    event_generator = EventGenerator(alert_service)
    asyncio.create_task(event_generator.start())
    logger.info("✅ Event generator started")
    
    logger.info("🎯 Enterprise SIEM ready!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Enterprise SIEM...")
    if event_generator:
        await event_generator.stop()

# Create FastAPI app
app = FastAPI(
    title="Mini SIEM Enterprise Edition",
    description="Enterprise-grade Security Information and Event Management System",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include incident management routes
app.include_router(incident_router)

# ============================================================================
# WEBSOCKET ENDPOINT
# ============================================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket_manager.connect(websocket)
    try:
        # Send welcome message
        await websocket.send_json({
            'type': 'connected',
            'message': 'Connected to Enterprise SIEM',
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Keep connection alive
        while True:
            try:
                # Receive messages (for heartbeat)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                
                # Echo back for heartbeat
                await websocket.send_json({
                    'type': 'heartbeat',
                    'timestamp': datetime.utcnow().isoformat()
                })
            except asyncio.TimeoutError:
                # Send heartbeat
                await websocket.send_json({
                    'type': 'heartbeat',
                    'timestamp': datetime.utcnow().isoformat()
                })
                
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        websocket_manager.disconnect(websocket)

# ============================================================================
# ALERT ENDPOINTS
# ============================================================================

@app.get("/alerts")
async def get_alerts(
    limit: int = Query(50, le=500),
    severity: str = Query(None),
    threat_type: str = Query(None)
):
    """Get recent alerts with optional filters"""
    try:
        query = {}
        if severity:
            query['severity'] = severity.upper()
        if threat_type:
            query['threat_type'] = {'$regex': threat_type, '$options': 'i'}
        
        cursor = db.alerts.find(query).sort('timestamp', -1).limit(limit)
        alerts = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string
        for alert in alerts:
            alert['_id'] = str(alert['_id'])
            if isinstance(alert.get('timestamp'), datetime):
                alert['timestamp'] = alert['timestamp'].isoformat()
        
        return alerts
    except Exception as e:
        logger.error(f"Error fetching alerts: {e}")
        return []

@app.get("/alerts/stats")
async def get_alert_stats():
    """Get alert statistics"""
    try:
        # Total alerts
        total = await db.alerts.count_documents({})
        
        # By severity
        severity_pipeline = [
            {'$group': {'_id': '$severity', 'count': {'$sum': 1}}}
        ]
        severity_results = await db.alerts.aggregate(severity_pipeline).to_list(length=100)
        by_severity = {item['_id']: item['count'] for item in severity_results}
        
        # Threat distribution
        threat_pipeline = [
            {'$group': {'_id': '$threat_type', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ]
        threat_results = await db.alerts.aggregate(threat_pipeline).to_list(length=10)
        
        # Active connections
        active_connections = len(websocket_manager.active_connections)
        
        return {
            'total_alerts': total,
            'by_severity': by_severity,
            'threat_distribution': threat_results,
            'active_connections': active_connections
        }
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return {
            'total_alerts': 0,
            'by_severity': {},
            'threat_distribution': [],
            'active_connections': 0
        }

@app.get("/alerts/{alert_id}")
async def get_alert(alert_id: str):
    """Get specific alert by ID"""
    try:
        from bson import ObjectId
        alert = await db.alerts.find_one({'_id': ObjectId(alert_id)})
        
        if alert:
            alert['_id'] = str(alert['_id'])
            if isinstance(alert.get('timestamp'), datetime):
                alert['timestamp'] = alert['timestamp'].isoformat()
            return alert
        
        return {'error': 'Alert not found'}
    except Exception as e:
        logger.error(f"Error fetching alert: {e}")
        return {'error': str(e)}

@app.get("/alerts/timeline")
async def get_alert_timeline(hours: int = Query(24, le=168)):
    """Get alert timeline for visualization"""
    try:
        from datetime import timedelta
        
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        
        pipeline = [
            {'$match': {'timestamp': {'$gte': cutoff}}},
            {
                '$group': {
                    '_id': {
                        'hour': {'$hour': '$timestamp'},
                        'severity': '$severity'
                    },
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'_id.hour': 1}}
        ]
        
        results = await db.alerts.aggregate(pipeline).to_list(length=1000)
        return results
        
    except Exception as e:
        logger.error(f"Error fetching timeline: {e}")
        return []

# ============================================================================
# SECURITY ENDPOINTS
# ============================================================================

@app.get("/security/blocked-ips")
async def get_blocked_ips():
    """Get list of blocked IPs"""
    try:
        cursor = db.blocked_ips.find().sort('blocked_at', -1)
        blocked_ips = await cursor.to_list(length=1000)
        
        for ip in blocked_ips:
            ip['_id'] = str(ip['_id'])
            if isinstance(ip.get('blocked_at'), datetime):
                ip['blocked_at'] = ip['blocked_at'].isoformat()
            if isinstance(ip.get('last_blocked'), datetime):
                ip['last_blocked'] = ip['last_blocked'].isoformat()
        
        return blocked_ips
    except Exception as e:
        logger.error(f"Error fetching blocked IPs: {e}")
        return []

@app.post("/security/block-ip")
async def block_ip(ip_address: str, reason: str = "Manual block"):
    """Manually block an IP address"""
    try:
        existing = await db.blocked_ips.find_one({'ip_address': ip_address})
        
        if existing:
            return {'message': 'IP already blocked', 'ip_address': ip_address}
        
        await db.blocked_ips.insert_one({
            'ip_address': ip_address,
            'reason': reason,
            'blocked_at': datetime.utcnow(),
            'last_blocked': datetime.utcnow(),
            'block_count': 1,
            'auto_blocked': False
        })
        
        # Broadcast
        await websocket_manager.broadcast({
            'type': 'ip_blocked',
            'data': {'ip_address': ip_address, 'reason': reason}
        })
        
        return {'message': 'IP blocked successfully', 'ip_address': ip_address}
        
    except Exception as e:
        logger.error(f"Error blocking IP: {e}")
        return {'error': str(e)}

@app.delete("/security/unblock-ip/{ip_address}")
async def unblock_ip(ip_address: str):
    """Unblock an IP address"""
    try:
        result = await db.blocked_ips.delete_one({'ip_address': ip_address})
        
        if result.deleted_count > 0:
            return {'message': 'IP unblocked successfully', 'ip_address': ip_address}
        
        return {'message': 'IP not found in blocklist', 'ip_address': ip_address}
        
    except Exception as e:
        logger.error(f"Error unblocking IP: {e}")
        return {'error': str(e)}

# ============================================================================
# SYSTEM ENDPOINTS
# ============================================================================

@app.get("/system/status")
async def get_system_status():
    """Get system status"""
    return {
        'status': 'operational',
        'mode': 'enterprise',
        'version': '2.0.0',
        'event_generator_running': event_generator.running if event_generator else False,
        'active_websocket_connections': len(websocket_manager.active_connections),
        'email_service_enabled': email_service is not None,
        'features': [
            'Real-time event generation',
            'Threat intelligence enrichment',
            'Anomaly detection',
            'MITRE ATT&CK mapping',
            'Advanced risk scoring',
            'Event correlation',
            'Incident management',
            'Auto IP blocking',
            'Email alerts'
        ]
    }

@app.get("/system/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database
        await db.command('ping')
        
        return {
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        'name': 'Mini SIEM Enterprise Edition',
        'version': '2.0.0',
        'status': 'operational',
        'docs': '/docs',
        'features': [
            'ML-based threat detection',
            'Threat intelligence enrichment',
            'Behavioral anomaly detection',
            'MITRE ATT&CK framework mapping',
            'Advanced risk scoring',
            'Event correlation engine',
            'Incident management',
            'Real-time WebSocket updates',
            'Automatic IP blocking',
            'Email alerting'
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
