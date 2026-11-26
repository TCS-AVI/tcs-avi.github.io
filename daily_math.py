"""Daily computed Quant and Reasoning questions (no AI, no internet).
Answers are calculated by code, so they are exact. Seeded by date: the same day gives the same set."""
import hashlib, random
import qgen, rgen

def daily(today, nq=6, nr=4, seen=None):
    seen = set(seen or ())
    seed = int(hashlib.md5(today.encode()).hexdigest()[:8], 16)
    out = []
    for gen, n in ((qgen, nq), (rgen, nr)):
        got = 0
        for extra in range(6):  # retry with other seeds if a question was already used
            for sub, q, c, w, x, topic in gen.run(seed + extra * 7919, n * 3):
                if got >= n:
                    break
                if q.strip().lower() in seen:
                    continue
                seen.add(q.strip().lower())
                rnd = random.Random(hashlib.md5((today + q).encode()).hexdigest())
                opts = list(w) + [c]
                rnd.shuffle(opts)
                out.append({
                    "id": "d" + hashlib.md5((today + sub + q).encode()).hexdigest()[:10],
                    "date": today, "subject": sub, "topic": topic,
                    "exams": ["SSC", "Banking", "Railways", "JKSSB"],
                    "q": q, "options": opts, "answer": opts.index(c), "explain": x,
                    "source": "Daily practice (computed)", "sourceUrl": "", "verified": False,
                })
                got += 1
            if got >= n:
                break
    return out
