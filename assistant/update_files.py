from openai import OpenAI
import os
client = OpenAI()

assistant_id = os.environ.get("ASSISTANT_ID")

# then list all files associated with assistant
assistant_files = client.beta.assistants.files.list(
  assistant_id=assistant_id
)

for file in assistant_files:
    file_to_delete = file.id

# delete old 
deleted_assistant_file = client.beta.assistants.files.delete(
    assistant_id=assistant_id,
    file_id=file_to_delete
)
print("Delete status: ", deleted_assistant_file)

# create new file
new_file = client.files.create(
    file=open("../media/hello.pdf", "rb"),
    purpose='assistants'
)
# print(new_file)

new_file_id = new_file.id

# then add new to assistant
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

# How to add without overwriting: 
    #     // Upload the file
    #     const file = await openai.files.create({
    #       file: fs.createReadStream(fileName),
    #       purpose: "assistants",
    #     });

    #     // Retrieve existing file IDs from assistant.json to not overwrite
    #     let existingFileIds = assistantDetails.file_ids || [];

    #     // Update the assistant with the new file ID
    #     await openai.beta.assistants.update(assistantId, {
    #       file_ids: [...existingFileIds, file.id],
    #     });

    #     // Update local assistantDetails and save to assistant.json
    #     assistantDetails.file_ids = [...existingFileIds, file.id];
    #     await fsPromises.writeFile(
    #       assistantFilePath,
    #       JSON.stringify(assistantDetails, null, 2)
    #     );

    #     console.log("File uploaded and successfully added to assistant\n");
    #   }


