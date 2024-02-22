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

# import openai  
# import json  

# api_key = "API-KEY-HERE"  
# openai.api_key = api_key

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": "celsius"})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": "fahrenheit"})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": "celsius"})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})

def run_conversation():
    messages = [{
        "role": "user",
        "content": "What's the weather in Tokyo, San Francisco, and Paris. Provide the temps for Tokyo in celsius, San Francisco in fahrenheit, and Paris in celsius."
    }]
    
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g., San Francisco, CA"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"]
                        }
                    },
                    "required": ["location", "unit"]
                }
            }
        }
    ]
    
    # response = openai.chat.completions.create(
    #     model="gpt-4-1106-preview",
    #     messages=messages,
    #     tools=tools,
    #     tool_choice="auto"
    # )

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

    run_id = start_run.id

    run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    response_message = run_status.required_action.submit_tool_outputs.tool_calls[0].message
    tool_calls = response_message.tool_calls
    
    if tool_calls:
        available_functions = {
            "get_current_weather": get_current_weather,
        }  
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = globals().get(function_name)
            
            if function_to_call:
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                
                function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )
                messages.append({
                      "role": "assistant",
                      "content": str(response),
                })
                messages.append({
                      "tool_call_id": tool_call.id,
                      "role": "function",
                      "name": function_name,
                      "content": function_response,
                })
            else:
                print(f"No function found for the name {function_name}")
    else:
        print("No tool calls made by the model.")
    
    try: 
        function_run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=messages
        )
        
        run = wait_on_run(function_run, message_thread)
    except: 
        print("what even")
    # print(get_response(message_thread))

    # response = openai.chat.completions.create(
    #     model="gpt-4-1106-preview",
    #     messages=messages,
    #     tools=tools,
    #     tool_choice="none"
    # )
    messages.append({
        "role": "assistant",
        "content": str(messages),
    })
    
    print(messages)
    return json.dumps(messages, indent=2)

print(run_conversation())