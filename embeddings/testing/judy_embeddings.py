# make periodic API calls to real-time data and store results in .txt -> PERIODIC_API.py
# combine all .txt and .pdfs together, just shove in filenames
# use embeddings

# need to ask zhichen about being re-added to gpt4

# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
import os
from langchain_openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY4"),) #To use the GPT4 model

from PyPDF2 import PdfMerger, PdfReader
filenames = ["../media/New Formatted K.pdf", "./Upcoming_Roots_Classes.pdf", "./Current_Studio_Workers.pdf", "./Current_Student_Devs.pdf"]
merger = PdfMerger()
for filename in filenames:
    merger.append(PdfReader(open(filename, 'rb')))

from langchain_community.document_loaders import PyPDFLoader
merger.write("All_Info.pdf")
loader = PyPDFLoader("All_Info.pdf")
pages = loader.load()

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

from langchain.chains import RetrievalQA
qa_chain = RetrievalQA.from_chain_type(llm=client, retriever=vStore.as_retriever(), chain_type_kwargs={"prompt": prompt})


# Question
question = "What can I do at the Colab?"
result = qa_chain.invoke({"query": question})
result["result"]
print(result)



