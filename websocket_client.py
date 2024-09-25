import asyncio
import websockets
import json

async def send_booking():
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            booking_info = input("This is a table booking agent, what would you like to say? ")

            await websocket.send(booking_info)
            print(f"Sent: {booking_info}")


            while True:
                msg = await websocket.recv()
                print(msg)


    except websockets.exceptions.ConnectionClosedError as e:
        print(f"WebSocket connection closed with error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        print("Connection closed")


asyncio.run(send_booking())


