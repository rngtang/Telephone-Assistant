from openai import OpenAI
import time
import os
import requests

import azure.cognitiveservices.speech as speechsdk

# STT configs
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('COLAB_SPEECH_KEY'), region=os.environ.get('COLAB_SPEECH_REGION'))
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
# TTS configs
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.speech_synthesis_voice_name='en-US-AvaNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# OpenAI configs
StudioUrl = 'https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/CoLab%20Studios/TEC'
StudentDevsUrl = 'https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/Colab%20Student%20Developer/TEC%20Office%20Hours'
assistant_id = os.environ.get("ASSISTANT_ID")
print(assistant_id)

# Creates a thread
client = OpenAI()
message_thread = client.beta.threads.create()
thread_id = message_thread.id

# Calls the API to get the current workers
def getInfo(url):
    response = requests.get(url)
    workers = ""

    if response.status_code == 200:
        data = response.json()
        for worker in data:
            workers = workers + ", " + worker["user_name"]
    return workers[2:]

# Submits the function output to the assistant
def requiresAction(run, run_id):
    tool_calls = run.required_action.submit_tool_outputs.tool_calls[0]
    # print(tool_calls)
    workers = getInfo(StudioUrl) if tool_calls.function.name == "get_current_worker" else getInfo(StudentDevsUrl)
    tool_outputs = []
    tool_outputs.append({"tool_call_id":tool_calls.id, "output": workers})
    # print(tool_outputs)

    run = client.beta.threads.runs.submit_tool_outputs(
        run_id=run_id,
        thread_id=thread_id,
        tool_outputs=tool_outputs
    )

def speech_recognize_keyword_locally_from_microphone():
    model = speechsdk.KeywordRecognitionModel("../../models/high_accepts.table")
    keyword = "Hey CoLab"
    keyword_recognizer = speechsdk.KeywordRecognizer()
    done = False

    def recognized_cb(evt):
        result = evt.result
        if result.reason == speechsdk.ResultReason.RecognizedKeyword:
            print("RECOGNIZED KEYWORD: {}".format(result.text))
        nonlocal done
        done = True

    keyword_recognizer.recognized.connect(recognized_cb)

    result_future = keyword_recognizer.recognize_once_async(model)
    print('Start by saying "{}"'.format(keyword))
    try: 
        result = result_future.get()
    except: 
        print("Error with getting result")

    if result.reason == speechsdk.ResultReason.RecognizedKeyword:
        # print('This is result: "{}" '.format(result))
        
        main()

    # If active keyword recognition needs to be stopped before results, it can be done with
    stop_future = keyword_recognizer.stop_recognition_async()
    print('Stopping...')
    stopped = stop_future.get()
    print('Stopped: "{}" '.format(stopped))

# Main function
def main():
    while True:
        print("Ask me anything: ")
        speech_synthesizer.speak_text_async("Ask me anything:").get()
        userSpeech = speech_recognizer.recognize_once_async().get()
        question = userSpeech.text

        # If the user doesn't say anything, breaks the loop
        if(question == ""):
            speech_synthesizer.speak_text_async("Nothing asked. Exiting.").get()
            print("Nothing asked. Exiting.")
            break

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
            instructions="You are the assistant of Duke's Innovation Colab. Your main role is to assist students in answering their questions. Most of the students come for help to use tools like 3d printers, laser cutters, or software. All the information that you need is the document provided, or in the links of functions for function calls. You should avoid answering questions that don't have a relationship with the Colab or its facilities. If someone asks anything that is not related to the colab, you should respond that you are not able to answer their questions. Try to keep answers short, around 100 words."
        )

        time.sleep(1)
        # Gets the current status
        run_id = start_run.id
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

        # Prints the status of the run. Ex: "in_progress", "requires_action", "completed"
        print(run.status)
        
        # Creates the answer
        speech_synthesizer.speak_text_async("Thinking...")
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
                speech_synthesizer.speak_text_async("Sorry, the run timed out.")
                print("Run timed out:", run.last_error)
                break
            # If for some reason it fails
            elif run.status == "failed":
                speech_synthesizer.speak_text_async("Sorry, the run failed.")
                speech_synthesizer.speak_text_async(run.last_error.code)
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
                        time.sleep(1)
                        response = content.text.value 
                        print(f'\n{role}: {response}')
                        # speech_synthesizer.speak_text_async(role).get()
                        speech_synthesizer.speak_text_async(response).get()
            except: 
                print("No return message")
        print("\n")

if __name__ == "__main__":
    assistant_files = client.beta.assistants.files.list(
        assistant_id=assistant_id
    )
    
    print("Waking up...")
    speech_synthesizer.speak_text_async("Waking up...")
    speech_recognize_keyword_locally_from_microphone() # <- calls on main from inside there