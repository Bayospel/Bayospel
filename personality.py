import pyttsx3
import random

engine = pyttsx3.init()

# --- JARVIS SETTINGS ---
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) # Usually the male 'English' voice
engine.setProperty('rate', 175)           # Speed of talking
engine.setProperty('volume', 1.0)         # Full volume

def speak(text):
    print(f"Bayospel: {text}")
    engine.say(text)
    engine.runAndWait()

def greeting():
    responses = [
        "At your service, Boss.",
        "Systems online. How can I assist you today?",
        "Ready and waiting. What's the plan for today?",
        "I'm here. Scanning for instructions."
    ]
    speak(random.choice(responses))

def suggest_action(command_type):
    # Jarvis-style suggestions
    if command_type == "scan":
        speak("Initial scans complete. Would you like me to generate a PDF report for your records?")
    elif command_type == "phone":
        speak("WhatsApp is now open. Shall I check your battery levels while I'm connected?")
