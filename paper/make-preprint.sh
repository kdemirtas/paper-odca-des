#!/bin/bash
# The preprint (Zenodo) version of the manuscript: the same text, set single-spaced and without
# the "Preprint submitted to <journal>" footer. preprint/paper-odca-des.pdf is the file to upload
# to the Zenodo record. It is built from a flat self-contained source tree (the .tex, the .bbl,
# the class, the bibliography style and the figures it includes), kept in preprint/source/ and
# packed as preprint/paper-odca-des.tar.gz for a server that builds from source.
#   ./make-preprint.sh
# Writes preprint/paper-odca-des.pdf (tracked) and, beside it and gitignored, preprint/source/
# and preprint/paper-odca-des.tar.gz.
set -euo pipefail
cd "$(dirname "$0")"

src=paper-odca-des_smpt.tex
stem=paper-odca-des
out=preprint/source
rm -rf "$out" "preprint/$stem.tar.gz"
mkdir -p "$out"

grep -q '^\\documentclass\[review,number\]{elsarticle}' "$src" || { echo "class line moved"; exit 1; }
sed -e 's#^\\documentclass\[review,number\]{elsarticle}#\\documentclass[preprint,number,nopreprintline]{elsarticle}#' \
    -e 's#{\.\./figures/#{#g' "$src" > "$out/$stem.tex"
grep -o '\\includegraphics\[[^]]*\]{[^}]*}' "$out/$stem.tex" | sed 's/.*{\(.*\)}/\1/' | sort -u |
    while read -r figure; do cp "../figures/$figure" "$out/"; done
style=$(sed -n 's/^\\bibliographystyle{\(.*\)}/\1/p' "$src")
cp elsarticle.cls "$style.bst" references.bib "$out/"

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
echo "preprint: $pages pages, $errors errors, $undefined undefined, $missing missing files, $overfull overfull box(es) over 10pt"
if [ "$errors" -ne 0 ] || [ "$undefined" -ne 0 ] || [ "$missing" -ne 0 ] || [ "$overfull" -ne 0 ]; then
    echo "FAILED: the preprint does not compile clean on its own"; exit 1
fi

cp "$out/$stem.pdf" "preprint/$stem.pdf"
echo "preprint/$stem.pdf: the file for the Zenodo record"

# a source build reads the .bbl; references.bib and the build products stay out of the archive
rm -f "$out"/*.aux "$out"/*.log "$out"/*.out "$out"/*.blg "$out"/*.spl "$out/references.bib"
tar czf "preprint/$stem.tar.gz" -C "$out" --exclude="$stem.pdf" .
echo "preprint/$stem.tar.gz: $(tar tzf "preprint/$stem.tar.gz" | grep -vc '/$') files"
