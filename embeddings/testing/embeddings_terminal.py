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
from langchain import hub
from PyPDF2 import PdfMerger, PdfReader

# Merges all documents together
filenames = ["../files/New Formatted K.pdf", "../files/Upcoming_Roots_Classes.pdf", "../files/Current_Studio_Workers.pdf", "../files/Current_Student_Devs.pdf"]
merger = PdfMerger()
for filename in filenames:
    merger.append(PdfReader(open(filename, 'rb')))
merger.write("All_Info.pdf")

# Loads document and splits it
loader = PyPDFLoader("../files/All_Info.pdf")
pages = loader.load()

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
prompt = hub.pull("rngtang/colab-bot")
model = RetrievalQA.from_chain_type(llm=client, retriever=vStore.as_retriever(), chain_type_kwargs={"prompt": prompt})
print("Everything set up")

# Question
while True:
    question = input("Ask me anything: ")
    response = model.invoke(question)
    print("\nBot: " + response['result'] + '\n')