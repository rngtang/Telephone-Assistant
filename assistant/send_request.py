from openai import OpenAI
import os
client = OpenAI()

# Added the assistant id to the environment variables but it when called, it returns None
# print(os.environ.get("ASSISTANT_ID"))

# Gets the assistant by id
assistant_id = "asst_ohl8sJLMkCw6K6xN0iUrFuwJ"
assistant = client.beta.assistants.retrieve(assistant_id)
# print(assistant)

# Creates a thread
thread = client.beta.threads.create()

# Adds message to thread
