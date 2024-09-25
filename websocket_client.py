import asyncio
import websockets
import json

async def send_booking():
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            booking_info = {
                'message': 'Booking Information',
            }

            # Send the booking info
            await websocket.send(json.dumps(booking_info))
            print(f"Sent: {booking_info}")

            # Wait for the response
            response = await websocket.recv()
            print(f"Received: {response}")

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"WebSocket connection closed with error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        print("Connection closed")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_booking())
