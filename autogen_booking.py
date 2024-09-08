import os

import json

from autogen import ConversableAgent

# automatically terminate at the end system_message="You are helping a user
# book a table acting as a waitor at " "a restaurant called Pappadams," "take
# down email, full name, phone number must be uk" "number of guests, date of
# reservation, time of reservation",

# dict which stores the details of the reservation
booking_details = []

agent_booking_table = ConversableAgent(
    "agent_booking_table",
    system_message="You are a waitor at Pappadams taking a table booking collect full name email UK phone number number of guests Date and reservation time",
    llm_config={"config_list": [{"model": "gpt-4o-mini","temperature":1,"api_key": os.environ.get("API_KEY")}]},
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
    system_message="extract full name email UK phone number number of guests "
                   "Date reservation time from the given chat history ",
    llm_config={"config_list": [{"model": "gpt-4o-mini","temperature":0,"api_key": os.environ.get("API_KEY")}]},
    human_input_mode="NEVER"
)

json_result = human_proxy.initiate_chat(
    json_agent,
    message= formatted_chat
)

extracted_info = json_result.summary

print("chat summary extracted by json agent:")
print(json_result.summary)

with open("booking_summary.json", "w") as json_file:
    json.dump(extracted_info, json_file, indent=1)


# name is s s, mail is s@gmail.com, number 07960723102, 3 guests, 11/10/2024 reservation at 12pm




