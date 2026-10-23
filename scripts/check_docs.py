"""Check rendered Markdown links and informative image descriptions."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import markdown

ROOT = Path(__file__).resolve().parents[1]
GENERIC = {"здесь", "тут", "нажмите здесь", "here", "click here"}
LOCAL_PATH = re.compile(r"^(?:file:|/(?:Users|home|private|tmp)/|[A-Za-z]:[\\/])", re.I)

class Rules(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.anchor = None
        self.label = []
        self.h1_count = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if tag == "a":
            href = attributes.get("href", "")
            if LOCAL_PATH.search(href):
                self.errors.append(f"M02 nonportable link: {href}")
            self.anchor = href
            self.label = []
        if tag == "img" and not attributes.get("alt", "").strip():
            self.errors.append("C01 image requires nonempty alt text")

    def handle_data(self, data):
        if self.anchor is not None:
            self.label.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self.anchor is not None:
            if " ".join("".join(self.label).casefold().split()) in GENERIC:
                self.errors.append("M02 generic link text")
            self.anchor = None


def inspect_text(text):
    parser = Rules()
    parser.feed(markdown.markdown(text, extensions=["tables", "pymdownx.superfences"]))
    if parser.h1_count != 1:
        parser.errors.append(f"M01 expected one H1, found {parser.h1_count}")
    return parser.errors


def main():
    paths = sorted(ROOT.glob("*.md")) + sorted((ROOT / "docs").rglob("*.md"))
    paths += sorted((ROOT / ".github").glob("*.md"))
    errors = []
    for path in paths:
        errors.extend(f"{path.relative_to(ROOT)}: {e}" for e in inspect_text(path.read_text(encoding="utf-8")))
    if errors:
        print("\n".join(errors))
        return 1
    print(f"PASS: style link and alt checks in {len(paths)} Markdown files")
    return 0

if __name__ == "__main__":
    sys.exit(main())
