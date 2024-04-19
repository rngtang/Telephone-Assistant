# This file is just to test one single question using embeddings
# Essentially same as embeddings.py, just with <invoke> instead of <run> and <RetrievalQA> instead of <VectorDBQA>
# https://smith.langchain.com/hub/rlm/rag-prompt

import os
from langchain import hub
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAI

from langchain_openai import ChatOpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY4"),) #To use the GPT4 model
# Does this key do anything ? it's still gpt-3.5
print(client)
print("HELLO WORLD")

# Loads document and splits it
loader = PyPDFLoader("../media/New Formatted K.pdf")
pages = loader.load()

# Splits it
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
doc_texts = text_splitter.split_documents(pages)

# Makes the embedding
openAI_embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY4'])

# Creates to store the vectors
vStore = Chroma.from_documents(documents=doc_texts, embedding=openAI_embeddings)

# RAG prompt
prompt = hub.pull("rlm/rag-prompt")
# https://smith.langchain.com/hub/rlm/rag-prompt
print("SET UP DONE")

#Retrieval QA
qa_chain = RetrievalQA.from_chain_type(llm=client, retriever=vStore.as_retriever(), chain_type_kwargs={"prompt": prompt})

# Question
question = "Who is currently on shift?"
result = qa_chain.invoke({"query": question})
result["result"]
print(result)
