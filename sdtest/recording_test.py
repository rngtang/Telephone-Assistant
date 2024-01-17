import sounddevice
from scipy.io.wavfile import write
sr = 44100
seconds = 5

print("Recording")
record_voice = sounddevice.rec(sr*seconds, samplerate=sr, channels=2)
sounddevice.wait()

write("test_audio.wav", sr, record_voice)
print("Finished")