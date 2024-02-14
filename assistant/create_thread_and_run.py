from openai import OpenAI
import os
import time
client = OpenAI()

OPEN_API_KEY = os.environ.get('OPENAI_API_KEY')
assistant_id = "asst_ohl8sJLMkCw6K6xN0iUrFuwJ"
# assistant = client.beta.assistants.retrieve(assistant_id)

run = client.beta.threads.create_and_run(
  assistant_id=assistant_id,
  thread={
    "messages": [
      {"role": "user", 
       "content": "Explain deep learning to a 5 year old."}
    ]
  }
)

# print(run)
thread_id="thread_8lLYf7g4VobYywtU2TZQbENt"
run_id="run_RUDMVfYXjRBhQnoxxl6sKLLV"

run = client.beta.threads.runs.retrieve(
  thread_id=thread_id,
  run_id=run_id
)

print(run)
