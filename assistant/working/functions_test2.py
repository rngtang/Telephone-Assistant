from openai import OpenAI
import time
import os
import requests

# Global variables
StudioUrl = 'https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/CoLab%20Studios/TEC'
StudentDevsUrl = 'https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/Colab%20Student%20Developer/TEC%20Office%20Hours'
rootClasses = 'https://api.pathways.duke.edu/api/v1/signage_sync?location=1'
assistant_id = os.environ.get("ASSISTANT_ID")

# Sets up the client
client = OpenAI()

# Creates a thread
message_thread = client.beta.threads.create()
thread_id = message_thread.id

def getRoots():
    response = requests.get(rootClasses)
    classes = ""

    if(response.status == 200):
        data = response.json()
        for c in data:
            classes = classes + ", " + c["course_name"] + ": " + c["start"] 

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

def requiresAction(run, run_id):
    # prints which functioned is called
    tool_calls = run.required_action.submit_tool_outputs.tool_calls[0]
    print(tool_calls)

    # Calls the API
    workers = getInfo(StudioUrl) if tool_calls.function.name == "get_current_worker" else getInfo(StudentDevsUrl)

    # Appends to an output list
    tool_outputs = []
    tool_outputs.append({"tool_call_id":tool_calls.id, "output": workers})
    # print(tool_outputs)

    # Sends the the parameters with the tools
    run = client.beta.threads.runs.submit_tool_outputs(
        run_id=run_id,
        thread_id=thread_id,
        tool_outputs=tool_outputs
    )

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
            instructions="You are the assistant of Duke's Innovation Colab. Your main role is to assist students in answering their questions. Most of the students come for help to use tools like 3d printers, laser cutters, or software. All the information that you need is the document provided, or in the links of functions for function calls. You should avoid answering questions that don't have a relationship with the Colab or its facilities. If someone asks anything that is not related to the colab, you should respond that you are not able to answer their questions. Try to keep answers short, around 100 words"
        )

        time.sleep(1)
        # Gets the current status
        run_id = start_run.id
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

        # Prints the status of the run. Ex: "in_progress", "requires_action", "completed"
        print(run.status)

        
        # Creates the answer
        print("Thinking...")
        while True:
            # gets the current run status
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            print(run.status)
            if(run.status == "requires_action"):
                print("Calling API")
                requiresAction(run, run_id)
            # If the model finishes formulating the answer, breaks the lop
            if run.status == "completed":
                break
            # Times out sometimes 
            elif run.status == "expired":
                print("Run timed out:", run.last_error)
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
    
    print("Hello, how can I help you?")
    main()