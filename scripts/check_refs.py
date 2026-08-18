#!/usr/bin/env python3
"""Cross-reference integrity check for the collected book.

Two failure modes here are SILENT — neither produces a "??" in the PDF, so
neither shows up in a normal build:

  * a \\label that never reaches the .aux. Observed with \\label placed
    immediately after \\begin{env}[...] — on the same line or the next one —
    for a theorem environment wrapped by \\tcolorboxenvironment. The statement
    still renders and still numbers correctly (the counter steps; only the
    write is lost), so nothing looks wrong until something tries to \\ref it.
    Moving the \\label a few words into the first sentence fixes it. Nearly
    every label in the book sits in the leading position and is fine, so this
    is not worth linting for statically — whether a given one survives seems to
    depend on how its box breaks across pages, which means an unrelated edit in
    the same chapter can knock one out. Run this check after any substantial
    edit, not just after adding labels.
  * a \\crosslecture{label}{text} pointing at a label that no longer exists.
    In the book \\crosslecture expands to \\hyperref, which quietly prints the
    text with no link rather than erroring.

Run after building. Exits non-zero if either is found.

    python3 scripts/build_lectures.py
    python3 scripts/check_refs.py
"""
import glob
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_lectures import BOOK_PDF  # noqa: E402  (one definition of the name)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEC = os.path.join(ROOT, "lectures")
AUX = os.path.join(LEC, "lectures_full.aux")


def main():
    # Compile to a FIXED POINT. This matters: on a run where the TOC or the
    # label numbering is still settling, tectonic reruns TeX and the .aux left
    # behind can be from a pass that had not yet seen every label. Checking that
    # file reports labels as missing when they are perfectly fine — the tool
    # then lies in the most confusing possible direction.
    def compile_once():
        r = subprocess.run(["tectonic", "-X", "compile", "--keep-intermediates",
                            "lectures_full.tex"], cwd=LEC,
                           capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("build failed:\n" + r.stderr[-2000:])
        return "Rerunning" in r.stderr

    for _ in range(4):
        if not compile_once():
            break
    else:
        print("warning: build did not stabilise; results may be unreliable")
    # One more pass after convergence: the .aux is written during the run, so it
    # can still trail the settled state by a single pass.
    compile_once()
    if not os.path.exists(AUX):
        sys.exit("could not produce lectures_full.aux")

    # This script compiles as well, so it owns the freshest PDF by the time it
    # gets here. Leaving it in lectures/ would strand the root deliverable one
    # edit behind, so move it the same way build_lectures.py does.
    built = os.path.join(LEC, "lectures_full.pdf")
    if os.path.exists(built):
        os.replace(built, BOOK_PDF)

    aux = open(AUX, encoding="utf-8").read()

    labels, refs = {}, {}
    for path in sorted(glob.glob(os.path.join(LEC, "bodies", "*.tex"))):
        name = os.path.basename(path)
        text = open(path, encoding="utf-8").read()
        for lbl in re.findall(r"\\label\{([^}]*)\}", text):
            labels[lbl] = name
        for ref in re.findall(r"\\(?:ref|crosslecture)\{([^}]*)\}", text):
            refs.setdefault(ref, name)

    unregistered = sorted(l for l in labels if ("newlabel{%s}" % l) not in aux)
    dangling = sorted(r for r in refs if r not in labels)

    print("labels: %d   references: %d" % (len(labels), len(refs)))
    ok = True

    if unregistered:
        ok = False
        print("\nLABELS THAT NEVER REACH THE AUX "
              "(usually \\label on the same line as \\begin{...}):")
        for l in unregistered:
            print("   %-32s %s" % (l, labels[l]))

    if dangling:
        ok = False
        print("\nREFERENCES TO LABELS THAT DO NOT EXIST:")
        for r in dangling:
            print("   %-32s referenced from %s" % (r, refs[r]))

    if ok:
        print("all labels register; no dangling references")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
