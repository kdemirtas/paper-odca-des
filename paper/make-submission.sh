#!/bin/bash
# The LaTeX source package for one journal's submission system: the manuscript with figure paths
# made flat (Editorial Manager puts every uploaded file in one folder), the figures it includes,
# the class, the bibliography style, references.bib and the .bbl, and the Highlights file. The
# package is compiled on its own in a clean folder and held to the manuscript's gate before the
# zip is written.
#   ./make-submission.sh <journal>      (smpt, trb or treng)
# Writes submission_<journal>/ and submission_<journal>.zip next to this script.
set -euo pipefail
cd "$(dirname "$0")"

journal=${1:?usage: make-submission.sh <journal>}
src=paper-odca-des_${journal}.tex
[ -f "$src" ] || { echo "no $src"; exit 1; }
out=submission_${journal}
rm -rf "$out" "$out.zip"
mkdir -p "$out"

sed 's#{\.\./figures/#{#g' "$src" > "$out/$src"
grep -o '\\includegraphics\[[^]]*\]{[^}]*}' "$out/$src" | sed 's/.*{\(.*\)}/\1/' | sort -u |
    while read -r figure; do cp "../figures/$figure" "$out/"; done
style=$(sed -n 's/^\\bibliographystyle{\(.*\)}/\1/p' "$src")
cp elsarticle.cls "$style.bst" references.bib "$out/"
[ -f "highlights_${journal}.txt" ] && cp "highlights_${journal}.txt" "$out/"

stem=${src%.tex}
(
    cd "$out"
    pdflatex -interaction=nonstopmode "$stem" >/dev/null || true
    bibtex "$stem" >/dev/null
    pdflatex -interaction=nonstopmode "$stem" >/dev/null || true
    pdflatex -interaction=nonstopmode "$stem" >/dev/null || true
)
log=$out/$stem.log
errors=$(grep -c '^!' "$log" || true)
undefined=$(grep -c 'undefined' "$log" || true)
missing=$(grep -c 'File .* not found' "$log" || true)
overfull=$({ grep 'Overfull \\hbox' "$log" || true; } | awk -F'[()]' '{split($2, a, "pt"); if (a[1] + 0 > 10) n++} END {print n + 0}')
pages=$(pdfinfo "$out/$stem.pdf" | awk '/^Pages/ {print $2}')
echo "$out: $pages pages, $errors errors, $undefined undefined, $missing missing files, $overfull overfull box(es) over 10pt"
if [ "$errors" -ne 0 ] || [ "$undefined" -ne 0 ] || [ "$missing" -ne 0 ] || [ "$overfull" -ne 0 ]; then
    echo "FAILED: the package does not compile clean on its own"; exit 1
fi

# the .bbl stays in the package so the system need not run BibTeX; the build products go
rm -f "$out"/*.aux "$out"/*.log "$out"/*.out "$out"/*.blg "$out"/*.spl
(cd "$out" && zip -q -r "../$out.zip" .)
echo "$out.zip: $(ls "$out" | wc -l) files"
