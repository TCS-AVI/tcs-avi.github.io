"""Smoke test: opens the site like a student's phone and uses the main parts. Exit 1 with smoke_report.md on any problem.
Usage: python3 smoke.py http://localhost:8000/   (the workflow starts a local server first)"""
import sys, re
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/"
bad = []

with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 390, "height": 800}, timezone_id="Asia/Kolkata", service_workers="block")
    c.add_init_script("try{sessionStorage.setItem('tcs_sp','1');localStorage.setItem('ed_ack','1');localStorage.setItem('ed_tour','1')}catch(e){}")
    p = c.new_page()
    errs = []
    p.route(re.compile(r"goatcounter|zgo\.at"), lambda r: r.abort())   # never count test visits
    p.set_default_timeout(15000)
    p.on("pageerror", lambda e: errs.append("page error: " + str(e)[:150]))
    p.on("response", lambda r: bad.append(f"{r.status} {r.url}") if r.status >= 400 and URL.split('/')[2] in r.url else None)
    try:
        p.goto(URL, wait_until="domcontentloaded", timeout=60000)
        p.wait_for_function("document.querySelector('#view') && document.querySelector('#view').children.length>0 && !document.querySelector('#view .ldq')", timeout=30000)
    except Exception as e:
        bad.append("home page did not finish loading: " + str(e)[:120])
    else:
        n = p.evaluate("(document.getElementById('hsub')||{}).textContent||''")
        m = re.match(r"([\d,]+) free questions", n)
        if not m or int(m.group(1).replace(",", "")) < 1000: bad.append("question count in header looks wrong: " + n)
        tabs = p.eval_on_selector_all("#tabs [data-t]", "a=>a.map(x=>x.dataset.t)")
        if len(tabs) < 6: bad.append(f"only {len(tabs)} tabs found")
        def tab(t):
            p.eval_on_selector(f"#tabs [data-t={t}]", "e=>e.click()"); p.wait_for_timeout(450)
        for t in [x for x in tabs if x not in ("more", "typing")]:
            try:
                tab(t)
                if len(p.inner_text("#view", timeout=5000).strip()) < 20 and t != "saved": bad.append(f"tab '{t}' is empty")
            except Exception as e:
                bad.append(f"tab '{t}' failed: {str(e)[:80]}")
        try:   # practice: answer the first question
            tab("practice")
            if p.locator(".opt").count() < 2: bad.append("practice: no answer options found")
            else:
                p.eval_on_selector(".opt", "e=>e.click()"); p.wait_for_timeout(300)
        except Exception as e:
            bad.append("practice failed: " + str(e)[:100])
        try:   # quick quiz: start and answer one
            tab("quiz")
            p.eval_on_selector("#view .btn", "e=>e.click()"); p.wait_for_timeout(500)
            if p.locator(".opt").count() < 2: bad.append("quick quiz did not start")
            else: p.eval_on_selector(".opt", "e=>e.click()")
        except Exception as e:
            bad.append("quick quiz failed: " + str(e)[:100])
        # Hindi switch
        try:
            p.evaluate("(()=>{var a=window.__a11y;if(a){var s=a.load();s.lang='hi';a.save(s);a.apply(s)}})()"); p.wait_for_timeout(500)
            if p.evaluate("document.documentElement.getAttribute('data-lang')") != "hi": bad.append("Hindi switch did not apply")
        except Exception as e:
            bad.append("Hindi check failed")
    bad += errs
    b.close()

if bad:
    open("smoke_report.md", "w").write("## Smoke test found problems\n\n" + "\n".join("- " + x for x in bad[:25]) + "\n")
    print("\n".join(bad)); sys.exit(1)
print("smoke ok")
