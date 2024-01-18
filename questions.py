# I'm trying to crete a script that recognizes a wake up word

import os
import azure.cognitiveservices.speech as speechsdk

# Settings
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('COLAB_SPEECH_KEY'), region=os.environ.get('COLAB_SPEECH_REGION'))
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

print("Ask me a question")

# Result
result = speech_recognizer.recognize_once()
print(result)
