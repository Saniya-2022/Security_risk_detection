"""
Quick WebSocket Diagnostic Script
Run this to check if WebSocket is working
"""

import asyncio
import websockets
import json
from datetime import datetime

async def test_websocket():
    print("🔍 Testing WebSocket Connection...")
    print("=" * 60)
    
    try:
        # Connect to WebSocket
        uri = "ws://localhost:8000/ws"
        print(f"📡 Connecting to {uri}...")
        
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket Connected!")
            print("=" * 60)
            print("📨 Waiting for messages (will show first 10)...\n")
            
            message_count = 0
            
            # Listen for messages
            async for message in websocket:
                message_count += 1
                data = json.loads(message)
                
                print(f"\n📬 Message #{message_count}")
                print(f"Type: {data.get('type')}")
                print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
                
                if data.get('type') == 'alert':
                    alert = data.get('data', {})
                    print(f"Threat: {alert.get('threat_type')}")
                    print(f"Severity: {alert.get('severity')}")
                    print(f"Risk Score: {alert.get('risk_score')}")
                elif data.get('type') == 'statistics':
                    stats = data.get('data', {})
                    print(f"Total Alerts: {stats.get('total_alerts')}")
                    print(f"HIGH: {stats.get('by_severity', {}).get('HIGH', 0)}")
                elif data.get('type') == 'connected':
                    print(f"Message: {data.get('message')}")
                elif data.get('type') == 'heartbeat':
                    print(f"Active Connections: {data.get('active_connections')}")
                
                print("-" * 60)
                
                if message_count >= 10:
                    print("\n✅ Test Complete! WebSocket is working!")
                    print("=" * 60)
                    break
                    
    except ConnectionRefusedError:
        print("❌ ERROR: Cannot connect to WebSocket!")
        print("=" * 60)
        print("\n🔧 SOLUTION:")
        print("1. Make sure backend is running:")
        print("   uvicorn backend.api.main_dynamic:app --reload --host 0.0.0.0 --port 8000")
        print("\n2. Check if you see this message:")
        print("   ✅ Mini SIEM is now LIVE and generating events!")
        print("\n3. If not, restart the backend")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("=" * 60)

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🔬 WEBSOCKET DIAGNOSTIC TOOL")
    print("=" * 60)
    print("\nThis will test if your WebSocket is working.")
    print("You should see messages appearing every 3-7 seconds.\n")
    
    try:
        asyncio.run(test_websocket())
    except KeyboardInterrupt:
        print("\n\n⏹️  Test stopped by user")
        print("=" * 60)
