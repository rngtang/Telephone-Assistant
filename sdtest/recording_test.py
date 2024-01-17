import sounddevice
from scipy.io.wavfile import write
import wavio as wv

sr = 44100
seconds = 5

print("Recording")
record_voice = sounddevice.rec(int(sr*seconds), samplerate=sr, channels=2, dtype='float32')
sounddevice.wait()

wv.write("test_audio.wav", record_voice, sr, sampwidth=2)
print("Finished")