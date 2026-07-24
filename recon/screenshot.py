import subprocess
from pathlib import Path

def _slug(url: str) -> str:
    """Reproduce gowitness's filename scheme: ://  and / become dashes."""
    return url.replace("://", "---").replace("/", "-")

def capture_screenshots(hosts: list[dict], outdir: str = "screenshots") -> list[dict]:
    Path(outdir).mkdir(exist_ok=True)
    for host in hosts:
        url = host["url"]
        try:
            subprocess.run(
                ["gowitness", "scan", "single",
                 "--url", url,
                 "--screenshot-path", outdir,
                 "--write-none",          # silence the "no writers" warning
                 "--timeout", "30"],
                capture_output=True, text=True, timeout=90
            )
            expected = Path(outdir) / f"{_slug(url)}.jpeg"
            host["screenshot"] = str(expected) if expected.exists() else None
        except Exception:
            host["screenshot"] = None
    return hosts
