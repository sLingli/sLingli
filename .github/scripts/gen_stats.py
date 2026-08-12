import json, os, urllib.request

TOKEN = os.environ["GH_TOKEN"]
USER = "sLingli"
HDRS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}

def api(url):
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req) as r:
        return json.load(r)

u = api(f"https://api.github.com/users/{USER}")
repos = api(f"https://api.github.com/users/{USER}/repos?per_page=100&type=all")
stars = sum(r["stargazers_count"] for r in repos)
forks = sum(r["forks_count"] for r in repos)

rows, y = "", 60
for name, val in [("Repos", u["public_repos"]), ("Stars", stars),
                  ("Forks", forks), ("Followers", u["followers"])]:
    rows += f'<text x="20" y="{y}" fill="#8b949e" font-size="14">{name}</text>'
    rows += f'<text x="280" y="{y}" fill="#6CABDD" font-size="16" font-weight="bold" text-anchor="end">{val}</text>'
    y += 32

h = y + 20
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="{h}" viewBox="0 0 400 {h}">
<rect width="400" height="{h}" rx="10" fill="#0D1117"/>
<text x="20" y="30" fill="#6CABDD" font-size="16" font-weight="bold">sLingli's GitHub Stats</text>
<line x1="20" y1="42" x2="380" y2="42" stroke="#30363D"/>
{rows}
</svg>'''

os.makedirs("assets", exist_ok=True)
with open("assets/stats.svg", "w") as f:
    f.write(svg)
print("stats.svg generated")
