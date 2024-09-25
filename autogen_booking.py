import json
import uuid
import subprocess
import asyncio
import websockets
from autogen import ConversableAgent
from autogen.io.websockets import IOWebsockets


def parse_booking_info(extracted_info):
    name_start = extracted_info.find("Name:") + len("Name: ")
    name_end = extracted_info.find("\n", name_start)
    full_name = extracted_info[name_start:name_end].strip()

    email_start = extracted_info.find("Email: ") + len("Email: ")
    email_end = extracted_info.find("\n", email_start)
    email = extracted_info[email_start:email_end].strip()

    phone_start = extracted_info.find("UK Phone Number: ") + len(
        "UK Phone Number: ")
    phone_end = extracted_info.find("\n", phone_start)
    phone_number = extracted_info[phone_start:phone_end].strip()

    guests_start = extracted_info.find("Number of Guests: ") + len(
        "Number of Guests: ")
    guests_end = extracted_info.find("\n", guests_start)
    number_of_guests = extracted_info[guests_start:guests_end].strip()

    date_start = extracted_info.find("Date of Reservation: ") + len(
        "Date of Reservation: ")
    date_end = extracted_info.find("\n", date_start)
    reservation_date = extracted_info[date_start:date_end].strip()

    time_start = extracted_info.find("Reservation Time: ") + len(
        "Reservation Time: ")
    reservation_time = extracted_info[time_start:].strip()

    booking_id = str(uuid.uuid4())

    return {
        "booking_id": booking_id,
        "full_name": full_name,
        "email": email,
        "phone_number": phone_number,
        "number_of_guests": number_of_guests,
        "date": reservation_date,
        "time": reservation_time
    }


async def process_booking(websocket):
    try:
        while True:
            data = await websocket.recv()
            print(f"Received message: {data}")

            api_key = "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"

            agent_booking_table = ConversableAgent(
                "agent_booking_table",
                system_message="You are a waitor at Pappadams taking a table booking collect name email UK phone number number of guests Date and reservation time",
                llm_config={"config_list": [
                    {"model": "gpt-4o-mini", "temperature": 1,
                     "api_key": api_key}]},
                human_input_mode="NEVER",
            )

            human_proxy = ConversableAgent(
                "human_proxy",
                llm_config=False,
                human_input_mode="ALWAYS",
            )

            result = human_proxy.initiate_chat(
                agent_booking_table,
                message=data
            )

            full_chat = result.chat_history
            formatted_chat = "\n".join([str(message) for message in full_chat])

            json_agent = ConversableAgent(
                name="json_agent",
                system_message="extract name email UK phone number number of guests Date reservation time from the given chat history in same format every time",
                llm_config={"config_list": [
                    {"model": "gpt-4o-mini", "temperature": 0,
                     "api_key": api_key}]},
                human_input_mode="NEVER",
            )

            json_result = human_proxy.initiate_chat(
                json_agent,
                message=formatted_chat,
                max_turns=1
            )

            chat_summary = json_result.summary
            booking_info = parse_booking_info(chat_summary)

            with open("booking_summary.json", "w") as json_file:
                json.dump([booking_info], json_file, indent=1)

            print(f"Booking summary saved: {booking_info}")

            await websocket.send(json.dumps({
                "status": "Received",
                "booking_id": booking_info["booking_id"]
            }))

            subprocess.run(["python", "add_reservation.py"])
            print("Finished executing add_reservation.py")

            await websocket.close()
            print("Websocket connection closed")

            asyncio.get_event_loop().stop()

    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed")


start_server = websockets.serve(process_booking, "localhost", 8765)

print("WebSocket server started on ws://localhost:8765")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
