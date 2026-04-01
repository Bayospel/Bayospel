import speech_recognition as sr

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # These lines MUST be indented (4 spaces)
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        # Back to the same level as 'with'
        return recognizer.recognize_google(audio).lower()
    except Exception:
        return ""
