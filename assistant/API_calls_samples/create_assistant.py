from openai import OpenAI
import os
client = OpenAI()

# knowledge_base = client.files.create(
#     file=open("./formatted.pdf", "rb"),
#     purpose='assistants'
# )

# This is a test to create an assistant from python. 
# Don't run this program several times, otherwise you'll end up creating a bunch of assistants
# colab_assistant = client.beta.assistants.create(
#     instructions="You are the assistant of Duke's Innovation Colab. Your main role is to assist students in answering their questions. Most of the students come for help to use tools like 3d printers, laser cutters, or software. All the information that you need is the document provided. Anything else, you don't know. You should avoid answering questions that don't have a relationship with the Colab or its facilities. If someone asks anything that is not related to the colab, you should respond that you are not able to answer their questions",
#     name="Colab Assistant",
#     tools=[{"type": "retrieval"}],
#     model="gpt-3.5-turbo-0125",
# )
# print(colab_assistant)