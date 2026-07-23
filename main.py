import typer
from recon.subdomains import find_subdomains
from recon.probe import probe_hosts
from recon.portscan import scan_ports

def scan(domain: str):
    print(f"[*] Enumerating subdomains for {domain}...")
    subs = find_subdomains(domain)
    print(f"[+] Found {len(subs)} subdomains")

    print("[*] Probing for live hosts...")
    live = probe_hosts(subs)
    print(f"[+] {len(live)} are alive\n")
    
    print("[*] Port scanning live hosts...")
    live = scan_ports(live)

    for host in live:
        tech = ", ".join(host["tech"]) if host["tech"] else "-"
        ports = ", ".join(host["ports"]) if host["ports"] else "none"
        print(f"  {host['status']}  {host['url']}")
        print(f"       tech: {tech}")
        print(f"       ports: {ports}")

if __name__ == "__main__":
    typer.run(scan)
