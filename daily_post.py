"""Daily post bot: builds a ready-to-copy WhatsApp post page (share/post.html + share/post.txt).
Runs inside update.py. No AI, no internet. Open https://tcs-avi.github.io/share/post.html on your phone, tap Copy, paste in WhatsApp."""
import hashlib, json, os
from datetime import date, timedelta

SITE = "https://tcs-avi.github.io/"
def _hours():
    try:
        return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "hours.json"), encoding="utf-8"))
    except Exception:
        return {"days": {}, "holidays": {}}


def _status(h, d):
    """Plain description of one date from hours.json, or None when normal full hours."""
    hol = h.get("holidays", {}).get(d.isoformat())
    if hol:
        return hol
    e = h.get("days", {}).get(d.strftime("%A"), "x")
    if e is None:
        return "closed"
    if e == "x":
        return None
    if e["close"] <= "15:00":
        return f"open {e['open']} to {e['close']} only (half day)"
    return None


def shop_note(d):
    h = _hours()
    t, n = _status(h, d), _status(h, d + timedelta(days=1))
    parts = []
    if t:
        parts.append(f"⛔ {t}" if t[0].isupper() else ("⛔ Shop closed today." if t == "closed" else f"⏰ Shop {t} today."))
    if n:
        parts.append(f"📅 Tomorrow: {n if n[0].isupper() else 'shop ' + n}.")
    return "\n".join(parts) or None


LET = "ABCD"


def _pick(pool, day, k=1, salt=""):
    """Deterministic pick: the same day always gives the same questions."""
    ranked = sorted(pool, key=lambda m: hashlib.md5((day + salt + m["id"]).encode()).hexdigest())
    return ranked[:k]


def _pool(mcqs, day):
    # today's fresh questions first; fall back to the whole bank so there is always something
    fresh = [m for m in mcqs if m.get("date") == day]
    return fresh if len(fresh) >= 3 else mcqs


def _fmt_q(m, n=None):
    head = (f"{n}. " if n else "") + m["q"].strip()
    opts = "\n".join(f"{LET[i]}) {o}" for i, o in enumerate(m["options"]))
    return head + "\n" + opts


def _ans(m):
    return f"{LET[m['answer']]}) {m['options'][m['answer']]}"


def build(root, data, bank_mcqs, today):
    mcqs = [m for m in list(bank_mcqs) + list(data.get("mcqs", []))
            if len(m.get("options", [])) == 4 and len(m["q"]) < 220 and max(len(o) for o in m["options"]) < 70]
    if not mcqs:
        return
    d = date.fromisoformat(today)
    yday = (d - timedelta(days=1)).isoformat()
    qod = _pick(_pool(mcqs, today), today, 1, "qod")[0]
    prev = _pick(_pool(mcqs, yday), yday, 1, "qod")[0]
    quiz = _pick([m for m in _pool(mcqs, today) if m["id"] != qod["id"]], today, 3, "quiz")
    note = shop_note(d)
    morning = ["🌅 *Question of the Day*", "", _fmt_q(qod), "",
               f"✅ Yesterday's answer: {_ans(prev)}", "",
               f"📚 Practise 6,500+ free questions: {SITE}"]
    if note:
        morning += ["", note]
    morning += ["", "— The Computer Services, Jakh, Samba"]
    evening = ["🌙 *3-question quiz*", ""]
    for i, m in enumerate(quiz, 1):
        evening += [_fmt_q(m, i), ""]
    evening += ["Reply with your answers. Answers tomorrow morning.", "", f"Free practice and mock tests: {SITE}",
                "— The Computer Services, Jakh, Samba"]
    posts = {"morning": "\n".join(morning), "evening": "\n".join(evening)}
    out = os.path.join(root, "share")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "post.txt"), "w", encoding="utf-8") as f:
        f.write(posts["morning"] + "\n")
    payload = json.dumps({"date": today, "posts": posts}, ensure_ascii=False).replace("</", "<\\/")
    html = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Today's WhatsApp post</title>
<style>body{margin:0;font:16px/1.5 system-ui,sans-serif;background:#f4f1e8;color:#1b1d27}main{max-width:36rem;margin:0 auto;padding:16px}
h1{font-size:1.25rem;margin:.2em 0}.d{color:#5b5f6b;margin:0 0 16px}section{background:#fff;border:1px solid #d8d3c3;border-radius:10px;padding:14px;margin:0 0 16px}
h2{font-size:1rem;margin:0 0 8px}pre{white-space:pre-wrap;word-wrap:break-word;font:inherit;margin:0 0 12px}
button,a.b{font:inherit;display:inline-block;padding:10px 14px;border-radius:8px;border:1px solid #1d3b78;background:#1d3b78;color:#fff;text-decoration:none;margin:0 8px 8px 0;cursor:pointer}
a.b{background:#fff;color:#1d3b78}@media(prefers-color-scheme:dark){body{background:#14161d;color:#ece8da}section{background:#1d2029;border-color:#33374a}.d{color:#a3a79f}a.b{background:#1d2029;color:#a9bff5}button{background:#a9bff5;color:#14161d;border-color:#a9bff5}}</style></head>
<body><main><h1>Today's WhatsApp post</h1><p class="d" id="d"></p><div id="w"></div>
<p class="d">Made automatically each morning. Check the answer before posting.</p></main>
<script>var P=__PAYLOAD__;document.getElementById("d").textContent=P.date;var W=document.getElementById("w");
[["morning","Morning post"],["evening","Evening quiz"]].forEach(function(k){var t=P.posts[k[0]],s=document.createElement("section"),h=document.createElement("h2"),p=document.createElement("pre"),b=document.createElement("button"),a=document.createElement("a");
h.textContent=k[1];p.textContent=t;b.textContent="Copy";b.onclick=function(){(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){b.textContent="Copied"},function(){var r=document.createRange();r.selectNodeContents(p);var g=getSelection();g.removeAllRanges();g.addRange(r);b.textContent="Select and copy"});setTimeout(function(){b.textContent="Copy"},2500)};
a.className="b";a.textContent="Open WhatsApp";a.href="https://wa.me/?text="+encodeURIComponent(t);a.target="_blank";a.rel="noopener";
s.appendChild(h);s.appendChild(p);s.appendChild(b);s.appendChild(a);W.appendChild(s)});</script></body></html>""".replace("__PAYLOAD__", payload)
    with open(os.path.join(out, "post.html"), "w", encoding="utf-8") as f:
        f.write(html)
