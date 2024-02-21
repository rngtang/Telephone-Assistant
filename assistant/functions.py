from openai import OpenAI
import time
import json
import os
import requests

client = OpenAI()

assistant_id = os.environ.get("ASSISTANT_ID")
print("Hello, how can I help you?")

# Creates a thread
message_thread = client.beta.threads.create()
thread_id = message_thread.id
url = 'https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/CoLab%20Studios/TEC'

# parse the info
def get_info(url):
    response = requests.get(url)
    returning = []
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

            returning.append(user_name)

# def get_current_worker:
#     if 
            

# put the info in the function somehow -> function outline in add_function.py
# https://medium.com/@ralfelfving/learn-function-calls-in-openai-assistants-api-519ecc7596ce 


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

while True:
    question = input("Ask me anything: ")

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question
    )

    start_run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="You are the assistant of Duke's Innovation Colab. Your main role is to assist students in answering their questions. Most of the students come for help to use tools like 3d printers, laser cutters, or software. All the information that you need is the document provided, or in the links of functions for function calls. You should avoid answering questions that don't have a relationship with the Colab or its facilities. If someone asks anything that is not related to the colab, you should respond that you are not able to answer their questions."
    )

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

    run_id = start_run.id

    # Waits until gets the response
    print("Thinking...")
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        # If there is a response
        if run_status.status == "completed":
            break
        # If it requires to call a function
        elif run_status.status == "requires_action":
            try: 
                tool_call = run_status.required_action.submit_tool_outputs.tool_calls[0]
                print(tool_call)
                print(tool_call.function)
                name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                print("Function Name:", name)
                print("Function Arguments:", arguments)

                # try: 
                if(name == "get_current_worker"):
                    info = get_info(url)
                else:
                    print("Could not identify tool")
                    break
                # except: 
                #     print("failed case 1")

                try: 
                    function_run = client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run_id,
                        tool_outputs="test"
                    )
                except:
                    print("failed case 2")
                
                try: 
                    run = wait_on_run(function_run, message_thread)
                    function_response = get_response(message_thread)
                except:
                    print("failed case 3")
                # print(get_response(message_thread))

                try: 
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "function",
                        "name": get_current_worker,
                        "content": str(function_response)  # Append the Python dictionary here
                    })
                except:
                    print("failed case 4")
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



