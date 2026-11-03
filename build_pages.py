#!/usr/bin/env python3
"""Builds the static, search-engine-friendly pages and the daily share kit.
Reads bank.js, data.js, reviewed.js. Writes practice/, exams/, share/ and sitemap.xml.
Standard library only; the share image needs Pillow (optional, skipped if missing)."""
import html, json, os, random, re, sys
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://tcs-avi.github.io"
IST = timezone(timedelta(hours=5, minutes=30))
TODAY = datetime.now(IST).date()
CONTACT = "baglajakh@gmail.com"

EXAM_LABELS = ["SSC", "IBPS", "IBPS RRB", "RRB", "JKSSB", "JKPSC", "SBI", "AIIMS", "NTA", "Universities"]
LABEL_TO_EXAM = {"SSC": "SSC", "IBPS": "Banking", "IBPS RRB": "Banking", "SBI": "Banking", "RRB": "Railways",
                 "JKSSB": "JKSSB", "JKPSC": "JKPSC", "AIIMS": "Universities & Entrances",
                 "NTA": "Universities & Entrances", "Universities": "Universities & Entrances"}
LABEL_FULL = {"SSC": "SSC (CGL, CHSL, MTS, GD)", "IBPS": "IBPS (PO, Clerk, SO)", "IBPS RRB": "IBPS RRB (Gramin Banks)",
              "RRB": "Railway RRB (NTPC, Group D, ALP, JE)", "JKSSB": "JKSSB (J&K Services Selection Board)",
              "JKPSC": "JKPSC / JKAS", "SBI": "SBI (PO, Clerk)", "AIIMS": "AIIMS (NORCET, CRE)",
              "NTA": "NTA (CUET, NEET, JEE Main, UGC NET)", "Universities": "Universities (Kashmir, Jammu, Cluster)"}


def read_js(name, default):
    p = os.path.join(ROOT, name)
    if not os.path.exists(p):
        return default
    m = re.search(r"=\s*(\{.*\})\s*;?\s*$", open(p, encoding="utf-8").read(), re.S)
    return json.loads(m.group(1)) if m else default


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("&", "and")).strip("-")


def e(s):
    return html.escape(str(s), quote=True)


def write(rel, text):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


CSS = """:root{--bg:#f6f5f1;--fg:#1c1b19;--mut:#625e56;--card:#fff;--line:#dedad0;--acc:#0b3b8c;--ok:#176b35}
@media (prefers-color-scheme:dark){:root{--bg:#141412;--fg:#ece9e1;--mut:#9a958a;--card:#1e1d1a;--line:#36342f;--acc:#8db6ff;--ok:#7bd49a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,sans-serif}
header,main,footer{max-width:820px;margin:0 auto;padding:12px 16px}header{display:flex;gap:12px;align-items:center}
header img{width:48px;height:48px;border-radius:50%}header a{color:var(--fg);text-decoration:none;font-weight:700}
nav a{margin-right:12px}a{color:var(--acc)}h1{font-size:1.4rem;margin:.4em 0}h3{font-size:1rem;margin:0 0 6px}
article,.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:12px 0}
ol.o{margin:6px 0;padding-left:1.4em}.ans{color:var(--ok);font-weight:600}.tag{font-size:.75rem;border:1px solid var(--line);border-radius:99px;padding:1px 8px;color:var(--mut)}
.mut,footer{color:var(--mut);font-size:.85rem}.btn{display:inline-block;background:var(--acc);color:var(--bg);padding:8px 14px;border-radius:10px;text-decoration:none}
ul.l{padding-left:1.2em}"""


def page(path_rel, title, desc, body, noindex=False):
    depth = path_rel.count("/")
    canon = SITE + "/" + path_rel.replace("index.html", "")
    robots = '<meta name="robots" content="noindex,nofollow">' if noindex else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">{robots}
<link rel="canonical" href="{canon}"><link rel="icon" href="/icon-192.png">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}/icon-512.png"><meta property="og:url" content="{canon}"><meta name="twitter:card" content="summary">
<style>{CSS}</style></head><body>
<header><img src="/logo.png" alt="The Computer Services logo" width="48" height="48"><div><a href="/">The Computer Services</a><br><span class="mut">Free exam preparation: MCQs, mock tests, exam updates</span></div></header>
<main><nav><a href="/">App</a><a href="/practice/">Practice by subject</a><a href="/exams/">Exam updates</a><a href="/touch/">Typing practice</a></nav>
{body}</main>
<footer>These pages are practice material written from standard reference knowledge. Questions marked "not yet reviewed" have not been checked by a person and can contain errors; verify against official sources. Official answer keys are published only on each board's website, and exam dates change, so always confirm on the official notification. Found a mistake? Email <a href="mailto:{CONTACT}">{CONTACT}</a>. &copy; The Computer Services.</footer>
</body></html>"""


def main():
    bank = read_js("bank.js", {"mcqs": []})["mcqs"]
    data = read_js("data.js", {"mcqs": [], "updates": [], "exams": []})
    rv = read_js("reviewed.js", {"ok": [], "hide": []})
    ok, hide = set(rv.get("ok", [])), set(rv.get("hide", []))
    seen, mcqs = set(), []
    for m in data.get("mcqs", []) + bank:
        if m["id"] in seen or m["id"] in hide:
            continue
        seen.add(m["id"])
        m["_st"] = "reviewed" if m["id"] in ok else ("computed" if m.get("static") and m["subject"] == "Quant" else
                                                      ("verified" if m.get("verified") else "unreviewed"))
        mcqs.append(m)

    urls = [("/", None), ("/touch/", None)]
    # ---------- subject pages ----------
    cnt = {}
    for m in mcqs:
        cnt[m["subject"]] = cnt.get(m["subject"], 0) + 1
    subjects = sorted(k for k, v in cnt.items() if v >= 10)  # thin subjects stay in the app only
    rank = {"reviewed": 0, "verified": 0, "computed": 1, "unreviewed": 2}
    for sub in subjects:
        qs = sorted([m for m in mcqs if m["subject"] == sub and (m.get("static") or m["_st"] != "unreviewed" or True)],
                    key=lambda m: (rank[m["_st"]], m["id"]))
        total = len(qs)
        pick = qs[:50]
        arts = []
        for i, m in enumerate(pick, 1):
            lab = {"reviewed": "reviewed", "verified": "verified", "computed": "answer computed",
                   "unreviewed": "not yet reviewed"}[m["_st"]]
            opts = "".join(f"<li>{e(o)}</li>" for o in m["options"])
            arts.append(f'<article id="q-{e(m["id"])}"><h3>{i}. {e(m["q"])}</h3><ol class="o" type="A">{opts}</ol>'
                        f'<p class="ans">Answer: {"ABCD"[m["answer"]]}) {e(m["options"][m["answer"]])}</p>'
                        f'<p>{e(m.get("explain",""))}</p><span class="tag">{lab}</span></article>')
        rel = f"practice/{slug(sub)}.html"
        app = f"/#tab=practice&subject={quote(sub)}"
        others = " &middot; ".join(f'<a href="/practice/{slug(s)}.html">{e(s)}</a>' for s in subjects if s != sub)
        body = (f"<h1>{e(sub)} MCQs with answers</h1><p>{total} practice questions in this subject for SSC, Banking, Railways, "
                f"JKSSB, JKPSC and entrance tests. Below are {len(pick)} of them with answers and explanations.</p>"
                f'<p><a class="btn" href="{app}">Practise all {total} in the app (free)</a></p>' + "".join(arts) +
                f'<p><a class="btn" href="{app}">Practise all {total} in the app (free)</a></p><p class="mut">Other subjects: {others}</p>')
        title = f"{sub} MCQs with Answers for SSC, Banking, RRB and JKSSB | The Computer Services"
        write(rel, page(rel, title, f"{total} {sub} practice questions with answers and explanations for SSC, Banking, Railways, JKSSB and JKPSC. Free.", body))
        urls.append(("/" + rel, None))
    idx = "".join(f'<li><a href="/practice/{slug(s)}.html">{e(s)}</a> <span class="mut">({cnt[s]} questions)</span></li>' for s in subjects)
    write("practice/index.html", page("practice/index.html", "Free MCQs by Subject for SSC, Banking, RRB and JKSSB | The Computer Services",
          "Browse practice MCQs by subject with answers: maths, reasoning, English, GK, J&K special and more.",
          f'<h1>Practice MCQs by subject</h1><ul class="l">{idx}</ul>'))
    urls.append(("/practice/", None))

    labels = []  # exam-update pages removed on purpose

    # ---------- sitemap ----------
    lm = TODAY.isoformat()
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{lm}</lastmod></url>\n" for u, _ in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /review.html\nDisallow: /share/\nSitemap: {SITE}/sitemap.xml\n")

    build_share(mcqs, data)
    print(f"pages: {len(urls)} urls, {len(subjects)} subjects, {len(labels)} exams")


# ---------- daily share kit ----------
def pick_daily(mcqs):
    rnd = random.Random("share-" + TODAY.isoformat())
    pool = [m for m in mcqs if len(m["q"]) <= 130 and all(len(o) <= 36 for o in m["options"])]
    good = [m for m in pool if m["_st"] in ("reviewed", "verified", "computed")] or pool
    if len([m for m in pool if m["_st"] in ("reviewed", "verified")]) >= 20:
        good = [m for m in pool if m["_st"] in ("reviewed", "verified")]
    by = {}
    for m in sorted(good, key=lambda m: m["id"]):
        by.setdefault(m["subject"], []).append(m)
    subs = sorted(by)
    rnd.shuffle(subs)
    return [rnd.choice(by[s]) for s in subs[:5]]


def build_share(mcqs, data):
    qs = pick_daily(mcqs)
    if not qs:
        return
    d = TODAY.strftime("%d %b %Y").lstrip("0")
    L = [f"\U0001F4DA *Daily Quiz | {d}*", "The Computer Services", ""]
    for i, m in enumerate(qs, 1):
        L.append(f"*{i}. {m['q']}*")
        L += [f"{'ABCD'[j]}) {o}" for j, o in enumerate(m["options"])]
        L.append("")
    L += ["Reply with your answers. Answers below \U0001F447", ".", ".", ".", ".", ".", ""]
    L.append("✅ *Answers:* " + ", ".join(f"{i}-{'ABCD'[m['answer']]}" for i, m in enumerate(qs, 1)))
    L.append("")
    ups = sorted(data.get("updates", []), key=lambda u: u.get("date", ""), reverse=True)[:3]
    if ups:
        L.append("\U0001F4E2 *Exam updates*")
        L += [f"• {u['title']}" for u in ups]
        L.append("(Confirm on the official website.)")
        L.append("")
    L += [f"\U0001F517 Practise free: {SITE}/", "\U0001F4F2 Tap *Install* in the app to add it to your phone.",
          "Found a mistake or have feedback? Use the Report button in the app.", "",
          "Practice material only. Verify with official sources. Not affiliated with any exam body.", f"Spotted a mistake? Email {CONTACT}"]
    text = "\n".join(L)
    write("share/post.txt", text)
    has_img = make_image(qs, d)
    img = '<p><img src="status.png" alt="Status image" style="max-width:100%;width:320px;border-radius:12px"></p><p><a class="btn" href="status.png" download="status.png">Download image</a></p>' if has_img else "<p class=mut>Image not generated today.</p>"
    body = (f"<h1>Daily Quiz ({e(d)})</h1><p class='mut'>Try today's questions, then share them with friends who are preparing too. Answers are at the end of the text.</p>"
            f'<div class="card"><pre id="t" style="white-space:pre-wrap;font:inherit;margin:0">{e(text)}</pre></div>'
            '<p><button class="btn" id="c" style="border:0;cursor:pointer">Copy quiz text</button> '
            f'<a class="btn" href="https://wa.me/?text={quote(text)}">Open in WhatsApp</a></p>' + img +
            "<script>document.getElementById('c').onclick=function(){var t=document.getElementById('t').textContent,b=this;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){b.textContent='Copied'}).catch(function(){var r=document.createRange();r.selectNodeContents(document.getElementById('t'));var s=getSelection();s.removeAllRanges();s.addRange(r)})}</script>")
    write("share/index.html", page("share/index.html", "Daily Quiz", "Today's daily quiz to copy and share.", body, noindex=True))


def make_image(qs, d):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return False
    def font(size, bold=False):
        for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""),
                  "/usr/share/fonts/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else "")):
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
        try:
            return ImageFont.load_default(size)
        except Exception:
            return ImageFont.load_default()
    W, H = 1080, 1920
    im = Image.new("RGB", (W, H), (251, 250, 246))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 14], fill=(255, 153, 51)); dr.rectangle([0, 14, W, 28], fill=(255, 255, 255)); dr.rectangle([0, 28, W, 42], fill=(19, 136, 8))
    y = 190  # keep clear of WhatsApp's top bar
    lp = os.path.join(ROOT, "logo.png")
    if os.path.exists(lp):
        lg = Image.open(lp).convert("RGBA").resize((150, 150))
        im.paste(lg, (70, y), lg)
    dr.text((250, y + 10), "Daily Quiz", font=font(70, True), fill=(11, 59, 140))
    dr.text((250, y + 100), d + "  |  The Computer Services", font=font(32), fill=(98, 94, 86))
    y += 230

    def wrap(t, f, w):
        out, cur = [], ""
        for word in t.split():
            tr = (cur + " " + word).strip()
            if dr.textlength(tr, font=f) <= w:
                cur = tr
            else:
                out.append(cur); cur = word
        return out + [cur]
    fq, fo = font(40, True), font(34)
    limit = H - 440
    for i, m in enumerate(qs[:4], 1):
        lines = wrap(f"{i}. {m['q']}", fq, W - 200)
        h = len(lines) * 52 + 4 * 46 + 50
        if y + h > limit:
            break
        dr.rounded_rectangle([50, y, W - 50, y + h], radius=26, fill=(255, 255, 255), outline=(222, 218, 208), width=3)
        yy = y + 24
        for ln in lines:
            dr.text((80, yy), ln, font=fq, fill=(28, 27, 25)); yy += 52
        yy += 6
        for j, o in enumerate(m["options"]):
            dr.text((100, yy), f"{'ABCD'[j]})  {o}", font=fo, fill=(60, 58, 52)); yy += 46
        y += h + 34
    dr.text((70, H - 400), "More questions and answers: see the channel post.", font=font(38, True), fill=(11, 59, 140))
    dr.text((70, H - 340), "Practise free: tcs-avi.github.io", font=font(38), fill=(28, 27, 25))
    dr.text((70, H - 280), "Tap Install to add the app to your phone.", font=font(32), fill=(98, 94, 86))
    dr.text((70, H - 130), "Practice material only. Verify with official sources.", font=font(26), fill=(98, 94, 86))
    os.makedirs(os.path.join(ROOT, "share"), exist_ok=True)
    im.save(os.path.join(ROOT, "share", "status.png"), optimize=True)
    return True


if __name__ == "__main__":
    main()
