"""
Enhanced WebSocket Manager for Real-Time Alert Broadcasting
Pushes alerts to connected clients instantly with heartbeat
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
import json
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections and broadcasts"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.heartbeat_task = None
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"✅ New WebSocket connection. Total: {len(self.active_connections)}")
        
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to Mini SIEM",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"❌ WebSocket disconnected. Total: {len(self.active_connections)}")
    
    async def broadcast_alert(self, alert: Dict[str, Any]):
        """Broadcast alert to all connected clients"""
        
        message = {
            "type": "alert",
            "data": alert,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self._broadcast(message)
    
    async def broadcast_statistics(self, stats: Dict[str, Any]):
        """Broadcast updated statistics"""
        
        message = {
            "type": "statistics",
            "data": stats,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self._broadcast(message)
    
    async def broadcast_system_status(self, status: Dict[str, Any]):
        """Broadcast system status update"""
        
        message = {
            "type": "system_status",
            "data": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self._broadcast(message)
    
    async def broadcast_ip_block(self, ip_address: str, reason: str):
        """Broadcast IP block notification"""
        
        message = {
            "type": "ip_blocked",
            "data": {
                "ip_address": ip_address,
                "reason": reason,
                "blocked_at": datetime.utcnow().isoformat()
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self._broadcast(message)
    
    async def _broadcast(self, message: Dict[str, Any]):
        """Internal method to broadcast to all clients"""
        
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error sending to client: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)
    
    async def send_heartbeat(self):
        """Send periodic heartbeat to keep connections alive"""
        while True:
            try:
                await asyncio.sleep(30)  # Every 30 seconds
                
                if self.active_connections:
                    message = {
                        "type": "heartbeat",
                        "active_connections": len(self.active_connections),
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    await self._broadcast(message)
                    
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
    
    def start_heartbeat(self):
        """Start heartbeat task"""
        if not self.heartbeat_task:
            self.heartbeat_task = asyncio.create_task(self.send_heartbeat())
            logger.info("💓 Heartbeat started")
    
    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)


# Global connection manager instance
manager = ConnectionManager()


class WebSocketManager:
    """WebSocket Manager for Enterprise SIEM"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"✅ WebSocket connected. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"❌ WebSocket disconnected. Total: {len(self.active_connections)}")
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

