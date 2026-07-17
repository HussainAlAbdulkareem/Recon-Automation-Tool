import subprocess

def find_subdomains(domain: str) -> list[str]:
    result = subprocess.run(
        ["subfinder", "-d", domain, "-silent"],
        capture_output=True, text=True, timeout=300
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]
