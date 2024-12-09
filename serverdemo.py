import asyncio
from warpnerf.networking.websocket_client import WebSocketClient

async def main():
    client = WebSocketClient("ws://localhost:8765")

    # Define a subscriber callback
    def on_message(payload):
        print(f"Received message: {payload}")

    # Subscribe to a topic
    unsubscribe_on_message = client.subscribe("chat", on_message)

    # Connect to the server
    await client.connect()

    # Send a message
    await client.send("chat", {"text": "Hello, world!"})

    # Wait for messages or perform other tasks
    await asyncio.sleep(10)

    # Unsubscribe from the topic
    unsubscribe_on_message()

    # Disconnect from the server
    await client.disconnect()

# Run the client
asyncio.run(main())
