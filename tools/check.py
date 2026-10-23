"""Site check. Run with: python3 tools/check.py

Fails when a referenced local asset is missing or an absolute
bautiavila.com URL points to a file that does not exist.
No dependencies. Exits 1 on failure.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML_FILES = sorted(p for p in ROOT.glob("*.html") if not p.name.startswith("."))
ASSET = re.compile(r'(?:src|href)="([^"#:]+)"')
HOST_URL = re.compile(r"https://bautiavila\.com(/[^\"'\s>)]*)")
SKIP_PREFIX = ("http", "mailto:", "data:", "//")


def main() -> int:
    pages = {page.name: page.read_text(encoding="utf-8") for page in HTML_FILES}
    problems = []

    for name, html in pages.items():
        for asset in ASSET.findall(html):
            if asset.startswith(SKIP_PREFIX) or not asset:
                continue
            if not (ROOT / asset).exists():
                problems.append(f"{name}: missing asset {asset}")

        for path in HOST_URL.findall(html):
            if path == "/":
                continue
            if not (ROOT / path.lstrip("/")).exists():
                problems.append(f"{name}: missing absolute URL https://bautiavila.com{path}")

    for problem in problems:
        print(f"FAIL  {problem}")

    print(f"{len(pages)} pages checked")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
