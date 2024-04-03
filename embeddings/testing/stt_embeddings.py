import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
# from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAI
from langchain import hub
import azure.cognitiveservices.speech as speechsdk

# STT configs
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('COLAB_SPEECH_KEY'), region=os.environ.get('COLAB_SPEECH_REGION'))
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
# TTS configs
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.speech_synthesis_voice_name='en-US-AvaNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

def parse_doc():
    print("Loading information...")
    speech_synthesizer.speak_text_async("Loading information...")

    # Loads document and splits it
    loader = PyPDFLoader("/home/colabdev/Desktop/telephone-assistant/embeddings/files/All_Info.pdf")
    pages = loader.load()

    # Splits the document into smaller chunks
    char_text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    doc_texts = char_text_splitter.split_documents(pages)

    return doc_texts

def get_answer(doc_text):
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

def main():
    while True:
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
        
        print("Thinking...")
        speech_synthesizer.speak_text_async("Thinking...").get()
        response = model.invoke(question)

        print("\nBot: " + response['result'] + '\n')
        speech_synthesizer.speak_text_async(response['result']).get()

if __name__ == "__main__":

    doc_text = parse_doc() 
    model = get_answer(doc_text)

    main()


