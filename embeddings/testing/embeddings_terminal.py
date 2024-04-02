import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
# from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAI
from langchain import hub
from langchain_community.callbacks import get_openai_callback
# from langchain_community.document_loaders import TextLoader

def count_tokens():
    with get_openai_callback() as cb:
        print(f'Spent a total of {cb.total_tokens} tokens')

print("Loading information...")
loader = PyPDFLoader("../files/All_Info.pdf")
# loader = TextLoader("../files/info.txt")
pages = loader.load()

print("Generating embeddings...")
char_text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
doc_texts = char_text_splitter.split_documents(pages)

openAI_embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY4'])
client = OpenAI(openai_api_key=os.environ['OPENAI_API_KEY4'], temperature=0)

# only real change i made was adding labels ?? 
vStore = Chroma.from_documents(documents=doc_texts, embedding=openAI_embeddings)

# prompt = hub.pull("rlm/rag-prompt")
# prompt = hub.pull("rngtang/colab-bot")
prompt = hub.pull("judipettutti/telephone")

model = RetrievalQA.from_chain_type(llm=client, 
                                    retriever=vStore.as_retriever(), 
                                    chain_type_kwargs={
                                        "prompt": prompt,
                                        "verbose": True
                                        # "memory": ConversationBufferMemory(input_key="question", memory_key="context"),
                                    })
print("Everything set up")

# Question
while True:
    question = input("Ask me anything: ")
    response = model.invoke(question)
    count_tokens()
    print("\nBot: " + response["result"] + '\n')
