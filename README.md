# Co-Lab Telephone Assistant
Welcome to the Co-Lab's Telephone Assistant! This project is meant to serve as a conversational question-answering bot to which any student can ask questions about the Co-Lab, such as its facilities, tools, workers, and upcoming classes. 

This project consists of two main parts:
1. Azure AI Speech: used for speech-to-text and text-to-speech interaction
2. OpenAI Assistants: used to generate answers to questions

To learn more about the creation/use process of these technologies, go down to "Part 1" and "Part 2" respectively (after Getting Started).

## Getting Started

### Activate the Virtual environment
In order for the project to work, it is necessary to activate the virtual environment. To do so, run the following command:
```
source /home/colabdev/Desktop/telephone-assistant/openai-env/bin/activate
```

### Testing Combined Project
To test the combined project that uses both Azure and OpenAI together, first make sure a speaker is turned on and plugged into the Raspberry Pi. The microphone should already be attached to the Pi. When speaking to ask a question, make sure to hold up the Pi and talk directly into the microphone. 

Once both the speaker and microphone are ready, run the program using the following command:

```
python /home/colabdev/Desktop/telephone-assistant/assistant/working/telephone.py
```
You should now be able to verbally ask questions and recieve answers about anything related to the Co-Lab! Please note that as the current program is being run on a free trial of OpenAI, the number of questions you can ask at one time is limited. 

### Optional: Testing just AzureAI Speech
To test just the AzureAI Speech (speech-to-text and text-to-spech), make sure the microphone and speaker are both set up (as described above). Here, the Question Answering is implemented through AzureAI's Language service, not OpenAI. As a result, the answers generated are not very flexible or complete, as described in "Part 1: Azure AI Speech".

To run the program, use the following command: 
```
python /home/colabdev/Desktop/telephone-assistant/assistant/working/ask.py
```

### Optional: Testing just the OpenAI Assistant
To test just the OpenAI Assistant using your terminal (text input), use this command: 
```
python /home/colabdev/Desktop/telephone-assistant/assistant/working/functions_test2.py
```

### Optional: Testing the Project with Wake-up Word
Currently, this feature is still in development. It requires hardware (microphone and speaker) to be set up. 

To test the combined project (STT/TTS and OpenAI Assistant) additionally integrated with a wake-up word activation, use this command: 
```
python /home/colabdev/Desktop/telephone-assistant/assistant/working/wake_up.py
```
The wake-up word is "Hey Colab". Before saying this phrase, the robot will be "awake", but will not respond to questions. 

## Part 1: Azure AI Speech
The main functionalities of Azure AI Speech are its speech-to-text (STT) and Text-to-speech (TTS) features that the SDK provides. In this case, we are using STT to recognize what is the user asking and TTS for the assistant to verbally answer the question.

Additionally, we are also using the wake-up word function to have the telephone-assistant only start listening for questions once the wake-up word has been spoken. Currently, the wake-up word is set to "Hey Colab".

We originally planned to use Azure AI services for both STT/TTS and question answering. However, the capabilities of the Question Answering feature were not enough. It could only detect question intent and then pair word-for-word an answer to a question as written in whichever PDF we gave. As a result, we moved to using OpenAI Assistants for generating answers to questions.

Documentation for the Speech SDK can be found here: https://azure.microsoft.com/en-us/products/ai-services/ai-speech/. 

## Part 2: OpenAI Assistants 
As mentioned before, we are using OpenAI's custom assistant features to generate a more human-like conversation with the user. To do this, we are using the Retrieval and Functions tools that allow us to not only provide the assistant with information from a document, but also some real-time data, such as the current available employees. 

Currently, the assistant has a PDF document that constains all the necessary information about the Co-Lab. Furthermore, it also has the ability to call an external API when real-time data is required. 

## How It Works
The following chart represents how the Co-Lab assistant pipeline works. To answer questions, the assistant first creates a thread, to which messages (questions) can be appended and a run (answer generation) can start. Using the different status of an assistant's run object, the assistant can then know whether it needs to function call (request data from an API) to add real-time information to its answer, such as who is currently on shift. Only after the run status is completed does the answer get printed. This question-answering cycle should continue until the user asks no more questions, though the exiting process is still being worked on.
![Program flowchart](./media/diagram-updated.png)

Documentation for OpenAI Assistants can be found here: https://platform.openai.com/docs/assistants/overview. 

## How To Update the assistant
There are several ways to update the Assistant. Two methods that we set up include updating the knowledge base or updating the Assistant's settings. 

### Update the Knowledge Base
To update the knowledge base by adding new files, you can follow the `update_files.py` template, found in `/home/colabdev/Desktop/telephone-assistant/assistant/API_calls_samples`.

### Update the Assistant Settings
To update the Assistant settings, such as chaging its description or changing its functions, you can follow the `update_assistant.py` template, found in `/home/colabdev/Desktop/telephone-assistant/assistant/API_calls_samples`.

## Known Bugs 
* Currently, there are a few errors with the assistant recognizing when a function call is necessary. For example, if you ask, "Where is Lily?", the assistant with sometimes think Lily is a person (rather than a typo for the library) and call the function. Additionally, the assistant sometimes gets confused between when to use one function versus the other (get_workers vs get_student_devs).
* Additionally, because we are using the model GPT-3.5-turbo-0125 (free), there is currently a limitation of 3 questions that can be asked before there is a 20 second cooldown. Trying to ask another question before the cooldown will result in the run failing. 

<!-- Furthermore, sometimes the function calls seem to conflict with knowledge inside the knowledge base PDF. We tried to store some information about FTEs and student devs on the PDF, but the assistant seems to want to function call whenever asked about any person, and as a result will get confused when asked questions about FTEs and student dev expertise. This can cause it to fime out and/or fail to generate an answer.  -->
