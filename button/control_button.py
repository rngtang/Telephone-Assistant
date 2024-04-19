# This file test the question-answering bot implementing a button to start asking questions to the bot. 
# This file does not implements the STT and TTS features

import time
import RPi.GPIO as GPIO
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
import azure.cognitiveservices.speech as speechsdk

# Initializes the button
button_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def parse_doc():
    print("Loading information...")

    # Loads document and splits it
    loader = PyPDFLoader("../embeddings/files/All_Info.pdf")
    pages = loader.load()

    # Splits the document into smaller chunks
    char_text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    doc_texts = char_text_splitter.split_documents(pages)

    return doc_texts

# Sets up up the Bot
def get_answer(doc_text):

    print("Building model...")

    # OpenAI to use embeddings and creates the client
    openAI_embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
    client = OpenAI(openai_api_key=os.environ['OPENAI_API_KEY'], temperature=0)

    # Creates to store the vectors
    vStore = Chroma.from_documents(doc_text, openAI_embeddings)

    # Gets prompt and retrieves model
    prompt = hub.pull("rngtang/colab-bot")
    model = RetrievalQA.from_chain_type(llm=client, 
                                        retriever=vStore.as_retriever(), 
                                        chain_type_kwargs={"prompt": prompt, 
                                                           "memory": ConversationBufferMemory(input_key="question", memory_key="context")
                                        })
    print("Model built")
    return model

# Asks and answers the questions
def main():

    # second_state = 0
    # Waits until you press the button
    print("Press button when ready.")

    while True:
        button_state = GPIO.input(button_pin)
        if button_state == False:
            # print(button_state)
            print('Button pressed, continuing...')

            break
        time.sleep(0.1)
    
    while True:
        # Asks for a question
        time.sleep(1)

        second_state =  GPIO.input(button_pin)

        question = input("Ask me anything: " + '\n')
    
        if second_state == False:
            print("Exiting.")
            break

        print("\nUser: " + question + '\n')
        
        # Generates the answer
        print("Thinking...")
        response = model.invoke(question)

        # Returns the answer
        print("\nBot: " + response['result'] + '\n')


if __name__ == "__main__":
    # Initializes the vectors and LLM
    doc_text = parse_doc() 
    model = get_answer(doc_text)
    
    # Calls main
    main()


