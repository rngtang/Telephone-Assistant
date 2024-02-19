from openai import OpenAI
import time
client = OpenAI()

assistant_id = "asst_ohl8sJLMkCw6K6xN0iUrFuwJ"
print("Hello, how can I help you?")

# Creates a thread
message_thread = client.beta.threads.create()
thread_id = message_thread.id

while True:
    question = input("Ask me anything: ")

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question
    )

    # Starts a run
    start_run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions="You are the assistant of Duke's Innovation Colab. Your main role is to assist students in answering their questions. Most of the students come for help to use tools like 3d printers, laser cutters, or software. All the information that you need is the document provided. You should avoid answering questions that don't have a relationship with the Colab or its facilities. If someone asks anything that is not related to the colab, you should respond that you are not able to answer their questions"
    )

    run_id = start_run.id

    # Waits until gets the response
    print("Thinking...")
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
    for i in reversed(range(0,2)):
        message = messages.data[i]
        role = message.role
        for content in message.content:
            if content.type == 'text':
                response = content.text.value 
                print(f'\n{role}: {response}')
    print("\n")
