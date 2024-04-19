# This is a general purpose file that we used to test different endpoints of the API like thread and retrieving messages

from openai import OpenAI
import os
import time
import json
import re
client = OpenAI()
# https://platform.openai.com/docs/assistants/overview
# GUIDE: https://medium.com/@nilakashdas/how-to-use-openais-assistants-api-in-python-a-beginner-friendly-guide-04bd6249f330  

# problem -> doesn't use file given

OPEN_API_KEY = os.environ.get('OPENAI_API_KEY')

# # This is a test to create an assistant from python. 
# # Don't run this program several times, otherwise you'll end up creating a bunch of assistants
# colab_assistant = client.beta.assistants.create(
#     instructions="You are the assistant of Duke's Innovation Colab. Your main role is to assist students in answering their questions. Most of the students come for help to use tools like 3d printers, laser cutters, or software. All the information that you need is the document provided. Anything else, you don't know. You should avoid answering questions that don't have a relationship with the Colab or its facilities. If someone asks anything that is not related to the colab, you should respond that you are not able to answer their questions",
#     name="Colab Assistnat",
#     tools=[{"type": "retrieval"}],
#     model="gpt-3.5-turbo-0125",
# )

# GET ALL DATA
my_assistants = client.beta.assistants.list(
    order="desc",
    limit="20",
)
for item in my_assistants.data:
      assistant_id = item.id

assistant_files = client.beta.assistants.files.list(
  assistant_id=assistant_id
)
for item in assistant_files.data:
      file_id = item.id

message_thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Hello, what is the Colab?",
      "file_ids": [file_id],
    },
    # {
    #   "role": "user",
    #   "content": "Where is the Ruby?", 
    #   "file_ids": [file_id]
    # },
  ]
)

thread_id = message_thread.id
my_thread = client.beta.threads.retrieve(thread_id)

start_run = client.beta.threads.runs.create(
  thread_id=thread_id,
  assistant_id=assistant_id,
  instructions="Answer the questions."
)

run_id = start_run.id


# GET ANSWERS 

while True:
    run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    if run_status.status == "completed":
        break
    elif run_status.status == "failed":
        print("Run failed:", run_status.last_error)
        break
    time.sleep(2)  

messages = client.beta.threads.messages.list(
    thread_id=thread_id
)

number_of_messages = len(messages.data)
print( f'Number of messages: {number_of_messages}')

for message in reversed(messages.data):
    role = message.role  
    for content in message.content:
        if content.type == 'text':
            response = content.text.value 
            print(f'\n{role}: {response}')






