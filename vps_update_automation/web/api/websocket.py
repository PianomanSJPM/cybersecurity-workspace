import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Set

import websockets
from websockets.exceptions import ConnectionClosed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Store active connections
connections: Dict[str, Set[websockets.WebSocketServerProtocol]] = {
    'backups': set(),
    'updates': set(),
    'security': set()
}

async def register(websocket: websockets.WebSocketServerProtocol, channel: str):
    """Register a new WebSocket connection."""
    connections[channel].add(websocket)
    logger.info(f"New connection registered for channel: {channel}")

async def unregister(websocket: websockets.WebSocketServerProtocol, channel: str):
    """Unregister a WebSocket connection."""
    connections[channel].remove(websocket)
    logger.info(f"Connection unregistered from channel: {channel}")

async def broadcast(channel: str, message: dict):
    """Broadcast a message to all connections in a channel."""
    if not connections[channel]:
        return
    
    message['timestamp'] = datetime.utcnow().isoformat()
    message_str = json.dumps(message)
    
    websockets_to_remove = set()
    for websocket in connections[channel]:
        try:
            await websocket.send(message_str)
        except ConnectionClosed:
            websockets_to_remove.add(websocket)
        except Exception as e:
            logger.error(f"Error broadcasting message: {e}")
            websockets_to_remove.add(websocket)
    
    # Remove dead connections
    for websocket in websockets_to_remove:
        await unregister(websocket, channel)

async def handle_connection(websocket: websockets.WebSocketServerProtocol, path: str):
    """Handle a new WebSocket connection."""
    try:
        # Extract channel from path
        channel = path.strip('/')
        if channel not in connections:
            await websocket.close(1008, "Invalid channel")
            return
        
        await register(websocket, channel)
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    # Handle incoming messages if needed
                    logger.info(f"Received message on {channel}: {data}")
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON received: {message}")
        except ConnectionClosed:
            pass
        finally:
            await unregister(websocket, channel)
    except Exception as e:
        logger.error(f"Error handling connection: {e}")
        try:
            await websocket.close(1011, "Internal server error")
        except:
            pass

async def start_server(host: str = 'localhost', port: int = 5000):
    """Start the WebSocket server."""
    server = await websockets.serve(
        handle_connection,
        host,
        port,
        ping_interval=30,
        ping_timeout=10
    )
    
    logger.info(f"WebSocket server started on ws://{host}:{port}")
    return server

def run_server(host: str = 'localhost', port: int = 5000):
    """Run the WebSocket server."""
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(start_server(host, port))
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

if __name__ == '__main__':
    run_server() 