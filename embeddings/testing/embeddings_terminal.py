import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAI
from langchain import hub
from langchain_community.callbacks import get_openai_callback

# Function to count tokens used
def count_tokens():
    with get_openai_callback() as cb:
        print(f'Spent a total of {cb.total_tokens} tokens')

# Loads the file
print("Loading information...")
loader = PyPDFLoader("./embeddings/files/All_Info.pdf")
pages = loader.load()

# Splits the document
print("Generating embeddings...")
char_text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
doc_texts = char_text_splitter.split_documents(pages)

# Sets up OpenAI
openAI_embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
client = OpenAI(openai_api_key=os.environ['OPENAI_API_KEY'], temperature=0)

# Sets up the vector db
vStore = Chroma.from_documents(documents=doc_texts, embedding=openAI_embeddings)

# Sets up the prompt
prompt = hub.pull("rngtang/colab-bot")  # Generates longer answers. IDK if that's better or not
# prompt = hub.pull("judipettutti/telephone") # i accidently made this on our shared one oop: https://smith.langchain.com/hub/judipettutti/telephone/playground?organizationId=5ed40c29-8f7d-47af-ab9b-2c31f51d5ba3 

# Sets up the chain
model = RetrievalQA.from_chain_type(llm=client, 
                                    retriever=vStore.as_retriever(), 
                                    chain_type_kwargs={
                                        "prompt": prompt,
                                        "memory": ConversationBufferMemory(input_key="question", memory_key="context")
                                    })
print("Everything set up")

# Where it actually answers the question
while True:
    question = input("Ask me anything: ")
    response = model.invoke(question)
    count_tokens()
    print("\nBot: " + response["result"] + '\n')
