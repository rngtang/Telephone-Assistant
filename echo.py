import os
import azure.cognitiveservices.speech as speechsdk

# Configures the API key to use Azure
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('COLAB_SPEECH_KEY'), region=os.environ.get('COLAB_SPEECH_REGION'))
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

# Configure the audio
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.speech_synthesis_voice_name='en-US-AvaNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

print("Say something...")

# listens
result = speech_recognizer.recognize_once()

# converts to text and says it back
text = result.text
speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

try:

    # Checks result.
    # both stt and tts work
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        print("Speech synthesized for text [{}]".format(text))

    # stt error
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    # tts error
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
except:
    print("error")
# </code>