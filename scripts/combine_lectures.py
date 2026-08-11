#!/usr/bin/env python3
"""SUPERSEDED — do not use for new builds.

This stitched the 15 separately-compiled lecture PDFs together with PyMuPDF.
Because it merged at the *PDF* level rather than the LaTeX level, the result had
15 separate tables of contents, no master TOC, and page numbers that restarted
at 1 in every lecture (15 pages printed "1", 15 printed "2", ...).

The combined document is now a real LaTeX document: lectures/lectures_full.tex,
built by scripts/build_lectures.py. It has one title page, one master table of
contents, continuous pagination, running heads, and book-wide numbering for
every definition and theorem.

Kept only so the old lectures/all_lectures.pdf can be reproduced if needed.

Original docstring: Merge the 15 lecture PDFs into one combined PDF with a
proper bookmark tree: a level-1 bookmark per lecture, each lecture's own section
outline nested under it. Internal hyperlinks are preserved per lecture."""
import re, pymupdf

LEC = "/Users/g8row/Documents/lec2tex/lectures"
TITLES = {
    "01": "Въведение. Случайни експерименти, събития и σ-алгебри",
    "02": "Аксиоми на вероятността. Дискретна и геометрична вероятност",
    "03": "Условна вероятност, независимост и формула на Бейс",
    "04": "Случайни величини. Индикатори и дискретни случайни величини",
    "05": "Функция на разпределение. Математическо очакване и дисперсия",
    "06": "Пораждащи функции и основни дискретни разпределения",
    "07": "Теорема на Поасон. Хипергеометрично разпределение, ковариация и корелация",
    "08": "Условно математическо очакване. Непрекъснати случайни величини",
    "09": "Непрекъснати разпределения. Гама и хи-квадрат разпределение",
    "10": "Видове сходимост. Неравенство на Чебишов и закони за големите числа",
    "11": "Централна гранична теорема и функции на моментите",
    "12": "Точкови оценки. Максимално правдоподобие и метод на моментите",
    "13": "Доверителни интервали и проверка на хипотези",
    "14": "Линейна регресия",
    "15": "Комбинаторика и просто случайно блуждаене",
}

out = pymupdf.open()
toc = []
for n in [f"{i:02d}" for i in range(1, 16)]:
    doc = pymupdf.open(f"{LEC}/lecture_{n}.pdf")
    start = out.page_count            # 0-indexed page where this lecture begins
    out.insert_pdf(doc, links=True, annots=True)   # preserve internal links
    toc.append([1, f"Лекция {int(n)}. {TITLES[n]}", start + 1])
    for lvl, title, page in doc.get_toc():
        toc.append([lvl + 1, title, start + page])   # nest section outline under lecture
    doc.close()

out.set_toc(toc)
out.set_metadata({"title": "Вероятности и Статистика — Лекционни записки",
                  "author": ""})
out.save(f"{LEC}/all_lectures.pdf", garbage=4, deflate=True)
print(f"combined: {out.page_count} pages, {len(toc)} bookmarks -> {LEC}/all_lectures.pdf")
out.close()
