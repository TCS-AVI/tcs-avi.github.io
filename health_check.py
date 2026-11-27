"""Health and quality bot. Mode 'files' (every push): checks the repo files. Mode 'live' (weekly): checks the live site.
Exit code 1 and a report in health_report.md when something is wrong; the workflow opens a GitHub Issue."""
import json, os, re, sys, urllib.request
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://tcs-avi.github.io/"
bad = []

def rd(p):
    return open(os.path.join(ROOT, p), encoding="utf-8").read()

def files():
    for f in ("index.html", "sw.js", "version.json", "bank.js", "data.js", "manifest.webmanifest", "sitemap.xml"):
        if not os.path.exists(os.path.join(ROOT, f)) or os.path.getsize(os.path.join(ROOT, f)) < 50:
            bad.append(f"{f} is missing or empty")
    if bad: return
    sw = rd("sw.js")
    if "tcs-v" not in sw: bad.append("sw.js has no cache name")
    try: json.loads(rd("version.json")); json.loads(rd("manifest.webmanifest"))
    except Exception as e: bad.append(f"version.json/manifest invalid: {e}")
    for f in ("bank.js", "data.js"):
        t = rd(f)
        try: d = json.loads(t[t.index("{"):t.rindex("}") + 1])
        except Exception as e: bad.append(f"{f} is not valid data: {e}"); continue
        ms = d.get("mcqs", [])
        if len(ms) < (100 if f == "bank.js" else 1): bad.append(f"{f}: only {len(ms)} questions")
        ids = [m.get("id") for m in ms]
        if len(ids) != len(set(ids)): bad.append(f"{f}: duplicate question ids")
        n = 0
        for m in ms:
            o = m.get("options", [])
            if len(o) != 4 or len(set(map(str, o))) != 4 or not isinstance(m.get("answer"), int) or not 0 <= m["answer"] < len(o) or not str(m.get("q", "")).strip():
                n += 1
                if n <= 5: bad.append(f"{f}: broken question {m.get('id')}")
        if n > 5: bad.append(f"{f}: {n} broken questions in total")
    import gzip
    gz = len(gzip.compress(open(os.path.join(ROOT, "bank.js"), "rb").read(), 6))
    if gz > 1_200_000: bad.append(f"Speed budget: bank.js is {gz//1024} KB compressed (limit 1,200 KB). Slow phones will struggle. Time to split the bank.")
    if os.path.getsize(os.path.join(ROOT, "index.html")) > 700_000: bad.append("Speed budget: index.html is over 700 KB")
    ix = rd("index.html")
    if ix.count("<script") != ix.count("</script>"): bad.append("index.html: unbalanced script tags")
    v1 = re.search(r'var VER="([^"]+)"', ix); v2 = json.loads(rd("version.json"))
    cur = v2.get("version") or (v2.get("notes") or [{}])[0].get("v") if isinstance(v2, dict) else None
    if v1 and cur and v1.group(1) != str(cur): bad.append(f"version mismatch: index {v1.group(1)} vs version.json {cur}")

def live():
    def get(u):
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "TCS-health"}), timeout=30)
        return r.status, r.read().decode("utf-8", "replace")
    for p in ("", "bank.js", "data.js", "sw.js", "version.json", "manifest.webmanifest", "sitemap.xml", "share/post.html", "calendar.html", "digest.html", "hours.json"):
        try:
            s, t = get(SITE + p)
            if s != 200 or len(t) < 50: bad.append(f"{p or 'home'} returned {s}")
        except Exception as e: bad.append(f"{p or 'home'} failed: {e}")
    try:
        s, t = get(SITE + "data.js"); d = json.loads(t[t.index("{"):t.rindex("}") + 1])
        from datetime import datetime, timedelta, timezone
        ist = timezone(timedelta(hours=5, minutes=30)); today = datetime.now(ist).date()
        newest = max((m.get("date", "") for m in d.get("mcqs", [])), default="")
        if newest and (today - datetime.fromisoformat(newest).date()).days > 3:
            bad.append(f"Daily update looks stuck: newest question is {newest}")
    except Exception as e: bad.append(f"could not check freshness: {e}")
    try:
        sm = get(SITE + "sitemap.xml")[1]
        for u in re.findall(r"<loc>([^<]+)</loc>", sm)[:40]:
            try: get(u)
            except Exception as e: bad.append(f"sitemap page broken: {u}")
    except Exception: pass

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "files"
    (live if mode == "live" else files)()
    if bad:
        open(os.path.join(ROOT, "health_report.md"), "w").write("## Site check found problems\n\n" + "\n".join("- " + b for b in bad) + "\n")
        print("\n".join(bad)); sys.exit(1)
    print("all good")
