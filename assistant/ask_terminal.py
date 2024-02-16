from openai import OpenAI
import time
client = OpenAI()

assistant_id = "asst_ohl8sJLMkCw6K6xN0iUrFuwJ"

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
for i in range(1,3):
    message = messages.data[len(messages.data)-i]
    role = message.role
    for content in message.content:
        if content.type == 'text':
            response = content.text.value 
            print(f'\n{role}: {response}')
