# ask a question (stt) and have it respond with the answer
import os
import time

# Azure imports
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

# Speech imports
import azure.cognitiveservices.speech as speechsdk

# QnA imports and config
endpoint = os.environ.get('COLAB_QNA_ENDPOINT')
credential = AzureKeyCredential(os.environ.get('COLAB_QNA_KEY'))
knowledge_base_project = os.environ.get('COLAB_QNA_KNOWLEDGE_BASE')
deployment = "test"

# STT configs
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('COLAB_SPEECH_KEY'), region=os.environ.get('COLAB_SPEECH_REGION'))
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

# TTS configs
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.speech_synthesis_voice_name='en-US-AvaNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# identifies if its a question

# Uses the text from the user to use stuff
def listen(userSpeech):
    if userSpeech.reason == speechsdk.ResultReason.RecognizedSpeech:
        question = userSpeech.text
    answer(question)
    
def answer(question):
    # sends the question
    client = QuestionAnsweringClient(endpoint, credential)
    with client:
        question=question # the question is what was just asked
        output = client.get_answers(
            question = question,
            project_name=knowledge_base_project,
            deployment_name=deployment
        )

    # returns the answer
    response(output.answers[0])

def response(answer):
    print("A: {}".format(answer.answer))
    print("Confidence Score: {}".format(answer.confidence)) 

    try:
        speech_synthesis_result = speech_synthesizer.speak_text_async(answer.answer).get()
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Finished!")
    except:
        print("Could not convert text to audio")


def main():

    # Initialization
    print("Ask something about the Co-Lab.")
    speech_synthesizer.speak_text_async("Ask something about the Co-Lab.")
    
    userSpeech = speech_recognizer.recognize_once()

    # if the user doesn't want to speak 
    if(userSpeech.text == ''):
        print("none")
        speech_synthesizer.speak_text("Sorry I could not understand you")
        return
    
    # Debug
    # answer("what is the colab?")

    while True:
        time.sleep(1)
        userSpeech = speech_recognizer.recognize_once()

        # if the user doesn't want to speak 
        if(userSpeech.text == ''):
            print("No speech detected.")
            return
        
        listen(userSpeech)
        
if __name__ == '__main__':
    main()


