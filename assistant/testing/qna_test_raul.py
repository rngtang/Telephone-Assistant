# The purpose of this file is to test how to ask and get the answer for a single question

from openai import OpenAI
import time
import os
client = OpenAI()

assistant_id = os.environ.get("ASSISTANT_ID")

# Creates a thread and adds a message
message_thread = client.beta.threads.create(
  messages=[
    {
        "role": "user",
        "content": "What is the colab?"
    }
  ]
)

# print("Assistant id: {id}".format(id=assistant_id))

thread_id = message_thread.id
# print("Thread id: {id}".format(id=thread_id))

# Starts a run
start_run = client.beta.threads.runs.create(
  thread_id=thread_id,
  assistant_id=assistant_id,
  instructions="Answer the questions."
)

run_id = start_run.id

# Waits until gets the response
while True:
    run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    if run_status.status == "completed":
        break
    elif run_status.status == "failed":
        print("Run failed:", run_status.last_error)
        break
    time.sleep(2)  

# Retrives the messages
messages = client.beta.threads.messages.list(
  thread_id=thread_id
)

# Prints the messages
for message in reversed(messages.data):
    role = message.role  
    for content in message.content:
        if content.type == 'text':
            response = content.text.value 
            print(f'\n{role}: {response}')