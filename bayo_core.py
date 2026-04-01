import os, subprocess, json, time, requests, sys, shutil, ollama
import bayo_reader, bayo_vision, bayo_recon, bayo_exploit, bayo_infiltrate, bayo_brute, bayo_wifi, bayo_sms

# Load Settings
try:
    with open('config.json', 'r') as f: config = json.load(f)
except:
    config = {"bot_name": "Bayospel", "boss_name": "Big Boss"}

BOT_NAME = config.get("bot_name", "Bayospel")
BOSS_NAME = config.get("boss_name", "Big Boss")
authenticated = False
chat_history = []

def speak(text):
    print(f"{BOT_NAME}: {text}")
    os.system(f"termux-tts-speak -p 1.1 \"{text}\"")

def track_ip(ip):
    # Try 3 different servers to avoid "Not Responding" errors
    urls = [
        f"https://ipapi.co{ip}/json/",
        f"http://ip-api.com{ip}",
        f"https://ipinfo.io{ip}/json"
    ]
    for url in urls:
        try:
            r = requests.get(url, timeout=5).json()
            if r.get('city') or r.get('region'):
                return r
        except: continue
    return None

def main():
    global authenticated, chat_history
    os.system("termux-wake-lock")
    knowledge = bayo_reader.load_knowledge()
    system_p = f"You are {BOT_NAME}, a Cyber-Jarvis. Use this data: {knowledge[:500]}"

    while True:
        try:
            line = input(f"\n[ {BOT_NAME} - ONLINE ]: ")
            cmd = line.strip().lower()
            if not cmd: continue

            # --- 1. SECURITY ---
            if not authenticated:
                if "debam" in cmd or "i am here" in cmd:
                    authenticated = True
                    speak(f"Identity confirmed. Welcome back, {BOSS_NAME}")
                else: speak("Access Denied")
                continue

            # --- 2. MULTI-SERVER IP TRACKER ---
            if "locate ip" in cmd or "track" in cmd:
                ip = cmd.split()[-1]
                speak(f"Locating target {ip} now.")
                data = track_ip(ip)
                if data:
                    city, country = data.get('city', 'Unknown'), data.get('country_name', data.get('country', 'Unknown'))
                    speak(f"Target is in {city}, {country}.")
                    print(json.dumps(data, indent=2))
                else:
                    speak("All tracking servers are currently blocked. Try again later.")
                continue

            # --- 3. PHONE CONTROL ---
            elif "open" in cmd:
                app = cmd.split("open")[-1].strip()
                speak(f"Launching {app}")
                pkg = "com.zhiliaoapp.musically" if "tiktok" in app else "com.whatsapp" if "whatsapp" in app else "com.facebook.katana" if "facebook" in app else "com.google.android.gm" if "gmail" in app else app
                os.system(f"am start --user 0 -n {pkg}/.MainActivity || am start --user 0 {pkg}")
                continue
            elif "home" in cmd or "minimize" in cmd:
                os.system("input keyevent 3")
                continue
            elif "torch" in cmd:
                state = "on" if "on" in cmd else "off"
                os.system(f"termux-torch {state}")
                speak(f"Torch {state}")
                continue

            # --- 4. CYBER TOOLS ---
            elif "scan" in cmd or "recon" in cmd:
                target = cmd.split()[-1]
                speak(f"Recon initiated on {target}")
                print(bayo_recon.full_recon(target))
                continue
            elif "find admin" in cmd:
                target = cmd.split()[-1]
                panels = bayo_infiltrate.find_admin_panels(target)
                if panels:
                    print(f"Found: {panels}")
                    speak("Attempt crack?")
                    if input("y/n: ").lower() == 'y': print(bayo_brute.start_attack(panels))
                continue

            # --- 5. THE BRAIN ---
            else:
                try:
                    chat_history.append({"role": "user", "content": cmd})
                    res = ollama.chat(model="gemma2:2b", messages=[{"role":"system","content":system_p}] + chat_history[-3:])
                    reply = res["message"]["content"]
                    chat_history.append({"role": "assistant", "content": reply})
                    speak(reply)
                except: speak("Brain lag. Check Ollama.")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
