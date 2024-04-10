import time
import os
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

# Initializes the button
button_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initializes LED
red_pin = 18
yellow_pin = 27
green_pin = 22
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(yellow_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)

# Sets all leds off
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
    print("Model built.")
    return model

# Asks and answers the questions
def main():
    # Waits until you press the button
    GPIO.output(red_pin, GPIO.HIGH)
    print("Press button when ready.")

    while True:
        button_state = GPIO.input(button_pin)
        if button_state == False:
            # print(button_state)
            print('Button pressed!')

            break
        time.sleep(0.1)
    GPIO.output(red_pin ,GPIO.LOW)

    
    while True:
        # Asks for a question
        
        counter = 0
        print("Hold button to exit.")

        GPIO.output(green_pin, GPIO.HIGH)
        GPIO.output(yellow_pin, GPIO.LOW)
        # print("Ask me anything: " + '\n')

        time.sleep(3)

        if GPIO.input(button_pin) == 0: # if button is held
            counter += 1
            time.sleep(0.2)
            if counter == 1 and GPIO.input(button_pin) == 0:
                GPIO.cleanup() # turn all LEDs off 
                print("Leaving...")
                break 
        
        question = input("Ask me anything: " + '\n')
        # question = input()

        print("\nUser: " + question + '\n')
        
        # Generates the answer
        GPIO.output(green_pin, GPIO.LOW)
        GPIO.output(yellow_pin, GPIO.HIGH)
        print("Thinking...")
        response = model.invoke(question)

        # Returns the answer
        print("\nBot: " + response['result'] + '\n')


if __name__ == "__main__":
    # Initializes the vectors and LLM
    doc_text = parse_doc() 
    model = get_answer(doc_text)
    
    # Calls main
    try:
        main()
    
    except KeyboardInterrupt:
        GPIO.cleanup() 


