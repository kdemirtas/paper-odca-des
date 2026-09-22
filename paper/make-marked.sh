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

# A table whose column layout changed between the baseline and now cannot be diffed
# cell by cell: latexdiff splits its header row across the deleted and added blocks and
# pdflatex loops on the misplaced alignment tabs. Tables are paired by the \label{tab:...}
# of their enclosing table environment; a pair whose column specs differ is renamed
# tabularblock in working copies of both files, and latexdiff marks it as one block
# (PICTUREENV: old version commented out, new version shown as added). A table present
# in one file only, or without a label, is left to the ordinary diff. The .diff beside
# the marked pair keeps every cell.
BASE_D="$(mktemp --suffix=.tex)"
NEW_D="$(mktemp --suffix=.tex)"
trap 'rm -f "$BASE_D" "$NEW_D"' EXIT
python3 - "$BASE" "$NEW" "$BASE_D" "$NEW_D" <<'PY'
import re
import sys
base, new, base_out, new_out = sys.argv[1:5]

def tabulars(s):
    """{label: (start, spec_end, spec)} for every tabular whose enclosing table
    environment carries a label; braces in the column spec are balanced."""
    out, i, key = {}, 0, r"\begin{tabular}"
    while True:
        i = s.find(key, i)
        if i < 0:
            return out
        j = i + len(key)
        assert s[j] == "{", "tabular without a column spec"
        depth, k = 0, j
        while True:
            depth += {"{": 1, "}": -1}.get(s[k], 0)
            k += 1
            if depth == 0:
                break
        env_start = s.rfind(r"\begin{table", 0, i)
        env_end = s.find(r"\end{table", k)
        if env_start >= 0 and env_end >= 0:
            label = re.search(r"\\label\{([^}]*)\}", s[env_start:env_end])
            if label:
                out[label.group(1)] = (i, k, s[j:k])
        i = k

def rename(s, positions):
    for start, spec_end, _ in sorted(positions, reverse=True):
        end = s.find(r"\end{tabular}", spec_end)
        s = s[:end] + r"\end{tabularblock}" + s[end + len(r"\end{tabular}"):]
        s = s[:start] + r"\begin{tabularblock}" + s[start + len(r"\begin{tabular}"):]
    return s

b, n = open(base).read(), open(new).read()
tb, tn = tabulars(b), tabulars(n)
paired = sorted(set(tb) & set(tn))
changed = [label for label in paired if tb[label][2] != tn[label][2]]
unpaired = sorted(set(tb) ^ set(tn))
b = rename(b, [tb[label] for label in changed])
n = rename(n, [tn[label] for label in changed])
print(f"  tables: {len(paired)} paired by label, {len(changed)} with a changed column layout "
      f"marked as a block{' (' + ', '.join(changed) + ')' if changed else ''}, "
      f"{len(unpaired)} in one file only{' (' + ', '.join(unpaired) + ')' if unpaired else ''}")
open(base_out, "w").write(b)
open(new_out, "w").write(n)
PY
# --exclude-textcmd="textbf": without it latexdiff descends into a \textbf{...}
# argument and splits its braces across the added and deleted blocks.
latexdiff --exclude-textcmd="textbf" \
    --config "PICTUREENV=(?:picture|DIFnomarkup|tabularblock)[\w\d*@]*" \
    "$BASE_D" "$NEW_D" > "${OUT}.tex" 2>/dev/null

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
% A table whose column layout changed is marked as one block (see the latexdiff call).
\newenvironment{tabularblock}[1]{\begin{tabular}{#1}}{\end{tabular}}
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

# A marked build that pdflatex cannot finish (a table it cannot typeset) loops instead
# of failing; the timeout turns that into a failure the caller sees.
timeout 600 pdflatex -interaction=nonstopmode "$OUT" > /dev/null
bibtex "$OUT" > /dev/null
timeout 600 pdflatex -interaction=nonstopmode "$OUT" > /dev/null
timeout 600 pdflatex -interaction=nonstopmode "$OUT" > /dev/null

printf '%s: %s pages, %s errors, %s undefined, %s overfull box(es) over 10pt\n' \
    "$OUT" \
    "$(pdfinfo "${OUT}.pdf" | awk '/Pages/{print $2}')" \
    "$(grep -c '^!' "${OUT}.log" || true)" \
    "$(grep -ci 'undefined' "${OUT}.log" || true)" \
    "$(grep -oE 'Overfull .hbox \([0-9.]+pt' "${OUT}.log" | grep -oE '[0-9.]+' | awk '$1>10' | wc -l)"
