"""Run the same documentation checks locally and in CI."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
markdown_files = sorted(str(p.relative_to(ROOT)) for p in ROOT.glob("*.md"))
markdown_files += sorted(str(p.relative_to(ROOT)) for p in (ROOT / "docs").rglob("*.md"))
markdown_files += sorted(str(p.relative_to(ROOT)) for p in (ROOT / ".github").glob("*.md"))
commands = [
    [sys.executable, "-m", "pymarkdown", "--config", ".pymarkdown.json", "scan", *markdown_files],
    [sys.executable, "scripts/check_docs.py"],
    [sys.executable, "-m", "mkdocs", "build", "--strict"],
    [sys.executable, "scripts/check_site.py"],
]
for command in commands:
    print("RUN", " ".join(command[1:3]), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)
print("PASS: Markdown, style rules, strict MkDocs build and local HTML links", flush=True)
