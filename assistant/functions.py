from openai import OpenAI
import time
import json
import requests

client = OpenAI()

assistant_id = "asst_ohl8sJLMkCw6K6xN0iUrFuwJ"
print("Hello, how can I help you?")

# Creates a thread
message_thread = client.beta.threads.create()
thread_id = message_thread.id
url = 'https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/CoLab%20Studios/TEC'

def get_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for item in data:
            location = item['location']
            user_name = item['user_name']
            status = item['status']
            start = item['start']
            end = item['end']
            expertise = item['expertise']
            netid = item['netid']
            clocked_in = item['clocked_in']
    #     parameters_object = {
    #         "location": location,
    #         "user_name": user_name,
    #         "status": status,
    #         "start": start,
    #         "end": end,
    #         "expertise": expertise,
    #         "netid": netid,
    #         "clocked_in": clocked_in
    #     }
    #     print(parameters_object)
    # else:
    #     print(f"Failed to fetch data from {url}. Status code: {response.status_code}")


# create smaller subfunctions for use: https://cookbook.openai.com/examples/assistants_api_overview_python 
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

# def submit_message(assistant_id, thread, user_message):
#     client.beta.threads.messages.create(
#         thread_id=thread.id, role="user", content=user_message
#     )
#     return client.beta.threads.runs.create(
#         thread_id=thread.id,
#         assistant_id=assistant_id,
#     )

# def create_thread_and_run(user_input):
#     thread = client.beta.threads.create()
#     run = submit_message(assistant_id, thread, user_input)
#     return thread, run


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
        instructions="You are the assistant of Duke's Innovation Colab. Your main role is to assist students in answering their questions. Most of the students come for help to use tools like 3d printers, laser cutters, or software. All the information that you need is the document provided, or in the links of functions for function calls. You should avoid answering questions that don't have a relationship with the Colab or its facilities. If someone asks anything that is not related to the colab, you should respond that you are not able to answer their questions."
    )

    run_id = start_run.id

    # Waits until gets the response
    print("Thinking...")
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run_status.status == "completed":
            break
        elif run_status.status == "requires_action":
            try: 
                tool_call = run_status.required_action.submit_tool_outputs.tool_calls[0]
                print(tool_call)
                print(tool_call.function)
                name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                print("Function Name:", name)
                print("Function Arguments:", arguments)

                function_run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run_id,
                    tool_outputs=[
                        {
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(arguments),
                        }
                    ],
                )

                run = wait_on_run(function_run, message_thread)
                print(get_response(message_thread))

                break
            except: 
                print("Tool call failed")
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
        try:
            message = messages.data[i]
            role = message.role
            for content in message.content:
                if content.type == 'text':
                    response = content.text.value 
                    print(f'\n{role}: {response}')
        except: 
            print("No return message")
    print("\n")



