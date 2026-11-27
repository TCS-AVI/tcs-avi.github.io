"""Question quality bot. Reads bank.js and data.js; writes quality_report.md only for real problems."""
import json, os, re, sys
from collections import Counter
ROOT = os.path.dirname(os.path.abspath(__file__))


def load(f):
    t = open(os.path.join(ROOT, f), encoding="utf-8").read()
    return json.loads(t[t.index("{"):t.rindex("}") + 1]).get("mcqs", [])


def norm(s): return re.sub(r"[\W_]+", " ", str(s).lower()).strip()


def main():
    ms = load("bank.js") + load("data.js"); P = []
    seen, dup = {}, []
    for m in ms:
        k = norm(m["q"]) + "|" + "|".join(sorted(norm(o) for o in m["options"]))
        if k in seen and seen[k] != m["id"]: dup.append((m["id"], seen[k]))
        seen.setdefault(k, m["id"])
    if len(dup) > 150: P.append(f"{len(dup)} questions are exact duplicates (same text and options), e.g. {dup[0][0]} and {dup[0][1]}")
    same_q = Counter(norm(m["q"]) for m in ms if len(norm(m["q"])) > 30)
    conflict = [q for q, c in same_q.items() if c > 1]
    amb = []
    byq = {}
    for m in ms:
        if len(norm(m["q"])) > 30:
            byq.setdefault(norm(m["q"]) + "|" + "|".join(sorted(norm(o) for o in m["options"])), set()).add(norm(m["options"][m["answer"]]))
    amb = [q for q, a in byq.items() if len(a) > 1]
    if amb:
        first = amb[0].split("|")[0][:90]
        P.append(f"{len(amb)} questions appear twice with DIFFERENT correct answers. One is wrong. First: {first}")
    short = [m["id"] for m in ms if len(norm(m["q"])) < 12]
    if len(short) > 30: P.append(f"{len(short)} questions are very short, e.g. {short[0]}")
    inopt = [m["id"] for m in ms if any(norm(o) in norm(m["q"]) and len(norm(o)) > 25 for o in m["options"])]
    if len(inopt) > 20: P.append(f"{len(inopt)} questions contain an answer option word-for-word in the question")
    pos = Counter(m["answer"] for m in ms[-1500:])
    tot = sum(pos.values()) or 1
    if max(pos.values()) / tot > 0.40: P.append("Correct answers are bunched on one option letter in recent questions: " + str(dict(pos)))
    nox = [m["id"] for m in ms if not str(m.get("explain", "")).strip()]
    if len(nox) / max(len(ms), 1) > 0.35: P.append(f"{len(nox)} of {len(ms)} questions have no explanation")
    out = os.path.join(ROOT, "quality_report.md")
    if os.path.exists(out): os.remove(out)
    if P:
        open(out, "w", encoding="utf-8").write("## Question quality check\n\n" + "\n".join("- " + p for p in P) + "\n")
    print(f"questions={len(ms)} dup={len(dup)} conflicting={len(amb)} problems={len(P)}")
    for p in P: print(" -", p)


if __name__ == "__main__":
    main()
