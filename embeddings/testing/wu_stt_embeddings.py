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

# Azure Language STT configs
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('COLAB_SPEECH_KEY'), region=os.environ.get('COLAB_SPEECH_REGION'))
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
# Azure Language TTS configs
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.speech_synthesis_voice_name='en-US-AvaNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# Recognizes wake-up word: "Hey CoLab"
def speech_recognize_keyword_locally_from_microphone():

    # Uses Azure model to initialize wake-up word
    keyword_model = speechsdk.KeywordRecognitionModel("/home/colabdev/Desktop/telephone-assistant/models/high_accepts.table")
    keyword = "Hey CoLab"
    # Set up keyword recognizer object
    keyword_recognizer = speechsdk.KeywordRecognizer()
    done = False

    # Event if recognized keyword
    def recognized_cb(evt):
        result = evt.result
        if result.reason == speechsdk.ResultReason.RecognizedKeyword:
            print("RECOGNIZED KEYWORD: {}".format(result.text))
        nonlocal done
        done = True

    # Connects model to recognizer
    keyword_recognizer.recognized.connect(recognized_cb)
    result_future = keyword_recognizer.recognize_once_async(keyword_model)

    print('Start by saying "{}"'.format(keyword))
    try: 
        result = result_future.get()
    except: 
        print("Error with getting result")

    # If the word is recognized, then call main (QA loop)
    if result.reason == speechsdk.ResultReason.RecognizedKeyword:
        main()

    # If active keyword recognition needs to be exitted before results
    stop_future = keyword_recognizer.stop_recognition_async()
    print('Stopping...')
    stopped = stop_future.get()
    print('Stopped: "{}" '.format(stopped))


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

# Sets up the Bot
def bot_setup(doc_text):

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

    speech_synthesizer.speak_text_async("Model built")
    print("Model built")
    return model

# Asks and answers the questions
def main():
    while True:
        # Asks for a question
        print("Ask me anything: ")
        speech_synthesizer.speak_text_async("Ask me anything:").get()
        userSpeech = speech_recognizer.recognize_once()
        question = userSpeech.text
        print("\nUser: " + question + '\n')

        # If the user doesn't say anything, breaks the loop
        if(question == ""):
            speech_synthesizer.speak_text_async("Nothing asked. Exiting.").get()
            print("Nothing asked. Exiting.")
            break
        
        # Generates the answer
        print("Thinking...")
        speech_synthesizer.speak_text_async("Thinking...").get()
        response = model.invoke(question)

        # Returns the answer
        print("\nBot: " + response['result'] + '\n')
        speech_synthesizer.speak_text_async(response['result']).get()


if __name__ == "__main__":

    # Parse doc and set-up model
    doc_text = parse_doc() 
    model = bot_setup(doc_text)

    # Wait for wake-up word. Calls on main (QA loop) if wake-up word is used
    speech_recognize_keyword_locally_from_microphone() 

