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
# from PyPDF2 import PdfMerger, PdfReader

def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        print(f'Spent a total of {cb.total_tokens} tokens')

    return result

print("Loading information...")
# Loads document and splits it
loader = PyPDFLoader("../files/All_Info.pdf")
pages = loader.load()

print("Generating embeddings...")
# Splits the document into smaller chunks
char_text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
doc_texts = char_text_splitter.split_documents(pages)

# OpenAI to use embeddings and creates the client
openAI_embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY4'])
client = OpenAI(openai_api_key=os.environ['OPENAI_API_KEY4'], temperature=0.7)

# Creates to store the vectors
vStore = Chroma.from_documents(doc_texts, openAI_embeddings)
prompt = hub.pull("rngtang/colab-bot")
model = RetrievalQA.from_chain_type(llm=client, 
                                    retriever=vStore.as_retriever(), 
                                    chain_type_kwargs={
                                        "prompt": prompt,
                                        "verbose": True,
                                        "memory": ConversationBufferMemory(
                                            memory_key="context",
                                            input_key="question"),
                                    })
print("Everything set up")

# Question
while True:
    question = input("Ask me anything: ")
    response = model.invoke(question)
    print(count_tokens(model, question))
    print("\nBot: " + response['result'] + '\n')
