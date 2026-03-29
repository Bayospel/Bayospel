import nmap
import dns.resolver

def scan_target(target):
    nm = nmap.PortScanner()
    print(f"Bayospel is scanning {target} for open ports...")
    
    # -sV: service version detection, -sC: default scripts
    nm.scan(target, arguments='-sV -sC')
    
    results = []
    for host in nm.all_hosts():
        results.append(f"Host: {host} ({nm[host].hostname()})")
        results.append(f"State: {nm[host].state()}")
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in ports:
                state = nm[host][proto][port]['state']
                service = nm[host][proto][port]['name']
                results.append(f"Port {port}/{proto} is {state} (Service: {service})")
    return "\n".join(results)

def get_dns_info(domain):
    print(f"Bayospel is looking up DNS for {domain}...")
    records = ['A', 'MX', 'NS', 'TXT']
    results = []
    for record in records:
        try:
            answers = dns.resolver.resolve(domain, record)
            for rdata in answers:
                results.append(f"{record} Record: {rdata}")
        except:
            continue
    return "\n".join(results)

