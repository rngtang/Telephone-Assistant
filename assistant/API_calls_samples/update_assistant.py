from openai import OpenAI
import os
client = OpenAI()

assistant_id = os.environ.get("ASSISTANT_ID")

my_updated_assistant = client.beta.assistants.update(
  assistant_id,
  instructions="You are the assistant of Duke's Innovation Colab. Your main role is to assist students in answering their questions. Most of the students come for help to use tools like 3d printers, laser cutters, or software. All the information that you need is the document provided. Anything else, you don't know. You should avoid answering questions that don't have a relationship with the Colab or its facilities and workers. If someone asks anything that is not related to the colab, you should respond that you are not able to answer their questions. Keep all answers short, at about 1-5 sentences.",
  name="Colab Assistant",
  tools=[{"type": "retrieval"}, 
         {"type": "function", "function": {
      "name": "get_current_worker", 
      "description": "When asked about 'who is available at the Colab?' or if a person requests help to use hardware tools, get the name of the current worker that is passed as an array. If the parameter passed is empty, respond with 'No worker is available right now'. Do not call on this function if asked about software or FTEs (Full Time Employees)."
      }},
        {"type": "function", "function": {
      "name": "get_current_student_devs", 
      "description": "When asked about 'which student developer is available at the Colab?' or if a person requests help with software, get the name of the current worker and expertise. If the parameter passed is empty, respond with 'No worker is available right now'. Do not call on this function if asked about hardware/tools or FTEs (Full Time Employees)."
      }},
        {"type": "function", "function": {
      "name": "get_root_classes", 
      "description": "When asked about root classes, like what root classes are coming, the next 5 root classes will be provided, so just respond with them"
      }}]
)

print(my_updated_assistant)
