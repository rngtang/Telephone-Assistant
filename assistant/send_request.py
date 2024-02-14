from openai import OpenAI
import os
import time
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
thread_message = client.beta.threads.messages.create(
  thread.id,
  role="user",
  content="what is the colab?",
)

time.sleep(3)

# Creates a run
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Answer the question"
)

time.sleep(3)
# print(run.id)

# run = client.beta.threads.runs.retrieve(
#   thread_id="thread_1jRO1AFXA6nAjxOngn3xjQID",
#   run_id="run_bG5kKz2Y6zKjCcstm8WeppNY"
# )

# print(run)

# Gets the responses from the thread
messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

print(messages)
# print(thread_message)