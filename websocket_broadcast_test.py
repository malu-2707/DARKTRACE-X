import asyncio

import websockets


async def test_broadcast():
    async with websockets.connect("ws://127.0.0.1:8000/ws") as websocket:
        print("Dashboard connected")

        await websocket.send("dashboard_ready")
        print("Dashboard connection active")

        try:
            message = await asyncio.wait_for(
                websocket.recv(),
                timeout=3
            )
            print("Received:", message)
        except asyncio.TimeoutError:
            print("No broadcast received")


asyncio.run(test_broadcast())