import asyncio
import websockets


async def test_websocket():
    async with websockets.connect("ws://127.0.0.1:8000/ws") as websocket:
        print("Connected to WebSocket")
        await websocket.send("dashboard_test")
        print("Test message sent")

        try:
            message = await asyncio.wait_for(
                websocket.recv(),
                timeout=3
            )
            print("Received:", message)
        except asyncio.TimeoutError:
            print("No broadcast received - connection is still active")


asyncio.run(test_websocket())