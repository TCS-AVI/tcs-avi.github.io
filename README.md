# The Computer Services

Static web app (no server needed) for current affairs MCQs, interesting questions and exam updates (SSC, IBPS, RRB, SBI/RBI, JKSSB, JKPSC/JKAS, AIIMS, NTA, universities).

## Run locally
```
python3 -m http.server 8000     # open http://localhost:8000
```

## Host free (GitHub Pages)
1. Push this folder to a GitHub repo.
2. Settings > Pages > deploy from branch `main`, folder `/ (root)`.
3. (Optional, free) Auto-drafted MCQs: get a free key from Google AI Studio (Gemini) or Groq, then in your repo go to Settings > Secrets and variables > Actions > New secret, and add it as `GEMINI_API_KEY` or `GROQ_API_KEY`. Free-tier limits and model names change; if drafting stops working, set the `GEMINI_MODEL` / `GROQ_MODEL` environment variable in the workflow to a current free model.

The workflow in `.github/workflows/update.yml` runs `update.py` daily at 06:00 IST and commits fresh `data.js`.

## What updates automatically
- News headlines from PIB, The Hindu, Indian Express, Greater Kashmir, Daily Excelsior.
- Exam updates (notifications, admit cards, results, answer keys) via Google News searches per exam.
- MCQs drafted from headlines, only if `GEMINI_API_KEY` or `GROQ_API_KEY` is set (both have free tiers). They are labelled "auto-generated".

Edit `EXAM_QUERIES` / `NEWS_FEEDS` in `update.py` to add exams or sources.

## Important notes
- **Answer keys:** official answer keys are published only on each board's portal (login-based for SSC/IBPS). The app links to sources and does not republish them.
- **Accuracy:** auto-generated MCQs can be wrong. Review them before relying on them; set `"verified": true` in `data.js` for ones you have checked.
- **Content rights:** the seed MCQs are original rewrites of facts, with source links. Do not bulk copy coaching-site question banks.
- Check each site's terms before adding scrapers; RSS feeds are used here.

## Install as an app / share
- On a phone, open the site in Chrome and tap **Install app** (or the browser menu > Add to Home screen). It then opens like an app and works offline with the last-loaded questions.
- Every question and exam update has a WhatsApp share button. Questions are shared without the answer.
- `sw.js` caches the site. `data.js` is always fetched fresh first, so daily updates appear when online.

## Mock tests
The **Mock Test** tab offers SSC-style, Banking-style and J&K-exam-style timed tests (drawn at random from the bank), plus a custom test. It has a countdown timer, question palette, mark-for-review, negative marking, a section-wise score and an answer review. Results are kept only in the visitor's browser.
