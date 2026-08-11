#!/usr/bin/env python3
"""One-time migration: lectures/lecture_NN.tex  ->  lectures/bodies/lecture_NN.tex

Strips the per-lecture preamble (now shared in lectures/preamble.tex) and
converts the ad-hoc presentation markup into real, numbered, referenceable
environments:

  \\begin{defbox}\\textbf{Дефиниция (X):} ...   ->  \\begin{defn}[X] ...
  \\begin{thmbox}\\textbf{Твърдение:} ...       ->  \\begin{prop} ...
  \\textbf{Доказателство:} ...                 ->  \\begin{proof} ... \\end{proof}

plus text normalisations that were inconsistent across the 15 files:
straight quotes -> Bulgarian „ “, math decimal commas -> 0{,}95, ь/ъ typos.

After this runs, lectures/bodies/ is the source of truth and is hand-edited;
this script is not part of the regular build.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEC = os.path.join(ROOT, "lectures")
OUT = os.path.join(LEC, "bodies")

# label -> (environment, explicit name override or None)
LABEL_ENV = {
    "Дефиниция": "defn",
    "Теорема": "thm",
    "Твърдение": "prop",
    "Лема": "lem",
    "Следствие": "cor",
}

# Labels that don't fit the "Label (Name):" shape, or that were filed under the
# wrong colour. Keyed by the exact \textbf{...} content.
OVERRIDE = {
    "Дефиниция за две случайни величини:": ("defn", "независимост на две случайни величини"),
    "Дефиниция за независимост в съвкупност:": ("defn", "независимост в съвкупност"),
    "Дефиниция на модела:": ("defn", "хипергеометричен модел"),
    # was in a blue defbox, but it is a theorem
    "Дефиниция / Теорема (Усилен ЗГЧ):": ("thm", "Усилен закон за големите числа"),
}

BOX_RE = re.compile(
    r"\\begin\{(?:defbox|thmbox)\}\s*\n?\s*"
    r"\\textbf\{([^}]*(?:\{[^}]*\}[^}]*)*)\}\s*"
    r"(.*?)"
    r"\\end\{(?:defbox|thmbox)\}",
    re.DOTALL,
)


def convert_boxes(body, report):
    def repl(m):
        label, inner = m.group(1), m.group(2)
        if label in OVERRIDE:
            env, name = OVERRIDE[label]
        else:
            mm = re.match(r"^(\S+?)\s*(?:\(([^)]*(?:\{[^}]*\}[^)]*)*)\))?\s*:?\s*$", label)
            if not mm or mm.group(1) not in LABEL_ENV:
                report.append("UNMAPPED BOX LABEL: %r" % label)
                return m.group(0)
            env, name = LABEL_ENV[mm.group(1)], mm.group(2)
        opt = "[%s]" % name if name else ""
        return "\\begin{%s}%s\n%s\n\\end{%s}" % (env, opt, inner.strip(), env)

    return BOX_RE.sub(repl, body)


# A proof runs until the next structural element.
PROOF_START = re.compile(r"^\\textbf\{Доказателство([^}]*)\}:?\s*(.*)$")
PROOF_END = re.compile(
    r"^\s*(?:\\(?:sub)*section\{"
    r"|\\begin\{(?:defn|thm|prop|lem|cor|defbox|thmbox)\}"
    r"|\\textbf\{(?:Пример|Дефиниция|Теорема|Твърдение|Лема|Следствие|Забележка|Доказателство|Задача|Коментар|Извод|Интуиция)"
    r"|\\end\{document\})"
)
QED_TAIL = re.compile(r"\s*(?:\\hfill)?\s*\$\\(?:black)?square\$\s*$")


def convert_proofs(body, report, fname):
    lines = body.split("\n")
    out, i = [], 0
    while i < len(lines):
        m = PROOF_START.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        qualifier = m.group(1).strip().rstrip(":").strip()
        # \textbf{Доказателство (за частен случай)} -> \begin{proof}[Доказателство (за частен случай)]
        opt = "[Доказателство %s]" % qualifier if qualifier else ""
        # find the end
        j = i + 1
        while j < len(lines) and not PROOF_END.match(lines[j]):
            j += 1
        # back off over trailing blank lines
        k = j
        while k > i + 1 and not lines[k - 1].strip():
            k -= 1
        chunk = [m.group(2)] + lines[i + 1:k]
        while chunk and not chunk[0].strip():
            chunk.pop(0)
        # drop a hand-written QED — amsthm supplies it now
        if chunk:
            chunk[-1] = QED_TAIL.sub("", chunk[-1])
            if not chunk[-1].strip():
                chunk.pop()
        report.append("%s: proof %d..%d ends -> %r" % (fname, i + 1, k, chunk[-1][-60:] if chunk else ""))
        out.append("\\begin{proof}%s" % opt)
        out.extend(chunk)
        out.append("\\end{proof}")
        out.extend(lines[k:j])
        i = j
    return "\n".join(out)


def normalise_text(body):
    # Straight "..." -> Bulgarian „ “ (some files already use the correct marks).
    body = re.sub(r'"([^"\n]{1,120}?)"', r"„\1“", body)
    # Decimal comma inside math: 0,95 renders as "0, 95" because TeX treats the
    # comma as punctuation. Brace it. (Leaves genuine lists like N(0,1) alone —
    # those are handled by only matching digit,digit with no space, inside $...$,
    # where the left digit is 0 and the fraction has >=2 digits.)
    def fix_math(m):
        return re.sub(r"(?<![\d{])(\d),(\d\d+)(?![\d}])", r"\1{,}\2", m.group(0))

    body = re.sub(r"\$[^$]*\$", fix_math, body)
    # ь/ъ transcription typos
    body = body.replace("параметьр", "параметър")
    return body


def main():
    # This is a ONE-TIME migration. It reads the old self-contained
    # lectures/lecture_NN.tex, which no longer exist in that form — those files
    # are now thin auto-generated drivers that \input bodies/. Re-running would
    # overwrite the hand-edited bodies with garbage.
    if os.path.isdir(OUT) and "--force" not in sys.argv:
        sys.exit(
            "refusing to run: lectures/bodies/ already exists.\n"
            "This migration has already been applied and bodies/ is now the\n"
            "hand-edited source of truth. Use scripts/build_lectures.py to\n"
            "rebuild. Pass --force only if you really mean to redo the migration."
        )

    os.makedirs(OUT, exist_ok=True)
    report = []
    for n in ["%02d" % i for i in range(1, 16)]:
        src = os.path.join(LEC, "lecture_%s.tex" % n)
        text = open(src, encoding="utf-8").read()
        b = text.find("\\newpage", text.find("\\tableofcontents"))
        e = text.rfind("\\end{document}")
        body = text[b + len("\\newpage"):e].strip("\n")

        body = convert_boxes(body, report)
        body = convert_proofs(body, report, "lecture_%s" % n)
        body = normalise_text(body)

        dst = os.path.join(OUT, "lecture_%s.tex" % n)
        open(dst, "w", encoding="utf-8").write(body.strip("\n") + "\n")
        print("wrote", os.path.relpath(dst, ROOT))

    print("\n--- review ---", file=sys.stderr)
    for r in report:
        print(r, file=sys.stderr)


if __name__ == "__main__":
    main()
