from openai import OpenAI
import time
import os
import requests

# Variables
url = 'https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/CoLab%20Studios/TEC'

# Sets up the client
client = OpenAI()

# Gets Assistant ID from the OS
assistant_id = os.environ.get("ASSISTANT_ID")
print("Hello, how can I help you?")

# Creates a thread
message_thread = client.beta.threads.create()
thread_id = message_thread.id

# Calls the API to get the current workers
def getInfo(url):
    # Calls the API
    response = requests.get(url)

    # Creates empty array that will contain the name of the workers
    workers = ""

    # Checks return status
    if response.status_code == 200:
        # Parses through the json response and appends the names to the list
        data = response.json()
        for worker in data:
            workers = workers + ", " + worker["user_name"]
    
    return workers[2:]

# Main function
def main():
    while True:
        # Follow up promp
        question = input("Ask me anything: ")

        # Adds messsage to the thread
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


        time.sleep(2)
        # Gets the current status
        run_id = start_run.id
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

        # Printes the status of the run. Ex: "in_progress", "requires_action", "completed"
        print(run.status)

        # If it requires to call the API
        if(run.status == "requires_action"):
            tool_calls = run.required_action.submit_tool_outputs.tool_calls[0]
            print(tool_calls)

            if(tool_calls.function.name == "get_current_worker"):
                # Calls the api
                workers = getInfo(url)
                # print(workers)

                # Appends to an output list
                tool_outputs = []
                tool_outputs.append({"tool_call_id":tool_calls.id, "output": workers})
                print(tool_outputs)

                # Sends the the parameters with the tools
                run = client.beta.threads.runs.submit_tool_outputs(
                    run_id=run_id,
                    thread_id=thread_id,
                    tool_outputs=tool_outputs
                )
        else:
            # If the question can be answered without using the API
            print("No need to use API")
        
        # Creates the answer
        print("Thinking...")
        while True:
            # gets the current run status
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            print(run.status)
            # If the model finishes formulating the answer, breaks the lop
            if run.status == "completed":
                break
            # If for some reason it fails
            elif run.status == "failed":
                print("Run failed:", run.last_error)
                break
            time.sleep(1.5)

        # Retrives the messages from the thread
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
                

if __name__ == "__main__":
    main()