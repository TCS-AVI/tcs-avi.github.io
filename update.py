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
UA = {"User-Agent": "Mozilla/5.0 (ExamDaily updater)"}

def _gn(q):
    return "https://news.google.com/rss/search?" + urllib.parse.urlencode(
        {"q": q + " when:2d", "hl": "en-IN", "gl": "IN", "ceid": "IN:en"})


NEWS_FEEDS = [
    ("PIB", "https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3"),
    ("The Hindu", "https://www.thehindu.com/news/national/feeder/default.rss"),
    ("Greater Kashmir", "https://www.greaterkashmir.com/feed"),
    ("Google News India", _gn("India government OR economy OR RBI OR defence OR ISRO OR summit OR award")),
    ("Google News J&K", _gn("Jammu Kashmir OR Ladakh government OR JKSSB OR JKPSC OR university")),
]

# (label shown in app, search query)
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
    items = []
    for label, q in EXAM_QUERIES:
        url = "https://news.google.com/rss/search?" + urllib.parse.urlencode(
            {"q": q + " when:14d", "hl": "en-IN", "gl": "IN", "ceid": "IN:en"})
        try:
            for it in parse_rss(fetch(url))[:6]:
                items.append({"id": sid("u", it["url"]), "date": it["date"], "exam": label,
                              "type": classify(it["title"]), "title": it["title"],
                              "url": it["url"], "note": "Auto-collected headline. Confirm on the official website."})
        except Exception as e:
            print(f"[warn] exam query failed {label}: {e}", file=sys.stderr)
    return items


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


def parse_mcqs(text, headlines):
    """Turn model output into validated MCQ dicts. Bad items are skipped."""
    arr = json.loads(text[text.index("["): text.rindex("]") + 1])
    out = []
    today = datetime.now(timezone.utc).date().isoformat()
    for m in arr:
        try:
            h = headlines[int(m["h"])]
            opts = [str(o).strip() for o in m["options"]]
            ans = int(m["answer"])
            if len(opts) != 4 or not 0 <= ans <= 3 or len(set(opts)) != 4 or not m["q"].strip():
                continue
            out.append({"id": sid("a", m["q"]), "date": h["date"] or today,
                        "subject": m.get("subject") if m.get("subject") in SUBJECTS else "National",
                        "exams": m.get("exams") or ["SSC", "Banking"], "q": m["q"].strip(), "options": opts,
                        "answer": ans, "explain": str(m.get("explain", "")).strip(), "source": h["source"],
                        "sourceUrl": h["url"], "verified": False})
        except Exception:
            continue
    return out


def draft_mcqs(headlines, limit=12):
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
        return parse_mcqs(text, headlines) if text else []
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


def main():
    data = load()
    news = collect_news()
    for n in news:
        n["id"] = sid("n", n["url"])
    data["news"] = merge([], news, keep_days=7, cap=80)
    data["updates"] = merge(data.get("updates", []), collect_updates(), keep_days=120, cap=300)
    new_mcqs = draft_mcqs(news)
    static = [m for m in data.get("mcqs", []) if m.get("static")]
    dynamic = [m for m in data.get("mcqs", []) if not m.get("static")]
    dynamic = merge(dynamic, new_mcqs, keep_days=180, cap=1500)
    data["mcqs"] = dynamic + static
    data["generated"] = datetime.now(timezone.utc).date().isoformat()
    save(data)
    print(f"news={len(data['news'])} updates={len(data['updates'])} mcqs={len(data['mcqs'])} (+{len(new_mcqs)} new)")


if __name__ == "__main__":
    main()
