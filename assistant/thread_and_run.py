from openai import OpenAI
import os
import time
client = OpenAI()
# https://platform.openai.com/docs/assistants/overview

OPEN_API_KEY = os.environ.get('OPENAI_API_KEY')
assistant_id = "asst_ohl8sJLMkCw6K6xN0iUrFuwJ"
# assistant = client.beta.assistants.retrieve(assistant_id)

thread = client.beta.threads.create()
print(thread)

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What is the Colab?"
)

# time.sleep(3)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant_id,
  instructions="Please address the user as JUDY. The user has a premium account."
)

# time.sleep(3)

run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

print(run)
# print(messages)

