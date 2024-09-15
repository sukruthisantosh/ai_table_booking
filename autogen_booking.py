import os

import json

import uuid

import subprocess

from autogen import ConversableAgent

# automatically terminate at the end system_message="You are helping a user
# book a table acting as a waitor at " "a restaurant called Pappadams," "take
# down email, full name, phone number must be uk" "number of guests, date of
# reservation, time of reservation",

# the chat can't say booking confirmed at the end, we have to confirm, say recieved
booking_details = []

agent_booking_table = ConversableAgent(
    "agent_booking_table",
    system_message="You are a waitor at Pappadams taking a table booking collect name email UK phone number number of guests Date and reservation time",
    llm_config={"config_list": [{"model": "gpt-4o-mini", "temperature": 1,
                                 "api_key": os.environ.get(
                                     "API_KEY")}]},
    # max_consecutive_auto_reply=1,
    human_input_mode="NEVER",
)

human_proxy = ConversableAgent(
    "human_proxy",
    llm_config=False,
    human_input_mode="ALWAYS",
)

result = human_proxy.initiate_chat(
    agent_booking_table,
    message="This is a table booking agent",
)

full_chat = result.chat_history
formatted_chat = "\n".join([str(message) for message in full_chat])

print(formatted_chat)
print("FINISHED")

json_agent = ConversableAgent(
    name="json_agent",
    system_message="extract name email UK phone number number of guests "
                   "Date reservation time from the given chat history in same format every time",
    llm_config={"config_list": [{"model": "gpt-4o-mini", "temperature": 0,
                                 "api_key": os.environ.get(
                                     "API_KEY")}]},
    human_input_mode="NEVER",
)

json_result = human_proxy.initiate_chat(
    json_agent,
    message=formatted_chat,
    max_turns=1
)

chat_summary = json_result.summary

print("chat summary extracted by json agent:")
print(json_result.summary)


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

    time_start = extracted_info.find("Time of Reservation: ") + len(
        "Time of Reservation: ")
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


booking_info = parse_booking_info(chat_summary)

with open("booking_summary.json", "w") as json_file:
    json.dump([booking_info], json_file, indent=1)

print("Booking summary saved to booking_summary.json")

print("add_reservations.py is being executed")

subprocess.run(["python", "add_reservation.py"])

print("finished executing add_reservations.py")

# name is s s, mail is s@gmail.com, number 07960723102, 3 guests, 11/10/2024 reservation at 12pm
# name is sunny windy, mail is sw@gmail.com, number 07937623102, 5 guests, 31/11/2024 reservation at 1pm
