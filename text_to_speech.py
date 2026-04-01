# text_to_speech.py
import pyttsx3

def speak(text):
 engine = pyttsx3.init()
 engine.say(text)
 engine.runAndWait()

if __name__ == "__main__":
 speak("Hello, I am Bayospel.")

