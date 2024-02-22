from openai import OpenAI
import os
client = OpenAI()

assistant_id = os.environ.get("ASSISTANT_ID")

# create new file
new_file = client.files.create(
    file=open("./formatted.pdf", "rb"),
    purpose='assistants'
)

new_file_id = new_file.id

# then add to assistant
assistant_file = client.beta.assistants.files.create(
  assistant_id=assistant_id,
  file_id=new_file_id
)

# then list all files associated with assistant
assistant_files = client.beta.assistants.files.list(
  assistant_id=assistant_id
)
print(assistant_files)

