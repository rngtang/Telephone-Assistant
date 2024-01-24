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

# Keyword recognizer configs
model = speechsdk.KeywordRecognitionModel("./1f4d77be-1956-4c35-8530-221b1af24f4c.table")
keyword = "Hey CoLab"
        

def recognize_word():

    keyword_recognizer = speechsdk.KeywordRecognizer()

    def recognized(event):
        result = event.result

        if(result.reason == speechsdk.ResultReason.RecognizedKeyword):
            print("RECOGNIZED KEYWORD: {}".format(result.text))
            userSpeech = speech_recognizer.recognize_once()
            print(userSpeech)
        
    def canceled(event):
        result = event.result
        
        if (result.reason == speechsdk.ResultReason.Canceled):
            print('CANCELED: {}'.format(result.cancellation_details.reason))

    # Connects an event when the keyword is recongnized or when it is canceled
    keyword_recognizer.recognized.connect(recognized)
    keyword_recognizer.canceled.connect(canceled)

    # Start keyword recognition
    resultRecognize = keyword_recognizer.recognize_once_async(model)
    print('Say something starting with "{}" followed by whatever you want...'.format(keyword))
    result = resultRecognize.get()
    print(result)

    if (result.reason == speechsdk.ResultReason.RecognizedKeyword):
        time.sleep(5)
        speechsdk.AudioDataStream(result).detach_input()


def main():
    recognize_word()
    print("done")

if __name__ == '__main__':
    main()
