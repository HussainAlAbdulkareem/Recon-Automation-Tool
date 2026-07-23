import subprocess
from urllib.parse import urlparse

def scan_ports(hosts: list[dict]) -> list[dict]:
    """Port-scan each live host. Adds an 'ports' field to each."""
    for host in hosts:
        hostname = urlparse(host["url"]).hostname
        if not hostname:
            host["ports"] = []
            continue

        result = subprocess.run(
            ["nmap", "-T4", "--top-ports", "100", "-Pn", hostname],
            capture_output=True, text=True, timeout=300
        )

        open_ports = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if "/tcp" in line and "open" in line:
                parts = line.split()
                open_ports.append(parts[0] + " " + parts[2] if len(parts) > 2 else parts[0])
        host["ports"] = open_ports

    return hosts
