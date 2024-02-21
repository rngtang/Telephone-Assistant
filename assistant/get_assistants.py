from openai import OpenAI
import os
import time
import json
import re
client = OpenAI()

OPEN_API_KEY = os.environ.get('OPENAI_API_KEY')

my_assistants = client.beta.assistants.list(
    order="desc",
    limit="20",
)

print(my_assistants.data)