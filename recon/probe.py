import subprocess

def probe_hosts(subdomains: list[str]) -> list[dict]:
    """Feed subdomains to httpx, get back only the live ones with details."""
    if not subdomains:
        return []

    result = subprocess.run(
        ["httpx-toolkit", "-silent", "-title", "-tech-detect", "-status-code", "-json"],
        input="\n".join(subdomains),
        capture_output=True, text=True, timeout=600
    )

    import json
    live = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        data = json.loads(line)
        live.append({
            "url": data.get("url", ""),
            "title": data.get("title", ""),
            "status": data.get("status_code", ""),
            "tech": data.get("tech", []),
        })
        
    return live
