import pvporcupine
from pvrecorder import PvRecorder
import whisper
import os
from personality import speak, greeting, suggest_action
from cyber_skills import scan_target, get_dns_info
from report_generator import generate_pdf_report
from phone_control import connect_phone, open_app
import librosa
import numpy as np

# --- 1. SECURITY: VOICE VERIFICATION ---
def verify_voice(audio_path):
    master_feat = np.mean(librosa.feature.mfcc(y=librosa.load('my_voice_master.wav')[0], n_mfcc=40).T, axis=0)
    test_feat = np.mean(librosa.feature.mfcc(y=librosa.load(audio_path)[0], n_mfcc=40).T, axis=0)
    return np.linalg.norm(master_feat - test_feat) < 30

# --- 2. INITIALIZE EARS & BRAIN ---
PICOVOICE_KEY = "YOUR_ACCESS_KEY_HERE" 
porcupine = pvporcupine.create(access_key=PICOVOICE_KEY, keyword_paths=["bayospel.ppn"])
recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
stt_model = whisper.load_model("base")

greeting() # Jarvis says hello

try:
    recorder.start()
    while True:
        pcm = recorder.read()
        if porcupine.process(pcm) >= 0:
            speak("I'm listening, Boss.")
            
            # Record the command (simulated 4-second window)
            # Note: In a real run, you'd save 'command.wav' here
            os.system("arecord -d 4 -f cd command.wav") 
            
            if verify_voice("command.wav"):
                result = stt_model.transcribe("command.wav")
                text = result.lower()
                print(f"You said: {text}")

                # --- LOGIC GATE ---
                if "scan" in text:
                    target = text.split()[-1]
                    speak(f"Initiating reconnaissance on {target}.")
                    ports = scan_target(target)
                    dns = get_dns_info(target)
                    report = generate_pdf_report(target, ports, dns)
                    speak(f"Scan complete. Report saved as {report}.")
                    suggest_action("scan")

                elif "whatsapp" in text:
                    speak("Opening WhatsApp on your mobile device.")
                    phone = connect_phone()
                    if phone: open_app(phone, "com.whatsapp")

                elif "lock" in text:
                    speak("Securing your laptop immediately.")
                    # (Insert your SSH Lock logic here)

            else:
                speak("Identity not recognized. Access denied.")

finally:
    recorder.stop()
    porcupine.delete()
