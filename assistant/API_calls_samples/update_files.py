from openai import OpenAI
import os
client = OpenAI()

assistant_id = os.environ.get("ASSISTANT_ID")

assistant_files = client.beta.assistants.files.list(
  assistant_id=assistant_id
)

file_to_delete = []
for file in assistant_files:
    file_to_delete = file.id

# delete old 
if file_to_delete != []: 
    deleted_assistant_file = client.beta.assistants.files.delete(
        assistant_id=assistant_id,
        file_id=file_to_delete
    )
    print("Delete status: ", deleted_assistant_file)

# create new
new_file = client.files.create(
    file=open("../../media/formattedK.pdf", "rb"),
    purpose='assistants'
)
# print(new_file)

new_file_id = new_file.id

# add new to assistant
assistant_file = client.beta.assistants.files.create(
  assistant_id=assistant_id,
  file_id=new_file_id
)
# print(assistant_file)
my_updated_assistant = client.beta.assistants.update(
  assistant_id,
  file_ids=[new_file_id]
)

print("Updated assistant:", my_updated_assistant)
