from openai import OpenAI
import time
import json
import requests

client = OpenAI()

assistant_id = "asst_ohl8sJLMkCw6K6xN0iUrFuwJ"

# Creates a thread
message_thread = client.beta.threads.create()
thread_id = message_thread.id

get_current_worker = {
    "name": "get_current_worker",
    "description": "Get the name and other information about who is currently working at TEC (the Co-Lab). Find this information here: https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/CoLab%20Studios/TEC. Sometimes it will be empty, meaning no one is working. If so, respond with 'There is currently no one on shift.'",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {"type": "string"},
            "user_name": {"type": "string", "description": "The name of the current worker on shift e.g. Bob"},
            "status": {"type": "string"},
            "start": {"type": "number"},
            "end": {"type": "number"},
            "expertise": {"type": "string"},
            "netid": {"type": "string"},
            "clocked_in": {"type": "number"}
        },
        # "required": ["user_name"],
        "required": [],
    },
}


updated_assistant = client.beta.assistants.update(
    assistant_id,
    tools=[
        {"type": "retrieval"},
        {"type": "function", "function": get_current_worker},
    ],
)
print(updated_assistant)

