#!/usr/bin/env bash
# Build the change-marked PDF for revision N (D-2026-09-20-11). Run from paper/:
#   ./make-marked.sh 3 smpt
# The journal suffix defaults to trb and names the manuscript file (D-2026-09-20-14).
# Revisions 1 and 2 predate the split: one manuscript, unsuffixed names, kept as built.
set -euo pipefail

N="${1:?usage: make-marked.sh <revision-number> [journal]}"
J="${2:-trb}"

if [ "$N" -le 2 ]; then
    # Revisions 1 and 2 ran on the single unsuffixed manuscript, which no longer
    # exists in the working tree, so their exit states come from git.
    OUT="revision-${N}-marked"
    if [ "$N" = "1" ]; then
        BASE="$(mktemp)"
        git show 9f37dd2:paper/paper-odca-des.tex > "$BASE"
        NEW="paper-odca-des-prerevision-2.tex"   # the manuscript as revision 1 left it
    else
        BASE="paper-odca-des-prerevision-${N}.tex"
        NEW="$(mktemp)"
        git show d4ee424:paper/paper-odca-des.tex > "$NEW"
    fi
else
    NEW="paper-odca-des_${J}.tex"
    OUT="revision-${N}-${J}-marked"
    BASE="paper-odca-des_${J}-prerevision-${N}.tex"
    # The machine-readable record beside the marked pair: a unified diff of the
    # baseline against the manuscript as it stands now. Rebuilt every time, so a
    # late edit to the revision (a humanizer pass, D-2026-09-22-1) cannot leave it stale.
    diff -u "$BASE" "$NEW" > "revision-${N}-${J}.diff" || true
fi

# --exclude-textcmd="textbf": without it latexdiff descends into a \textbf{...}
# argument and splits its braces across the added and deleted blocks.
latexdiff --exclude-textcmd="textbf" "$BASE" "$NEW" > "${OUT}.tex" 2>/dev/null

# A revised table prints the old and the new value in one cell, so it outgrows the
# text block and the last column is clipped at the page edge. Shrink tables to fit;
# this touches the marked build only, never the manuscript.
python3 - "${OUT}.tex" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
block = r"""
% Marked build only: a revised table carries old and new in one cell, so shrink it to fit.
\usepackage{adjustbox}
\let\ODCAtabular\tabular
\let\endODCAtabular\endtabular
\renewenvironment{tabular}[2][c]{%
  \begin{adjustbox}{max width=\textwidth}\ODCAtabular[#1]{#2}%
}{%
  \endODCAtabular\end{adjustbox}%
}
% A deleted inline formula is one unbreakable box inside \sout and runs off the
% page; let TeX break inline math at relations and binary operators instead.
\relpenalty=0
\binoppenalty=0
\setlength{\emergencystretch}{6em}
% latexdiff wraps a citation inside added text in an \mbox, which can leave one
% line a few points long. Loosen interword spacing for the marked build only.
\sloppy
% The marked builds cite their own bibliography: references.bib plus the entries
% later revisions dropped, so the struck-through deleted text still resolves.
"""
s = s.replace(r"\begin{document}", block + "\n" + r"\begin{document}", 1)
s = s.replace(r"\bibliography{references}", r"\bibliography{references-marked}", 1)
open(p, "w").write(s)
PY

pdflatex -interaction=nonstopmode "$OUT" > /dev/null
bibtex "$OUT" > /dev/null
pdflatex -interaction=nonstopmode "$OUT" > /dev/null
pdflatex -interaction=nonstopmode "$OUT" > /dev/null

printf '%s: %s pages, %s errors, %s undefined, %s overfull box(es) over 10pt\n' \
    "$OUT" \
    "$(pdfinfo "${OUT}.pdf" | awk '/Pages/{print $2}')" \
    "$(grep -c '^!' "${OUT}.log" || true)" \
    "$(grep -ci 'undefined' "${OUT}.log" || true)" \
    "$(grep -oE 'Overfull .hbox \([0-9.]+pt' "${OUT}.log" | grep -oE '[0-9.]+' | awk '$1>10' | wc -l)"
