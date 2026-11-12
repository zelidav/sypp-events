"""Builds the static events.syppit.com pages from the fragments in src/.
Edit OPERATOR / CONTACT here; every page picks them up. Run: python build.py"""
import pathlib, re

OPERATOR = "SYPP Cloud Bar"
CONTACT_EMAIL = "info@syppit.com"
SMS_NUMBER = "(562) 4-SYPPIT, (562) 479-7748"
PROGRAM = "SYPP Cloud Bar Event Updates"
UPDATED = "November 12, 2026"
BOOK_ENDPOINT = ""       # set to the Cloud Run booking endpoint when it ships
API_BASE = "https://sypp-phone-avkv2gqima-ue.a.run.app"            # booking API base, no trailing slash, e.g. https://sypp-phone-avkv2gqima-ue.a.run.app
                         # (book.html uses /api/public/brands, /api/public/stores, /api/book). Empty = email fallback.

NAV = [("index.html", "Events"), ("book.html", "Book an event"), ("sms-terms.html", "Text messages"),
       ("privacy.html", "Privacy"), ("terms.html", "Terms")]

def page(fname, title, body):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{t}</a>' for h, t in NAV)
    sms_line = SMS_NUMBER or "our events line (shown on every text we send)"
    body = (body.replace("{{OPERATOR}}", OPERATOR).replace("{{EMAIL}}", CONTACT_EMAIL)
                .replace("{{PROGRAM}}", PROGRAM).replace("{{UPDATED}}", UPDATED)
                .replace("{{SMS_NUMBER}}", sms_line).replace("{{BOOK_ENDPOINT}}", BOOK_ENDPOINT)
                .replace("{{API_BASE}}", API_BASE))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="SYPP Cloud Bar in-store events for retail partners in New York.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@600;700&family=Figtree:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/site.css"><link rel="icon" href="assets/sypp-logo.png">
</head><body>
<header class="top"><div class="wrap"><a href="index.html"><img src="assets/sypp-logo.png" alt="SYPP Cloud Bar" width="101" height="40"></a><nav class="links">{nav}</nav></div></header>
<main><div class="wrap">
{body}
</div></main>
<footer><div class="wrap"><span>&copy; 2026 {OPERATOR}</span><span><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> · <a href="privacy.html">Privacy</a> · <a href="sms-terms.html">Text message terms</a> · <a href="terms.html">Terms</a></span></div></footer>
</body></html>
"""

src = pathlib.Path("src")
for f in sorted(src.glob("*.html")):
    raw = f.read_text(encoding="utf-8")
    title = re.search(r"<!--\s*title:\s*(.+?)\s*-->", raw).group(1)
    out = page(f.name, title, re.sub(r"<!--\s*title:.*?-->\s*", "", raw, count=1))
    pathlib.Path(f.name).write_text(out, encoding="utf-8")
    print("built", f.name)
