# Co-Lab Telephone Assistant
Welcome to the Co-Lab's Telephone Assistant! This project is meant to serve as a conversational question-answering bot to which any student can ask questions about the Co-Lab, such as its facilities, tools, workers, and upcoming classes. 

This project consists of two main parts:
1. Azure AI Speech: used for speech-to-text and text-to-speech interaction
2. Question-answering bot: used to generate answers to questions

To learn more about the creation/use process of these technologies, go down to "Part 1" and "Part 2" respectively (after Getting Started).

## Getting Started

### Activate the Virtual environment
In order for the project to work, it is necessary to activate the virtual environment. To do so, run the following command:
```
source /home/colabdev/Desktop/telephone-assistant/openai-env/bin/activate
```

### Testing Combined Project
To test the combined project that uses both Azure and the Bot together, first make sure a speaker is turned on and plugged into the Raspberry Pi. The microphone should already be attached to the Pi. When speaking to ask a question, make sure to hold up the Pi and talk directly into the microphone. 

Once both the speaker and microphone are ready, run the program using the following command:

```
python /home/colabdev/Desktop/telephone-assistant/embeddings/testing/stt_embeddings.py
```
You should now be able to verbally ask questions and recieve answers about anything related to the Co-Lab! Please note that as the current program is being run on a free trial of OpenAI, the number of questions you can ask at one time is limited. 

### Optional: Testing just AzureAI Speech
To test just the AzureAI Speech (speech-to-text and text-to-spech), make sure the microphone and speaker are both set up (as described above). Here, the Question Answering is implemented through AzureAI's Language service, not the Bot. As a result, the answers generated are not very flexible or complete, as described in "Part 1: Azure AI Speech".

To run the program, use the following command: 
```
python /home/colabdev/Desktop/telephone-assistant/assistant/working/ask.py
```

### Optional: Testing just the question-answering Bot
To test just the question-answering Bot using your terminal (text input), use this command: 
```
python /home/colabdev/Desktop/telephone-assistant/embeddings/testing/embeddings_terminal.py
```

### Optional: Testing the Project with Wake-up Word
Currently, this feature is still in development. It requires hardware (microphone and speaker) to be set up. 

To test the combined project (STT/TTS and question-answering Bot) additionally integrated with a wake-up word activation, use this command: 
```
python /home/colabdev/Desktop/telephone-assistant/assistant/working/wake_up.py
```
The wake-up word is "Hey Colab". Before saying this phrase, the robot will be "awake", but will not respond to questions. 

## Part 1: Azure AI Speech
The main functionalities of Azure AI Speech are its speech-to-text (STT) and Text-to-speech (TTS) features that the SDK provides. In this case, we are using STT to recognize what is the user asking and TTS for the assistant to verbally answer the question.

<!-- Additionally, we are also using the wake-up word function to have the telephone-assistant only start listening for questions once the wake-up word has been spoken. Currently, the wake-up word is set to "Hey Colab". -->

We originally planned to use Azure AI services for both STT/TTS and question answering. However, the capabilities of the Question Answering feature were not enough. It could only detect question intent and then pair word-for-word an answer to a question as written in whichever PDF we gave. As a result, we moved to using OpenAI Assistants for generating answers to questions. However, OpenAI assistants where not cost efficient and had high latency. 

After investigating other question-answering methods, we tried creating our own document-based question-answering bot using a vector database, OpenAI, and Langchain as our LLM application framework.

Documentation for the Speech SDK can be found here: https://azure.microsoft.com/en-us/products/ai-services/ai-speech/. 

## Part 2: Question-answering bot
As mentioned before, we are now using a custom-made document-based question-answering bot. To do this, we implement a vector-search to decrease the latency and increse the accuracy of answers. We are using OpenAI as our LLM, ChromDB as our vector database, and Langchain as the framework to build our bot.

By having our OpenAI 

The following diagram shows how our bot works:
![Program flowchart](./media/bot-diagram.png)

An introduction to LangChain and its complete possible functionalities can be found here: https://python.langchain.com/docs/get_started/introduction.  


## How It Works
The following chart represents how the Co-Lab assistant pipeline works. To answer questions, the question is converted into a vector. Then, it uses vector search to find a part of the text that has a close relationship with the questions. After that, it is passed to our LLM (OpenAI) to generate the answers. Finally, the answer is returned and the process is repeated.
![Program flowchart](./media/diagram.png)

Documentation for using OpenAI Embeddings can be found here: https://platform.openai.com/docs/guides/embeddings/use-cases.

### Update the Knowledge Base
Here comes the new stuff


## Known Bugs 
* There are no known bugs, for now...

<!-- Furthermore, sometimes the function calls seem to conflict with knowledge inside the knowledge base PDF. We tried to store some information about FTEs and student devs on the PDF, but the assistant seems to want to function call whenever asked about any person, and as a result will get confused when asked questions about FTEs and student dev expertise. This can cause it to fime out and/or fail to generate an answer.  -->
