"""Exam notification watcher. Run by GitHub Actions. Fetches each page in sources.json, finds links whose text looks like a
notification, and reports ones not seen before. First sight of a site is a silent baseline. No AI, standard library only.
Writes watch/state.json (memory) and watch/report.md (only when something new was found; the workflow turns it into a GitHub Issue)."""
import hashlib, json, os, re, sys, time, urllib.request, ssl
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from urllib.parse import urljoin

ROOT = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(ROOT, "watch", "state.json")
REPORT = os.path.join(ROOT, "watch", "report.md")
KEY = re.compile(r"(notif|recruit|vacanc|advert|admission|admit card|answer key|result|apply|application|walk-?in|"
                 r"exam|date sheet|datesheet|syllabus|corrigendum|schedule|merit|counsell?ing|cutoff|cut-off|"
                 r"interview|selection|registration|extension|extended|posts?\b|engagement)", re.I)
SKIP = re.compile(r"^(home|about|contact|login|sitemap|skip|screen reader|hindi|english|back|top|more|read more|click here|download|view|pdf)$", re.I)
URGENT = re.compile(r"(admit card|result|answer key|last date|extended|extension|corrigendum|walk-?in|date sheet|datesheet|cut-?off|merit list)", re.I)
KEEP_LINKS = 250       # per site
FAIL_LIMIT = 3         # consecutive failures before we report a broken source


class P(HTMLParser):
    def __init__(s, base):
        super().__init__(); s.base = base; s.out = []; s.h = None; s.t = []
    def handle_starttag(s, tag, a):
        if tag == "a":
            s.h = dict(a).get("href"); s.t = []
    def handle_data(s, d):
        if s.h is not None: s.t.append(d)
    def handle_endtag(s, tag):
        if tag == "a" and s.h is not None:
            txt = re.sub(r"\s+", " ", "".join(s.t)).strip()
            if 6 <= len(txt) <= 220 and not SKIP.match(txt) and not s.h.startswith(("#", "javascript", "mailto", "tel")):
                s.out.append((txt, urljoin(s.base, s.h)))
            s.h = None


def fetch(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE   # many government sites have broken certificates
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; TCS-notice-watcher; +https://tcs-avi.github.io)",
                                               "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
        raw = r.read(3_000_000)
        enc = r.headers.get_content_charset() or "utf-8"
    return raw.decode(enc, "replace")


MON = {m: i + 1 for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split())}


def find_dates(txt):
    """Dates written inside a notice title, as ISO strings. Titles often have none; that is fine."""
    out = []
    for d, m, y in re.findall(r"\b(\d{1,2})[./-](\d{1,2})[./-](20\d\d)\b", txt):
        out.append((int(y), int(m), int(d)))
    for d, m, y in re.findall(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]{3})[a-z]*,?\s+(20\d\d)\b", txt):
        if m.lower() in MON: out.append((int(y), MON[m.lower()], int(d)))
    res = []
    for y, m, d in out:
        try: res.append(datetime(y, m, d).date().isoformat())
        except ValueError: pass
    return sorted(set(res))


def lid(txt, href):
    return hashlib.md5((txt.lower() + "|" + href).encode()).hexdigest()[:12]


def main(sources_path=None, state_path=None):
    src = json.load(open(sources_path or os.path.join(ROOT, "sources.json"), encoding="utf-8"))["sources"]
    sp = state_path or STATE
    os.makedirs(os.path.dirname(sp), exist_ok=True)
    st = json.load(open(sp)) if os.path.exists(sp) else {}
    new_items, broken, baseline = [], [], 0
    for s in src:
        key = s["u"]; rec = st.get(key, {})
        try:
            html = fetch(s["u"]); p = P(s["u"]); p.feed(html)
            seen = {}
            for txt, href in p.out:
                seen.setdefault(lid(txt, href), (txt, href))
            relevant = {k: v for k, v in seen.items() if KEY.search(v[0])}
            if not rec.get("ids") and "ok" not in rec:   # first ever sight: silent baseline
                baseline += 1; fresh = []
            else:
                known = set(rec.get("ids", []))
                fresh = [(k, v) for k, v in relevant.items() if k not in known]
                if len(fresh) > 15: fresh = fresh[:15]
            for k, (t, h) in fresh:
                new_items.append((s["g"], s["n"], t, h))
            ids = list(dict.fromkeys(list(relevant) + rec.get("ids", [])))[:KEEP_LINKS]
            st[key] = {"n": s["n"], "ids": ids, "ok": int(time.time()), "fail": 0}
        except Exception as e:
            rec["fail"] = rec.get("fail", 0) + 1; rec["err"] = str(e)[:120]; rec["n"] = s["n"]
            st[key] = rec
            if rec["fail"] == FAIL_LIMIT: broken.append((s["n"], s["u"], rec["err"]))
        time.sleep(1)
    json.dump(st, open(sp, "w"), indent=0)
    ist = timezone(timedelta(hours=5, minutes=30)); today = datetime.now(ist).date().isoformat()
    nl = os.path.join(os.path.dirname(sp), "notices.json")
    log = json.load(open(nl, encoding="utf-8")) if os.path.exists(nl) else []
    for g, n, t, h in new_items:
        log.insert(0, {"d": today, "g": g, "n": n, "t": t, "h": h, "urgent": bool(URGENT.search(t)), "dates": find_dates(t)})
    json.dump(log[:600], open(nl, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    tp = os.path.join(os.path.dirname(sp), "title.txt")
    if os.path.exists(tp): os.remove(tp)
    ur = [x for x in new_items if URGENT.search(x[2])]
    rp = REPORT if not state_path else os.path.join(os.path.dirname(sp), "report.md")
    if os.path.exists(rp): os.remove(rp)
    if new_items or broken:
        L = []
        if new_items:
            L.append(f"## {len(new_items)} new notice link(s)\n")
            g = ""
            for grp, n, t, h in sorted(new_items):
                if grp != g: L.append(f"\n### {grp}"); g = grp
                L.append(f"- {'🔴 ' if URGENT.search(t) else ''}**{n}**: [{t}]({h})")
            L.append("\nCheck each on the official site before telling anyone.")
        if broken:
            L.append("\n## Sites that keep failing (fix the address in sources.json or ignore)\n")
            for n, u, e in broken: L.append(f"- {n}: {u} ({e})")
        open(rp, "w", encoding="utf-8").write("\n".join(L) + "\n")
        if ur: open(tp, "w").write("URGENT: " + "; ".join(sorted({x[1] for x in ur}))[:90] + " (" + today + ")")
    print(f"sites={len(src)} baseline={baseline} new={len(new_items)} newly_broken={len(broken)}")


if __name__ == "__main__":
    main()
