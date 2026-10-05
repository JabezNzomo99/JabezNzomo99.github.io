#!/usr/bin/env python3
"""
Tiny dependency-free BibTeX -> data/publications.js helper.

It intentionally handles a simple subset of BibTeX suitable for a personal site.
For advanced BibTeX, replace this parser with pybtex/bibtexparser.
"""

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "publications.bib"
OUT = ROOT / "data" / "publications.generated.js"

text = BIB.read_text(encoding="utf-8")

entries = []
for m in re.finditer(r"@(\w+)\s*\{\s*([^,]+),(.*?)\n\}", text, flags=re.S):
    kind, key, body = m.groups()
    fields = {}
    for fm in re.finditer(r"(\w+)\s*=\s*\{(.*?)\}\s*,?", body, flags=re.S):
        field, value = fm.groups()
        fields[field.lower()] = re.sub(r"\s+", " ", value).strip()

    entries.append({
        "id": key.strip(),
        "year": fields.get("year", ""),
        "title": fields.get("title", ""),
        "authors": fields.get("author", "").replace(" and ", ", "),
        "venue": fields.get("booktitle", fields.get("journal", fields.get("note", ""))),
        "selected": False,
        "summary": "",
        "thumbnail": "",
        "badge": "",
        "links": []
    })

OUT.write_text(
    "window.PUBLICATIONS = " + json.dumps(entries, indent=2, ensure_ascii=False) + ";\n",
    encoding="utf-8"
)
print(f"Wrote {OUT.relative_to(ROOT)} with {len(entries)} entries.")
