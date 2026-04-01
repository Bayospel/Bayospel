import os, subprocess, re, datetime

def advanced_recon():
    # 1. Get Network Range
    ip_info = subprocess.getoutput("ifconfig wlan0")
    match = re.search(r'inet ([\d\.]+)', ip_info)
    if not match: return
    
    network_range = ".".join(match.group(1).split('.')[:-1]) + ".0/24"
    
    # 2. Run Nmap with OS/Service detection (Fast Scan)
    # -sn = Ping scan, --lookup-passwords = Get Hostnames
    print(f"[*] Bayospel is sniffing for hardware details on {network_range}...")
    scan_results = subprocess.getoutput(f"nmap -sn {network_range}")
    
    # 3. Extract IPs and Hostnames
    # This regex looks for: Nmap scan report for [Hostname] ([IP])
    devices = re.findall(r'Nmap scan report for (.*) \(([\d\.]+)\)', scan_results)
    
    # Fallback for devices without hostnames
    if not devices:
        ips_only = re.findall(r'Nmap scan report for ([\d\.]+)', scan_results)
        devices = [("Unknown_Device", ip) for ip in ips_only]

    # 4. Update the Ledger
    log_file = os.path.expanduser("~/Bayospel/.targets.log")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    new_found = 0
    with open(log_file, "a") as f:
        for name, ip in devices:
            # We don't log your own phone (usually .1 or your specific IP)
            if ip in match.group(1): continue 
            
            entry = f"[{timestamp}] TARGET: {ip} | NAME: {name}\n"
            f.write(entry)
            new_found += 1
    
    # 5. Notify the Boss
    if new_found > 0:
        alert = f"Recon Complete: {new_found} targets identified and logged."
        os.system(f'termux-toast -b black -c green "{alert}"')
        os.system(f'termux-tts-speak "Boss, I don catch {new_found} devices. Check the ledger."')

if __name__ == "__main__":
    advanced_recon()

