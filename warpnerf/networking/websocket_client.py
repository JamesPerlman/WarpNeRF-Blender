import asyncio
from collections import defaultdict
from warpnerf.libs import msgpack
import warpnerf.libs.websockets as websockets

class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.is_connected = False
        self.subscribers = defaultdict(list)  # Topic -> List of callback functions


    def subscribe(self, topic, callback) -> callable:
        """Subscribe to a topic with a callback function."""

        self.subscribers[topic].append(callback)

        def unsubscribe():
            self.unsubscribe(topic, callback)

        return unsubscribe

    def unsubscribe(self, topic, callback):
        """Unsubscribe a callback from a topic."""
        
        if callback in self.subscribers[topic]:
            self.subscribers[topic].remove(callback)    
            if not self.subscribers[topic]:
                del self.subscribers[topic]

    async def _dispatch_message(self, message):
        """Dispatch a message to the appropriate subscribers."""
        try:
            data = msgpack.unpackb(message)
            topic = data.get("topic")
            payload = data.get("payload")

            if topic in self.subscribers:
                for callback in self.subscribers[topic]:
                    callback(payload)  # Notify subscribers
        
        except Exception as e:
            print(f"Failed to dispatch message: {e}")

    async def listen(self):
        """Listen for incoming WebSocket messages."""
        
        try:
            while self.is_connected:
                message = await self.websocket.recv()
                await self._dispatch_message(message)
        
        except Exception as e:
            print(f"Listening error: {e}")

    async def connect(self):
        """Connect to the WebSocket server."""
        try:
            self.websocket = await websockets.connect(self.uri)
            self.is_connected = True
            print(f"Connected to {self.uri}")

            # Start the listening task
            asyncio.create_task(self.listen())

        except Exception as e:
            print(f"Connection error: {e}")

    async def send(self, topic, payload):
        """Send a message to the WebSocket server."""
        if self.websocket:
            try:
                message = msgpack.packb({"topic": topic, "payload": payload})
                await self.websocket.send(message)
            
            except Exception as e:
                print(f"Failed to send message: {e}")
        
        else:
            print("Not connected to the server.")

    async def disconnect(self):
        """Disconnect from the WebSocket server."""
        
        self.is_connected = False
        
        if self.websocket:
            await self.websocket.close()
            print("Disconnected from the server.")
