import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chains import VectorDBQA
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAI

# Loads document and splits it
loader = PyPDFLoader("./../../assistant/media/New Formatted K.pdf")
pages = loader.load_and_split()

# print(len(pages))
# print(pages[0].page_content)

# Splits the document into smaller chunks
char_text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
doc_texts = char_text_splitter.split_documents(pages)

# OpenAI to use embeddings and creates the client
openAI_embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY4'])
client = OpenAI(openai_api_key=os.environ['OPENAI_API_KEY4'])

# Creates to store the vectors
vStore = Chroma.from_documents(doc_texts, openAI_embeddings)
model = RetrievalQA.from_chain_type(llm=client, retriever=vStore.as_retriever())
print("Everything set up")

# Question
while True:
    question = input("Ask me anything: ")
    response = model.invoke(question)
    print("\nBot: " + response['result'] + '\n')