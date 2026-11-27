"""Link checker. Checks outside links used on the site and in sources.json. Writes links_report.md when links look dead.
Government sites sometimes block bots, so a link is only reported after two tries."""
import json, os, re, ssl, time, urllib.request
ROOT = os.path.dirname(os.path.abspath(__file__))
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE


def ok(u):
    for _ in range(2):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (compatible; TCS-link-check)"}), timeout=25, context=ctx)
            if r.status < 400: return True
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 405, 429): return True   # blocks bots but the page exists
        except Exception: pass
        time.sleep(2)
    return False


def main():
    urls = {}
    for f in ("index.html", "review.html", "calendar.html", "digest.html"):
        p = os.path.join(ROOT, f)
        if os.path.exists(p):
            for u in re.findall(r'href="(https?://[^"#]+)"', open(p, encoding="utf-8").read()):
                if "tcs-avi.github.io" not in u and "fonts.g" not in u: urls[u] = "site link"
    try:
        for s in json.load(open(os.path.join(ROOT, "sources.json"), encoding="utf-8"))["sources"]:
            urls[s["u"]] = "watched: " + s["n"]
    except Exception: pass
    dead = [(u, w) for u, w in list(urls.items())[:150] if not ok(u)]
    out = os.path.join(ROOT, "links_report.md")
    if os.path.exists(out): os.remove(out)
    if dead:
        open(out, "w", encoding="utf-8").write("## Links that did not open\n\nThey may be down only for the checker. Open each once before changing anything.\n\n" +
                                                "\n".join(f"- {w}: {u}" for u, w in dead) + "\n")
    print(f"checked={min(len(urls),150)} dead={len(dead)}")


if __name__ == "__main__":
    main()
