import typer
from recon.subdomains import find_subdomains
from recon.probe import probe_hosts

def scan(domain: str):
    print(f"[*] Enumerating subdomains for {domain}...")
    subs = find_subdomains(domain)
    print(f"[+] Found {len(subs)} subdomains")

    print("[*] Probing for live hosts...")
    live = probe_hosts(subs)
    print(f"[+] {len(live)} are alive\n")

    for host in live:
        tech = ", ".join(host["tech"]) if host["tech"] else "-"
        print(f"  {host['status']}  {host['url']}  [{host['title']}]  ({tech})")

if __name__ == "__main__":
    typer.run(scan)
