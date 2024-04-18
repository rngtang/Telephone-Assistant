# This is the first test using embeddings.
# In this program, we are trying to test the embeddings and question answering by until taking one input

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
loader = PyPDFLoader("/embeddings/files/All_Info.pdf")
pages = loader.load_and_split()

# print(len(pages))
# print(pages[0].page_content)

# Splits it
char_text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
doc_texts = char_text_splitter.split_documents(pages)

# Gets OpenAI
openAI_embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])

# Creates to store the vectors
vStore = Chroma.from_documents(doc_texts, openAI_embeddings)
model = VectorDBQA.from_chain_type(llm=OpenAI(openai_api_key=os.environ['OPENAI_API_KEY']), chain_type="stuff", vectorstore=vStore)
# model = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=os.environ['OPENAI_API_KEY4']), chain_type="stuff", vectorstore=vStore)
print("Everything set up")

# Question
question = "what tools does the colab has?"
response = model.invoke(question)
print(response['result'])