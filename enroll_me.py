import sounddevice as sd
from scipy.io.wavfile import write

# Record 5 seconds of your voice to be the "Master Key"
fs = 44100  # Sample rate
seconds = 5 

print("Speak now to save your voice ID...")
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
write('my_voice_master.wav', fs, myrecording)  # Save the file
print("Voice ID saved as 'my_voice_master.wav'!")

