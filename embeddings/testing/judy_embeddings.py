# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
import os
from langchain_openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY4"),) #To use the GPT4 model

from langchain_community.document_loaders import PyPDFLoader
# merger.write("All_Info.pdf")
loader = PyPDFLoader("../files/All_Info.pdf")
pages = loader.load()

print("finished loading")

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
doc_texts = text_splitter.split_documents(pages)

from langchain_openai import OpenAIEmbeddings
openAI_embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY4'])

from langchain_community.vectorstores import Chroma
vStore = Chroma.from_documents(documents=doc_texts, embedding=openAI_embeddings)

# https://smith.langchain.com/hub/rlm/rag-prompt
from langchain import hub
prompt = hub.pull("rlm/rag-prompt")

print("Retrieving answer...")
from langchain.chains import RetrievalQA
qa_chain = RetrievalQA.from_chain_type(llm=client, retriever=vStore.as_retriever(), chain_type_kwargs={"prompt": prompt})

# Question
while True:
    question = input("Ask me anything: ")
    result = qa_chain.invoke({"query": question})
    # result["result"]
    print(result["result"])



