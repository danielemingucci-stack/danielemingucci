#!/usr/bin/env python3
"""Controlla i collegamenti del profilo (_data/cv.yml): se qualcuno si è trasferito, e il
vecchio e il nuovo indirizzo lo confermano entrambi, aggiorna l'indirizzo. Nessuna libreria."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "free-linkable-profile", "kit"))
from build import moved_target  # noqa: E402

CV = os.path.join(ROOT, "_data", "cv.yml")
URL = re.compile(r"^(\s+(?:- )?url:\s*)(['\"]?)(.*?)\2\s*$")


def main():
    with open(CV, encoding="utf-8") as f:
        lines = f.read().split("\n")
    inside, changed = False, 0
    for i, line in enumerate(lines):
        if re.match(r"^\S", line):
            inside = line.startswith("collegamenti:")
            continue
        m = URL.match(line) if inside else None
        if not m or not m.group(3).strip():
            continue
        old = m.group(3).strip()
        full = old if re.match(r"^https?://", old, re.I) else "https://" + old
        to = moved_target(full)
        if to and not re.search(r"[\s'\"#]", to):
            lines[i] = "%s%s" % (m.group(1), to)
            changed += 1
            print("Trasloco: %s → %s" % (old, to))
    if changed:
        with open(CV, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    print("%d collegamenti aggiornati." % changed)


if __name__ == "__main__":
    main()
