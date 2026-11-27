"""Builds calendar.html (upcoming dates) and digest.html (this week). Reads watch/notices.json, exams.json, data.js.
Standard library only. Safe to run any time; it never touches the question banks."""
import json, os, html
from datetime import datetime, timedelta, timezone
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://tcs-avi.github.io"
IST = timezone(timedelta(hours=5, minutes=30))
E = html.escape


def load(p, default):
    try: return json.load(open(os.path.join(ROOT, p), encoding="utf-8"))
    except Exception: return default


CSS = """<style>body{margin:0;font:17px/1.6 Georgia,serif;background:#faf7ef;color:#1d1f27}main{max-width:44rem;margin:0 auto;padding:20px 16px 48px}
h1{font-size:1.6rem;line-height:1.25}h2{font-size:1.2rem;margin-top:1.8em}a{color:#1d3b78}ul{padding-left:1.1em}li{margin:.5em 0}
.m{color:#5b5f6b;font-size:.9rem}.u{font-weight:700;color:#8a1c1c}.n{background:#fff;border:1px solid #d8d3c3;padding:10px 14px;border-radius:8px;font-size:.95rem}
@media(prefers-color-scheme:dark){body{background:#14161d;color:#ece8da}a{color:#a9bff5}.n{background:#1d2029;border-color:#33374a}.m{color:#a3a79f}.u{color:#ff9d9d}}</style>"""


def page(title, desc, body, path):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | The Computer Services</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{SITE}/{path}">{CSS}</head>
<body><main><p><a href="/">Back to practice</a></p>{body}
<p class="n">Compiled automatically from official websites. It can be late or wrong. Always confirm dates and rules on the official site before you apply.</p></main></body></html>"""


def build():
    now = datetime.now(IST).date()
    notices = load("watch/notices.json", [])
    exams = load("exams.json", {}).get("exams", [])
    rows = []
    for e in exams:
        rows.append((e.get("date", ""), e.get("exam", ""), e.get("note", ""), e.get("link", ""), True))
    for n in notices:
        for d in n.get("dates", []):
            rows.append((d, n["t"], n["n"], n["h"], False))
    up = sorted({r for r in rows if r[0] >= now.isoformat()})
    b = ["<h1>Exam dates and last dates</h1><p class='m'>Updated " + now.strftime("%d %B %Y") + "</p>"]
    if up:
        b.append("<ul>")
        for d, t, note, link, mine in up:
            dd = datetime.fromisoformat(d).date(); left = (dd - now).days
            tag = f" <span class='u'>{left} day{'s' if left != 1 else ''} left</span>" if left <= 7 else f" <span class='m'>in {left} days</span>"
            a = f"<a href='{E(link)}' rel='noopener'>{E(t)}</a>" if link else E(t)
            b.append(f"<li><b>{dd.strftime('%d %b %Y')}</b>{tag}<br>{a}<br><span class='m'>{E(note)}</span></li>")
        b.append("</ul>")
    else:
        b.append("<p>No upcoming dates found yet. New ones appear here as notices are found.</p>")
    cal = page("Exam calendar and last dates", "Upcoming exam dates and application last dates for J&K and central government exams.", "".join(b), "calendar.html")
    open(os.path.join(ROOT, "calendar.html"), "w", encoding="utf-8").write(cal)
    wk = (now - timedelta(days=7)).isoformat()
    recent = [n for n in notices if n["d"] >= wk]
    d = ["<h1>This week</h1><p class='m'>Week ending " + now.strftime("%d %B %Y") + "</p><h2>New notices found</h2>"]
    if recent:
        cur = ""
        for n in recent:
            if n["g"] != cur: d.append(f"</ul><h3>{E(n['g'])}</h3><ul>" if cur else f"<h3>{E(n['g'])}</h3><ul>"); cur = n["g"]
            d.append(f"<li>{'<span class=u>Urgent</span> ' if n.get('urgent') else ''}<b>{E(n['n'])}</b>: <a href='{E(n['h'])}' rel='noopener'>{E(n['t'])}</a></li>")
        d.append("</ul>")
    else:
        d.append("<p>Nothing new this week.</p>")
    d.append("<h2>Practise</h2><p><a href='/'>Take today's practice set</a> and the <a href='/calendar.html'>exam calendar</a>.</p>")
    open(os.path.join(ROOT, "digest.html"), "w", encoding="utf-8").write(
        page("Weekly digest", "New exam notices from the last 7 days.", "".join(d), "digest.html"))
    # plain text version for WhatsApp
    t = ["📰 *This week's notices*", ""] + [f"• {n['n']}: {n['t']}" for n in recent[:12]] + ["", f"All links: {SITE}/digest.html"]
    os.makedirs(os.path.join(ROOT, "share"), exist_ok=True)
    open(os.path.join(ROOT, "share", "digest.txt"), "w", encoding="utf-8").write("\n".join(t) + "\n")
    print(f"calendar rows={len(up)} digest notices={len(recent)}")


if __name__ == "__main__":
    build()
