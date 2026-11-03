#!/usr/bin/env python3
"""ExamDaily auto-updater (standard library only).

1. Pulls headlines from news RSS feeds   -> data["news"]
2. Pulls exam notices (answer key, result, admit card, notification) per exam
   from Google News RSS searches          -> data["updates"]
3. If ANTHROPIC_API_KEY is set, drafts MCQs from new headlines -> data["mcqs"]
   (flagged verified=false, shown as "auto-generated" in the app)

Run:  python3 update.py
Reads/writes data.js (a JS file that assigns window.CA_DATA).
"""
import hashlib, json, os, re, sys, urllib.error, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_JS = os.path.join(ROOT, "data.js")
BANK_JS = os.path.join(ROOT, "bank.js")
UA = {"User-Agent": "Mozilla/5.0 (ExamDaily updater)"}

def _gn(q):
    return "https://news.google.com/rss/search?" + urllib.parse.urlencode(
        {"q": q + " when:2d", "hl": "en-IN", "gl": "IN", "ceid": "IN:en"})


# Only the Press Information Bureau (Government of India) feed is used. PIB's copyright policy allows free reproduction
# with accurate context and a prominent acknowledgement of the source. Other publishers' feeds were removed on purpose.
NEWS_FEEDS = [
    ("PIB", "https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3"),
]

# Exam labels (used for page names). Third-party news searches are NOT run any more; exam updates link to official sites only.
EXAM_QUERIES = [
    ("SSC", "SSC CGL OR CHSL OR MTS OR GD answer key OR result OR admit card"),
    ("IBPS", "IBPS PO OR Clerk OR SO notification OR result OR admit card"),
    ("IBPS RRB", "IBPS RRB notification OR result OR admit card"),
    ("RRB", "RRB NTPC OR \"Group D\" OR ALP OR JE answer key OR result"),
    ("JKSSB", "JKSSB answer key OR admit card OR notification OR result"),
    ("JKPSC", "JKPSC OR JKAS CCE notification OR result OR admit card"),
    ("SBI", "SBI PO OR Clerk notification OR result"),
    ("AIIMS", "AIIMS NORCET OR CRE notification OR result OR admit card"),
    ("NTA", "NTA CUET OR NEET OR \"JEE Main\" OR \"UGC NET\" answer key OR result"),
    ("Universities", "University of Kashmir OR \"University of Jammu\" OR \"Cluster University\" notification OR date sheet OR result"),
]

TYPE_WORDS = [("answer-key", ["answer key", "response sheet"]),
              ("result", ["result", "merit list", "cut off", "cutoff"]),
              ("admit-card", ["admit card", "hall ticket", "call letter"]),
              ("notification", ["notification", "recruitment", "vacancy", "vacancies", "apply"]),
              ("exam", ["exam date", "schedule", "date sheet", "postponed", "rescheduled"])]

SUBJECTS = ["National", "International", "Economy & Banking", "Science & Tech", "Sports",
            "Awards & Honours", "Defence", "Environment", "Polity & Governance",
            "Schemes & Policies", "Important Days", "J&K Special", "Static GK"]


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def parse_rss(raw):
    root = ET.fromstring(raw)
    out = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        pub = it.findtext("pubDate")
        try:
            d = parsedate_to_datetime(pub).astimezone(timezone.utc).date().isoformat()
        except Exception:
            d = datetime.now(timezone.utc).date().isoformat()
        if title and link:
            out.append({"title": re.sub(r"\s+", " ", title), "url": link, "date": d})
    return out


def sid(prefix, text):
    return prefix + hashlib.sha1(text.encode()).hexdigest()[:10]


def load():
    with open(DATA_JS, encoding="utf-8") as f:
        txt = f.read()
    m = re.search(r"window\.CA_DATA\s*=\s*(\{.*\})\s*;?\s*$", txt, re.S)
    return json.loads(m.group(1))


def save(data):
    with open(DATA_JS, "w", encoding="utf-8") as f:
        f.write("window.CA_DATA = " + json.dumps(data, indent=1, ensure_ascii=False) + ";\n")


def classify(title):
    t = title.lower()
    for typ, words in TYPE_WORDS:
        if any(w in t for w in words):
            return typ
    return "update"


def collect_news():
    items = []
    for name, url in NEWS_FEEDS:
        try:
            for it in parse_rss(fetch(url))[:15]:
                it["source"] = name
                items.append(it)
        except Exception as e:
            print(f"[warn] feed failed {name}: {e}", file=sys.stderr)
    return items


def collect_updates():
    """Disabled on purpose: exam notices are no longer pulled from third-party news searches."""
    return []


def _post(url, headers, payload, timeout=120):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"content-type": "application/json", **headers})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=timeout).read())
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %s from %s: %s" % (e.code, url.split("?")[0], e.read()[:300].decode("utf-8", "replace")))


def gemini_models(key):
    """Ask Google which models this key can use, newest free-friendly 'flash' models first."""
    names, token = [], None
    for _ in range(3):
        url = "https://generativelanguage.googleapis.com/v1beta/models?pageSize=100"
        if token:
            url += "&pageToken=" + urllib.parse.quote(token)
        r = json.loads(fetch_h(url, {"x-goog-api-key": key}))
        for m in r.get("models", []):
            n = m.get("name", "").replace("models/", "")
            if "generateContent" in m.get("supportedGenerationMethods", []) and "flash" in n:
                if not any(w in n for w in ("image", "tts", "live", "audio", "embedding", "robotics", "computer", "thinking", "exp")):
                    names.append(n)
        token = r.get("nextPageToken")
        if not token:
            break

    def rank(n):
        v = re.search(r"(\d+(?:\.\d+)?)", n)
        return ("preview" in n, -(float(v.group(1)) if v else 0), "lite" in n, n)
    return sorted(set(names), key=rank)


def fetch_h(url, headers, timeout=30):
    req = urllib.request.Request(url, headers={**UA, **headers})
    return urllib.request.urlopen(req, timeout=timeout).read()


def call_llm(prompt):
    """Free options first: Gemini or Groq (free API keys), then Anthropic (paid). Returns text or None."""
    if os.environ.get("GEMINI_API_KEY"):
        key = os.environ["GEMINI_API_KEY"]
        wanted = os.environ.get("GEMINI_MODEL")
        models = [wanted] if wanted else []
        try:
            models += [m for m in gemini_models(key) if m != wanted][:4]
        except Exception as e:
            print(f"[warn] could not list Gemini models: {e}", file=sys.stderr)
            models += ["gemini-2.5-flash", "gemini-flash-latest"]
        last = None
        for model in models:
            try:
                r = _post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                          {"x-goog-api-key": key},
                          {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.3}})
                print(f"[info] drafted with Gemini model {model}")
                return r["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                last = e
                print(f"[warn] Gemini model {model} failed: {e}", file=sys.stderr)
        raise last or RuntimeError("no Gemini model available")
    if os.environ.get("GROQ_API_KEY"):
        model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
        r = _post("https://api.groq.com/openai/v1/chat/completions",
                  {"authorization": "Bearer " + os.environ["GROQ_API_KEY"]},
                  {"model": model, "temperature": 0.3,
                   "messages": [{"role": "user", "content": prompt}]})
        return r["choices"][0]["message"]["content"]
    if os.environ.get("ANTHROPIC_API_KEY"):
        model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
        r = _post("https://api.anthropic.com/v1/messages",
                  {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"},
                  {"model": model, "max_tokens": 4000, "messages": [{"role": "user", "content": prompt}]})
        return "".join(b.get("text", "") for b in r["content"])
    return None


BAD_OPTIONS = ("all of the above", "none of the above", "both a and b", "all of these", "none of these", "both of the above")


def words(t):
    return set(re.findall(r"[a-z0-9]+", t.lower()))


def too_similar(q, others, limit=0.8):
    a = words(q)
    for o in others:
        b = words(o)
        if a and b and len(a & b) / len(a | b) >= limit:
            return True
    return False


def good_mcq(q, opts, ans, explain):
    """Simple quality gate for AI-drafted questions."""
    if not (15 <= len(q) <= 300):
        return False
    if any(len(o) == 0 or len(o) > 120 for o in opts):
        return False
    if any(o.lower().strip(". ") in BAD_OPTIONS for o in opts):
        return False
    if len(explain) < 8:
        return False
    # the answer should not simply be written inside the question
    if opts[ans].lower() in q.lower() and len(opts[ans]) > 3:
        return False
    return True


def parse_mcqs(text, headlines, existing=()):
    """Turn model output into validated MCQ dicts. Weak or duplicate items are skipped."""
    arr = json.loads(text[text.index("["): text.rindex("]") + 1])
    out = []
    today = datetime.now(timezone.utc).date().isoformat()
    seen_q = list(existing)
    for m in arr:
        try:
            h = headlines[int(m["h"])]
            opts = [str(o).strip() for o in m["options"]]
            ans = int(m["answer"])
            q = str(m["q"]).strip()
            explain = str(m.get("explain", "")).strip()
            if len(opts) != 4 or not 0 <= ans <= 3 or len(set(opts)) != 4:
                continue
            if not good_mcq(q, opts, ans, explain) or too_similar(q, seen_q):
                continue
            seen_q.append(q)
            out.append({"id": sid("a", q), "date": h["date"] or today,
                        "subject": m.get("subject") if m.get("subject") in SUBJECTS else "National",
                        "exams": m.get("exams") or ["SSC", "Banking"], "q": q, "options": opts,
                        "answer": ans, "explain": explain, "source": h["source"],
                        "sourceUrl": h["url"], "verified": False})
        except Exception:
            continue
    return out


def draft_mcqs(headlines, existing=(), limit=12):
    """Draft MCQs from headlines with an LLM. Skipped silently if no key is configured."""
    if not headlines or not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GROQ_API_KEY")
                             or os.environ.get("ANTHROPIC_API_KEY")):
        return []
    lines = "\n".join(f"{i}. {h['title']} ({h['source']})" for i, h in enumerate(headlines[:40]))
    prompt = (
        "From these news headlines, write up to %d multiple-choice questions useful for Indian "
        "competitive exams (SSC, Banking, Railways, JKSSB, JKPSC). Use ONLY facts stated in the "
        "headline; do not add facts you are unsure of. Skip headlines that are not exam-relevant.\n"
        "Return ONLY a JSON array. Each item: {\"h\": headline index, \"subject\": one of %s, "
        "\"exams\": subset of [\"SSC\",\"Banking\",\"Railways\",\"JKSSB\",\"JKPSC\",\"Universities & Entrances\"], "
        "\"q\": str, \"options\": [4 distinct strings], \"answer\": 0-3, \"explain\": one sentence}.\n\n%s"
        % (limit, json.dumps(SUBJECTS), lines))
    try:
        text = call_llm(prompt)
        return parse_mcqs(text, headlines, existing) if text else []
    except Exception as e:
        print(f"[warn] MCQ drafting failed: {e}", file=sys.stderr)
        return []


def merge(old, new, keep_days=None, cap=None, key="id"):
    seen = {x[key] for x in old}
    merged = old + [x for x in new if x[key] not in seen]
    merged.sort(key=lambda x: x.get("date", ""), reverse=True)
    if keep_days:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=keep_days)).date().isoformat()
        merged = [x for x in merged if x.get("date", "9") >= cutoff or x.get("verified") is True]
    return merged[:cap] if cap else merged


IST = timezone(timedelta(hours=5, minutes=30))


def main():
    data = load()
    today = datetime.now(IST).date().isoformat()
    news = collect_news()
    for n in news:
        n["id"] = sid("n", n["url"])
    if news:  # if every feed failed, keep yesterday's PIB headlines instead of wiping them
        data["news"] = merge([], news, keep_days=7, cap=80)
    else:
        data["news"] = [n for n in data.get("news", []) if n.get("source") == "PIB"]
    # drop anything auto-collected from third-party searches earlier; keep hand-written entries
    data["updates"] = [u for u in data.get("updates", []) if not str(u.get("note", "")).startswith("Auto-collected")]
    new_mcqs = []
    if data.get("drafted_on") != today:  # draft new questions only once per day
        new_mcqs = draft_mcqs(news, [m["q"] for m in data.get("mcqs", [])][-300:])
        if new_mcqs:
            data["drafted_on"] = today
    static = [m for m in data.get("mcqs", []) if m.get("static")]
    dynamic = [m for m in data.get("mcqs", []) if not m.get("static")]
    dynamic = merge(dynamic, new_mcqs, keep_days=180, cap=1500)
    # when bank.js exists the static questions live there; keep data.js small
    data["mcqs"] = dynamic if os.path.exists(BANK_JS) else dynamic + static
    data["generated"] = today
    save(data)
    print(f"news={len(data.get('news', []))} updates={len(data['updates'])} mcqs={len(data['mcqs'])} (+{len(new_mcqs)} new)")


if __name__ == "__main__":
    main()
