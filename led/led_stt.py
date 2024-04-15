import os
import time
import select
import sys
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
import RPi.GPIO as GPIO

# STT configs
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('COLAB_SPEECH_KEY'), region=os.environ.get('COLAB_SPEECH_REGION'))
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
# TTS configs
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.speech_synthesis_voice_name='en-US-AvaNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

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

# Sets led on
GPIO.output(red_pin, GPIO.LOW)
GPIO.output(yellow_pin, GPIO.LOW)
GPIO.output(green_pin, GPIO.LOW)

# Loads and divides the text into smaller chunks
def parse_doc():
    print("Loading information...")
    speech_synthesizer.speak_text_async("Loading information...")

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
    speech_synthesizer.speak_text_async("Building model...")

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

    speech_synthesizer.speak_text_async("Model built.")
    print("Model built.")
    return model

# Asks and answers the questions
def main():
    while True:
        counter = 0

        # Waits until you press the button
        GPIO.output(red_pin, GPIO.HIGH)
        speech_synthesizer.speak_text_async("Press the button to ask a question.")
        print("Press the button to ask a question.")

        while True:
            button_state = GPIO.input(button_pin)
            if button_state == False:
                print('Button pressed, continuing...')
                break
        time.sleep(0.1)

        if GPIO.input(button_pin) == 0:  # exit if button is held
            counter += 1
            time.sleep(0.5)
            if counter == 1 and GPIO.input(button_pin) == 0:
                GPIO.cleanup() 
                print("Button held, leaving...")
                speech_synthesizer.speak_text_async("Button held, leaving...")
                break 

        while True:
            # Asks for a question
            print("Ask me anything: ")
            speech_synthesizer.speak_text_async("Ask me anything:").get()
            GPIO.output(red_pin ,GPIO.LOW)
            GPIO.output(yellow_pin ,GPIO.LOW)
            GPIO.output(green_pin, GPIO.HIGH)
            userSpeech = speech_recognizer.recognize_once()
            question = userSpeech.text

            print("\nUser: " + question + '\n')

            GPIO.output(green_pin, GPIO.LOW)
            # If the user doesn't say anything, breaks the loop
            if(question == ""):
                print("Nothing asked. Exiting.")
                speech_synthesizer.speak_text_async("Nothing asked. Exiting.").get()
                time.sleep(1)
                break
            
            # Generates the answer
            GPIO.output(yellow_pin, GPIO.HIGH)
            print("Thinking...")
            speech_synthesizer.speak_text_async("Thinking...").get()
            response = model.invoke(question)

            # Returns the answer
            print("\nBot: " + response['result'] + '\n')
            speech_synthesizer.speak_text_async(response['result']).get()

if __name__ == "__main__":
            
    GPIO.output(red_pin, GPIO.HIGH)
    speech_synthesizer.speak_text_async("Hello! Welcome to the Co-Lab Telephone Assistant.")
    print("Hello! Welcome to the Co-Lab Telephone Assistant.")

    time.sleep(0.5)

    # Initializes the vectors and LLM
    doc_text = parse_doc() 
    model = get_answer(doc_text)
    
    # Calls main
    main()