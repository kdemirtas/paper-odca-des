#!/usr/bin/env python3
"""Apply the accepted rewrites of a humanizer report to every manuscript file.

Usage, from paper/:
    python3 apply_rewrites.py ../review/self/humanizer_report_01.md          # dry run
    python3 apply_rewrites.py ../review/self/humanizer_report_01.md --write

Only findings whose Status is 'accepted' are applied. A finding is applied only when its old
string occurs exactly once in every file its scope names; any other count refuses that one
finding and leaves the rest alone. Nothing is rewritten by a model here: the new text is the
report's own, character for character.
"""

import argparse
import datetime as dt
import pathlib
import re
import subprocess
import sys

HEADING = re.compile(r"^###\s+(?P<id>[A-Za-z]\d+)\s*\|(?P<rest>.*)$", re.MULTILINE)
STATUS = re.compile(r"^\*\*Status:\*\*\s*(?P<status>\w+)", re.MULTILINE)
SCOPE = re.compile(r"scope:\s*(?P<scope>[\w-]+)")
BLOCK = re.compile(r"^```(?P<kind>old|new)\n(?P<body>.*?)\n?^```$", re.MULTILINE | re.DOTALL)


class Finding:
    def __init__(self, fid, scope, status, old, new):
        self.id, self.scope, self.status = fid, scope, status
        self.old, self.new = old, new
        self.outcome = "pending"

    def __repr__(self):
        return f"{self.id} [{self.scope}] {self.status}"


def parse_report(path):
    text = path.read_text()
    chunks = re.split(r"^(?=###\s)", text, flags=re.MULTILINE)
    findings = []
    for chunk in chunks:
        head = HEADING.match(chunk)
        if not head:
            continue
        status = STATUS.search(chunk)
        scope = SCOPE.search(chunk)
        blocks = {m.group("kind"): m.group("body") for m in BLOCK.finditer(chunk)}
        if "old" not in blocks or "new" not in blocks:
            print(f"  {head.group('id')}: no old/new block pair, skipped", file=sys.stderr)
            continue
        findings.append(Finding(
            head.group("id"),
            scope.group("scope") if scope else "shared",
            status.group("status").lower() if status else "proposed",
            blocks["old"],
            blocks["new"],
        ))
    return findings


def manuscript_files(paper_dir):
    """Every manuscript .tex in paper/: has a documentclass, is not a baseline or marked build."""
    out = []
    for p in sorted(paper_dir.glob("*.tex")):
        if "prerevision" in p.name or "marked" in p.name:
            continue
        if "\\documentclass" in p.read_text()[:4000]:
            out.append(p)
    return out


def targets_for(finding, files):
    if finding.scope == "shared":
        return files
    hit = [p for p in files if p.stem.endswith(finding.scope)]
    return hit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report", type=pathlib.Path)
    ap.add_argument("--write", action="store_true", help="write the files; default is a dry run")
    ap.add_argument("--paper-dir", type=pathlib.Path, default=pathlib.Path(__file__).parent)
    args = ap.parse_args()

    paper_dir = args.paper_dir.resolve()
    files = manuscript_files(paper_dir)
    if not files:
        sys.exit(f"no manuscript .tex found in {paper_dir}")
    print(f"manuscript files: {', '.join(p.name for p in files)}")

    findings = parse_report(args.report.resolve())
    accepted = [f for f in findings if f.status == "accepted"]
    print(f"report: {len(findings)} findings, {len(accepted)} accepted\n")
    if not accepted:
        print("nothing accepted, nothing to do.")
        return 0

    bodies = {p: p.read_text() for p in files}
    refused = []

    for f in accepted:
        targets = targets_for(f, files)
        if not targets:
            f.outcome = f"refused: scope '{f.scope}' matches no manuscript file"
            refused.append(f)
            continue
        counts = {p: bodies[p].count(f.old) for p in targets}
        bad = {p.name: n for p, n in counts.items() if n != 1}
        if bad:
            f.outcome = "refused: old text occurs " + ", ".join(
                f"{n}x in {name}" for name, n in bad.items()) + " (need exactly 1)"
            refused.append(f)
            continue
        for p in targets:
            bodies[p] = bodies[p].replace(f.old, f.new, 1)
        f.outcome = "applied to " + ", ".join(p.name for p in targets)

    for f in accepted:
        mark = "ok " if f.outcome.startswith("applied") else "REFUSED"
        print(f"{mark} {f.id} [{f.scope}] {f.outcome}")

    if not args.write:
        print("\ndry run, nothing written. Re-run with --write.")
        return 1 if refused else 0

    for p in files:
        p.write_text(bodies[p])
    print(f"\nwrote {len(files)} file(s).")

    if len(files) > 1:
        a, b = files[0], files[1]
        diff = subprocess.run(["diff", str(a), str(b)], capture_output=True, text=True)
        hunks = len([ln for ln in diff.stdout.splitlines() if ln and ln[0].isdigit()])
        print(f"divergence check: diff {a.name} {b.name} shows {hunks} hunks")

    stamp = dt.date.today().isoformat()
    with args.report.open("a") as fh:
        fh.write(f"\n\n## Applied {stamp}\n\n")
        for f in accepted:
            fh.write(f"- {f.id}: {f.outcome}\n")
        if len(files) > 1:
            fh.write(f"- divergence check after applying: {hunks} hunks\n")
        fh.write("\nBuild gate and the confirming critic round are not run by this script.\n")
    print(f"appended an Applied section to {args.report.name}")

    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
