# line 517: https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/b4257370e1d799f0b8b64be9bf2a34cad8b1a251/samples/python/console/speech_sample.py#L522

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

def speech_recognize_keyword_locally_from_microphone():
    model = speechsdk.KeywordRecognitionModel("./models/high_accepts.table")
    keyword = "Hey CoLab"
    keyword_recognizer = speechsdk.KeywordRecognizer()
    done = False

    def recognized_cb(evt):
        result = evt.result
        if result.reason == speechsdk.ResultReason.RecognizedKeyword:
            print("RECOGNIZED KEYWORD: {}".format(result.text))
            
        nonlocal done
        done = True

    def canceled_cb(evt):
        result = evt.result
        if result.reason == speechsdk.ResultReason.Canceled:
            print('CANCELED: {}'.format(result.cancellation_details.reason))

        nonlocal done
        done = True

    # Connect callbacks to the events fired by the keyword recognizer.
    keyword_recognizer.recognized.connect(recognized_cb)
    keyword_recognizer.canceled.connect(canceled_cb)

    # Start keyword recognition.
    result_future = keyword_recognizer.recognize_once_async(model)
    print('Say something starting with "{}" followed by whatever you want...'.format(keyword))
    try: 
        result = result_future.get()
    except: 
        print("Error with getting result")

    # Read result audio (incl. the keyword).
    if result.reason == speechsdk.ResultReason.RecognizedKeyword:
        print('This is result: "{}" '.format(result))           # print the metadata on result
        
        # put code for what to do once it's listening 
        talking = speech_recognizer.recognize_once()
        if talking.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(talking.text))

    # If active keyword recognition needs to be stopped before results, it can be done with
    stop_future = keyword_recognizer.stop_recognition_async()
    print('Stopping...')
    stopped = stop_future.get()
    print('Stopped: "{}" '.format(stopped))

def main(): 
    print("hello world")
    speech_recognize_keyword_locally_from_microphone()
    print("done")


if __name__ == '__main__':
    main()