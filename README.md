# to do
<!-- * Create/finish way to update the knowledge base -> have it well documented and easily usable for anyone  -->
* Update knowledge base pdf to include more information -> such as FTEs, map with where are rooms, tools, etc.
    * PROBLEM: can't seem to know who the FTEs are 
<!-- * Add way to exit the bot/finish 
    * auto times out for the complete one with speech -->
* Integrate with STT and TTS and wake-up word 
    * check out talk_functions.py, seems to do what it needs to kind of 
    * wake-up word : check out wake_up.py !!!! 
<!-- * Document everything 
    * this readme lol -->


# Co-Lab Telephone Assistant
Welcome to the Co-Lab's telephone assistant! This project is meant to serve as a conversational question-answering bot to which any student can ask questions about the Co-Lab, such as its facilities, tools, and workers. This project consists of two main parts:
1. Azure AI Speech: used for speech-to-text and text-to-speech interaction
2. OpenAI Assistants: used to generate answers to questions

To learn more about the creation/use process of these technologies, go down to "Part 1" and "Part 2" respectively (after Getting Started).

## Getting Started

### Activate the Virtual environment
In order for the project to work, it is important to activate the virtual environment. To do so, run the following command:
```
source /home/colabdev/Desktop/telephone-assistant/openai-env/bin/activate
```

### Testing Combined Project
To test the combined project that uses both Azure and OpenAI together, first make sure a speaker is turned on and plugged into the Raspberry Pi. The microphone should already be attached to the Pi. When speaking to ask a question, make sure to hold up the Pi and talk directly into the microphone. 

Once both the speaker and microphone are ready, run the program using the following command:

```
python /home/colabdev/Desktop/telephone-assistant/assistant/working/talk_functions.py
```
You should now be able to verbally ask questions and recieve answers about anything related to the Co-Lab! Please note that as the current program is being run on a free trial of OpenAI, the number of questions you can ask at one time is limited. 

### Optional: Testing just AzureAI Speech
To test just the AzureAI Speech (speech-to-text and text-to-spech), make sure the microphone and speaker are both set up (as described above). Here, the Question Answering is implemented through AzureAI's Language service, not OpenAI. As a result, the answers generated are not very flexible or complete, as described in "Part 1: Azure AI Speech".

To run the program, use the following command: 
```
python /home/colabdev/Desktop/telephone-assistant/assistant/working/ask_terminal.py
```

### Optional: Testing just the OpenAI Assistant
To test just the OpenAI Assistant using your terminal (text input), use this command: 
```
python /home/colabdev/Desktop/telephone-assistant/assistant/working/functions_test2.py
```

## Part 1: Azure AI Speech
The main functionality of Azure AI Speech to to be able to use the STT and TTS features that it provides. In this case, we are using STT to recognize what is the user asking and TTS for the assistant to answer the question.

We originally planned to use Azure AI services for both STT/TTS and question answering. However, the capabilities of the Question Answering feature were not enough. It could only detect question intent and then pair word-for-word an answer to a question as written in whichever PDF we gave. As a result, we moved to using OpenAI Assistants for generating answers to questions.

Documentation for the Speech SDK can be found here: https://azure.microsoft.com/en-us/products/ai-services/ai-speech/. 

## Part 2: OpenAI Assistants 
As mentioned before, we are using OpenAI's custom assistant features to generate a more human-like conversation with the user. To do this, we are using the Retrieval and Functions tools that allow us to not only provide the assistant with information from a document, but also some real-time data, such as the current available employees. Currently, the assistant has a PDF document that constains all the necessary information about the Co-Lab. Furthermore, it also has the ability to call an external API when real-time data is required.

## How It Works
The following chart represents how the Co-Lab assistant pipeline works. To answer questions, the assistant first creates a thread, to which messages (questions) can be appended and a run (answer generation) can start. Using the different status of an assistant's run object, the assistant can then know whether it needs to function call (request data from an API) to add real-time information to its answer, such as who is currently on shift. Only after the run status is completed does the answer get printed. This question-answering cycle should continue until the user asks no more questions, though the exiting process is still being worked on.
![Program flowchart](./assistant/media/Assistant%20flowchart.png)

Documentation for OpenAI Assistants can be found here: https://platform.openai.com/docs/assistants/overview. 

## How To Update the assistant
There are several ways to update the Assistant. For example, we can update the knowledge base or the settings.
### Update the Knowledge Base
To update the knowledge base, you can follow the `update_files.py` template, found in `/home/colabdev/Desktop/telephone-assistant/assistant/API_calls_samples`.

### Update the Assistant Settings
To update the Assistant settings, you can follow the `update_assistant.py` template, found in `/home/colabdev/Desktop/telephone-assistant/assistant/API_calls_samples`.

## Known Bugs 
Currently, there are a few errors with the assistant recognizing when a function call is necessary. For example, if you ask, "Where is Lily?", the assistant with sometimes think Lily is a person (rather than a typo for the library) and call the function. Additionally, the assistant sometimes gets confused between when to use one function versus the other (get_workers vs get_student_devs).

Furthermore, sometimes the function calls seem to conflict with knowledge inside the knowledge base PDF. We tried to store some information about FTEs and student devs on the PDF, but the assistant seems to want to function call whenever asked about any person, and as a result will get confused when asked questions about FTEs and student dev expertise. 