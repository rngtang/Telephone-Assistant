# This program implements QnA bot with embeddings, the button, and three LEDs to indicate the status of the bot

import time
import os
import sys
import select
import RPi.GPIO as GPIO
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAI
from langchain import hub

# Initialize the button
button_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize LEDs
red_pin = 18
yellow_pin = 27
green_pin = 22
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(yellow_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)

# Start with all LEDs off
GPIO.output(red_pin, GPIO.LOW)
GPIO.output(yellow_pin, GPIO.LOW)
GPIO.output(green_pin, GPIO.LOW)

# Divides the file into smaller chunks
def parse_doc():
    print("Loading information...")

    # Loads document and splits it
    loader = PyPDFLoader("./embeddings/files/All_Info.pdf")
    pages = loader.load()

    # Splits the document into smaller chunks
    char_text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    doc_texts = char_text_splitter.split_documents(pages)

    return doc_texts

# Sets up the Bot
def get_answer(doc_text):

    print("Building model...")

    # Use OpenAI for embeddings and as the LLM
    openAI_embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
    client = OpenAI(openai_api_key=os.environ['OPENAI_API_KEY'], temperature=0)

    # Creates to store the vectors
    vStore = Chroma.from_documents(doc_text, openAI_embeddings)

    # LangChain framework: gets prompt (https://smith.langchain.com/hub/rngtang/colab-bot) and combines with LLM and embeddings to make model
    prompt = hub.pull("rngtang/colab-bot")
    model = RetrievalQA.from_chain_type(llm=client, 
                                        retriever=vStore.as_retriever(), 
                                        chain_type_kwargs={"prompt": prompt, 
                                                           "memory": ConversationBufferMemory(input_key="question", memory_key="context")
                                        })
    print("Model built.")
    return model

# Check asynchronously for either user input (continue) or button holding (exit)
def wait_input(): 
    counter = 0
    print("Ask me anything: ")

    # Green LED = bot "listening/waiting for input"
    GPIO.output(green_pin, GPIO.HIGH)
    GPIO.output(yellow_pin, GPIO.LOW)

    try:
        while True:
            # Use select and sys for asynch checking
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            
            # If user enters input, return input
            for r in rlist:
                if r == sys.stdin:
                    question = input()
                    return question

            # If button held, exit
            if GPIO.input(button_pin) == 0:  
                counter += 1
                time.sleep(0.5)
                if counter == 1 and GPIO.input(button_pin) == 0:
                    GPIO.cleanup() 
                    print("Button held. Leaving...")
                    return ""
    
    # Cleanup if forced exit (Ctrl+C)
    except KeyboardInterrupt:
        GPIO.cleanup()

# Loop where user asks and bot answers 
def main():
    try: 
        GPIO.output(red_pin, GPIO.HIGH)
        print("Press the button to ask a question.")

        # Waits until user presses the button
        while True:
            button_state = GPIO.input(button_pin)
            if button_state == False:
                print('Button pressed!')
                break
            time.sleep(0.1)

        GPIO.output(red_pin, GPIO.LOW)

        while True:
            # After button pressed, check for user input (continue) or button holding (exit)
            question = wait_input()
            
            # if no question is asked, it breaks the loop
            if question == "":
                break

            print("\nUser: " + question + '\n')
            
            # Generates the answer. Yellow LED = bot "responding"
            GPIO.output(green_pin, GPIO.LOW)
            GPIO.output(yellow_pin, GPIO.HIGH)
            print("Thinking...")
            response = model.invoke(question)

            # Returns the answer
            print("\nBot: " + response['result'] + '\n')

    # Cleanup if forced exit (Ctrl+C)
    except KeyboardInterrupt:
        print("Keyboard interrupt. Exiting.")
        GPIO.cleanup() 


if __name__ == "__main__":
    # Red LED = bot "setting up" or "waiting for button"
    print("Welcome to the Co-Lab Assistant!")
    GPIO.output(red_pin, GPIO.HIGH)

    # Initializes the vectors and LLM
    doc_text = parse_doc() 
    model = get_answer(doc_text)
    
    # Calls main (QA loop)
    main()


