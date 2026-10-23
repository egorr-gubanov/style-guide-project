"""Validate local links and fragments in built HTML; external HTTP is out of scope."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1] / "site"

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])


def main():
    pages = {}
    for path in ROOT.rglob("*.html"):
        parsed = Links()
        parsed.feed(path.read_text(encoding="utf-8"))
        pages[path.resolve()] = parsed
    errors = []
    for page, parsed in pages.items():
        for href in parsed.links:
            u = urlsplit(href)
            if u.scheme or u.netloc or href.startswith("/"):
                continue
            target = (page.parent / unquote(u.path)).resolve() if u.path else page
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                errors.append(f"{page.relative_to(ROOT)}: missing {href}")
            elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
                errors.append(f"{page.relative_to(ROOT)}: missing anchor {href}")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"PASS: local links and fragments in {len(pages)} HTML files")
    return 0

if __name__ == "__main__":
    sys.exit(main())
