import os

from autogen import ConversableAgent

# automatically terminate at the end system_message="You are helping a user
# book a table acting as a waitor at " "a restaurant called Pappadams," "take
# down email, full name, phone number must be uk" "number of guests, date of
# reservation, time of reservation",

agent_booking_table = ConversableAgent(
    "agent_booking_table",
    system_message="You are a waitor at Pappadams taking a table booking collect full name email UK phone number number of guests Date and reservation time",
    llm_config={"config_list": [{"model": "gpt-4o-mini","temperature":1 ,"api_key": os.environ.get("API_KEY")}]},
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

print(result)