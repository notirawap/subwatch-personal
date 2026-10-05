"""Reddit official API smoke test (read-only, app-only OAuth). Reads credentials from .env.reddit next to this file.
Run: python subwatch_readonly.py"""
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

HERE = Path(__file__).parent
for line in (HERE / ".env.reddit").read_text().splitlines():
    if "=" in line and not line.lstrip().startswith("#"):
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

UA = os.environ["REDDIT_USER_AGENT"]
SUBS = ["pennystocks", "Shortsqueeze", "10xPennyStocks", "100xpennystock", "marketrodeo", "TheRaceTo10Million"]

# app-only ("userless") token: read-only public data, no Reddit password stored anywhere
tok = requests.post("https://www.reddit.com/api/v1/access_token",
                    auth=(os.environ["REDDIT_CLIENT_ID"], os.environ["REDDIT_CLIENT_SECRET"]),
                    data={"grant_type": "client_credentials"}, headers={"User-Agent": UA}, timeout=20)
tok.raise_for_status()
H = {"Authorization": f"bearer {tok.json()['access_token']}", "User-Agent": UA}
print("token OK, expires in", tok.json().get("expires_in"), "s")


def get(path, **params):
    r = requests.get("https://oauth.reddit.com" + path, headers=H, params={"raw_json": 1, **params}, timeout=20)
    print(f"  {r.status_code} {path}  ratelimit remaining={r.headers.get('x-ratelimit-remaining')} "
          f"reset={r.headers.get('x-ratelimit-reset')}s")
    r.raise_for_status()
    return r.json()


authors = set()
for sub in SUBS:
    posts = [c["data"] for c in get(f"/r/{sub}/new", limit=100)["data"]["children"]]
    comments = [c["data"] for c in get(f"/r/{sub}/comments", limit=100)["data"]["children"]]
    def rate(items):
        if len(items) < 2:
            return 0
        span = (items[0]["created_utc"] - items[-1]["created_utc"]) / 86400
        return len(items) / span if span else 0
    print(f"r/{sub}: {len(posts)} posts (~{rate(posts):.0f}/day), {len(comments)} comments (~{rate(comments):.0f}/day)")
    authors.update(c["author"] for c in comments[:5] if c["author"] not in ("[deleted]", "AutoModerator"))
    time.sleep(1)

for a in list(authors)[:5]:
    d = get(f"/user/{a}/about")["data"]
    age = (time.time() - d["created_utc"]) / 86400
    print(f"u/{a}: account {age:.0f} days, karma link {d.get('link_karma')} / comment {d.get('comment_karma')}, "
          f"created {datetime.fromtimestamp(d['created_utc'], timezone.utc):%Y-%m-%d}")
    time.sleep(1)
