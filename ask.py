# ask a question (stt) and have it respond with the answer
import os

# AI imports
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
# Speech imports
import azure.cognitiveservices.speech as speechsdk

# AI configs
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

# Ask for question and listen
print("Ask something about the Co-Lab.")
result = speech_recognizer.recognize_once()

# Checks result.
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))

    question = result.text

    client = QuestionAnsweringClient(endpoint, credential)
    with client:
        question=question # the question is what was just asked
        output = client.get_answers(
            question = question,
            project_name=knowledge_base_project,
            deployment_name=deployment
        )
    # print("Q: {}".format(question))
    print("A: {}".format(output.answers[0].answer))
    print("Confidence Score: {}".format(output.answers[0].confidence)) 

    # # tries to speak the answer back
    tts = output.answers[0].answer
    speech_synthesis_result = speech_synthesizer.speak_text_async(tts).get()
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(tts))

    # tts error
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

# stt error
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized: {}".format(result.no_match_details))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))


