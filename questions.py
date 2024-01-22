# I'm trying to crete a script that recognizes a question

import os
import azure.cognitiveservices.speech as speechsdk

# Settings for speech recognition
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('COLAB_SPEECH_KEY'), region=os.environ.get('COLAB_SPEECH_REGION'))
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

question_words = ["what", "who", "where", "when", "why", "how", "whose", "which", "question", "?"]

print("Hello, how can I help you?")

# Gets listens
result = speech_recognizer.recognize_once().text
# checks if it is a question
q = any(i in result for i in question_words)
print(result)
print(q)
