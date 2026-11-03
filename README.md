# The Computer Services (v3)

Free static exam-prep web app, hosted on GitHub Pages and updated by GitHub Actions.

## Files
- index.html - the app. bank.js - static question bank. data.js - bot-written daily content.
- reviewed.js - which questions a person has checked (and which are hidden until fixed).
- review.html - the review tool for teachers and reviewers (not linked from the app, not indexed).
- build_pages.py - builds practice/ (one page per subject), exams/ (one per exam body), share/ (daily WhatsApp post and Status image), sitemap.xml, robots.txt. Run automatically after update.py.
- update.py, update.yml.txt (-> .github/workflows/update.yml), sw.js, manifest, icons.

## Reviewing questions
1. Open https://tcs-avi.github.io/review.html (reviewers can do this on a phone).
2. For each question press Correct or Needs a fix. Computed maths questions are skipped (their answers come from calculation).
3. Press Export, then send the text to the owner (or paste it over the whole of reviewed.js on GitHub).
4. Reviewed questions show a "reviewed" tick. "Needs a fix" questions are hidden from the whole site until fixed; the export lists fix notes.
5. In Practice, "Reviewed or computed only" filters to checked questions.

## Daily share kit
Open https://tcs-avi.github.io/share/ on your phone: copy the post text for the WhatsApp channel, download the image for your Status. It refreshes automatically.

## Notes
- Official answer keys are only linked, never republished.
- Progress is stored only in the visitor's browser.
