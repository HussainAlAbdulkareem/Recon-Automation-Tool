from jinja2 import Template
from datetime import datetime
from pathlib import Path

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Recon Report: {{ domain }}</title>
<style>
  body { font-family: 'Segoe UI', system-ui, sans-serif; background: #0d1117; color: #e6edf3; margin: 0; padding: 40px; }
  h1 { color: #3fb950; font-weight: 600; }
  .meta { color: #7d8590; margin-bottom: 30px; font-size: 14px; }
  table { width: 100%; border-collapse: collapse; }
  th { text-align: left; padding: 12px; background: #161b22; color: #3fb950; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }
  td { padding: 12px; border-bottom: 1px solid #21262d; vertical-align: top; font-size: 14px; }
  tr:hover { background: #161b22; }
  .url { color: #58a6ff; font-weight: 500; }
  .status-200 { color: #3fb950; }
  .status-301, .status-302 { color: #d29922; }
  .status-404, .status-403 { color: #f85149; }
  .tech { color: #7d8590; font-size: 12px; }
  .ports { font-family: monospace; color: #79c0ff; font-size: 13px; }
  img { display: block; width: 180px; border: 1px solid #21262d; border-radius: 6px; }
</style>
</head>
<body>
  <h1>Recon Report</h1>
  <div class="meta">
    Target: <strong>{{ domain }}</strong> &nbsp;&bull;&nbsp;
    {{ hosts|length }} live hosts &nbsp;&bull;&nbsp;
    Generated {{ timestamp }}
  </div>
  <table>
    <tr>
      <th>Screenshot</th>
      <th>URL</th>
      <th>Status</th>
      <th>Title</th>
      <th>Tech</th>
      <th>Open Ports</th>
    </tr>
    {% for h in hosts %}
    <tr>
      <td>
        {% if h.screenshot %}
          <img src="../{{ h.screenshot }}" alt="screenshot of {{ h.url }}">
        {% else %}
          <span class="tech">no capture</span>
        {% endif %}
      </td>
      <td class="url">{{ h.url }}</td>
      <td class="status-{{ h.status }}">{{ h.status }}</td>
      <td>{{ h.title }}</td>
      <td class="tech">{{ h.tech|join(', ') }}</td>
      <td class="ports">{{ h.ports|join('<br>')|safe if h.ports else '-' }}</td>
    </tr>
    {% endfor %}
  </table>
</body>
</html>"""


def build_report(domain: str, hosts: list[dict]) -> str:
    html = Template(TEMPLATE).render(
        domain=domain,
        hosts=hosts,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    out_dir = Path("reports")
    out_dir.mkdir(exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in "-." else "_" for c in domain)
    out_file = out_dir / f"{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    out_file.write_text(html)
    return str(out_file)
