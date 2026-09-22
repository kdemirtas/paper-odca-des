# Humanizer report 02 (scoped)

Date: 2026-09-22
Scope: scoped second pass, not a full-manuscript scan. Covers only the three declaration
sections inserted before `% References` since report 01: CRediT authorship contribution
statement, Declaration of competing interest, Data availability.
Files read: `paper/paper-odca-des_trb.tex` (lines 1361-1369), `paper/paper-odca-des_smpt.tex`
(lines 1365-1373). Text is identical in both files.
Follows: critic round 9 (`review/self/critic_report_09.md`,
`review/self/critic_author_response_09.md`).
Revision: 3 (reopened).
Finding count: Tier A: 0. Tier B: 0. Total: 0.

## Findings

None.

## Section-by-section notes

**CRediT authorship contribution statement**: `Conceptualization, Methodology, Software,
Validation, Formal analysis, Writing (original draft)` for Demirtas, `Supervision, Writing
(review and editing)` for Mirchandani and Zhou. These are terms from the fixed CRediT taxonomy
(Elsevier/NISO), not the authors' free prose. A pattern matcher would treat the flat noun list
as a rule-of-three or synonym-cycling candidate; it is not, because the list is the required
form and each term names a distinct, non-overlapping taxonomy role. Not flagged.

**Declaration of competing interest**: "The authors declare that they have no known competing
financial interests or personal relationships that could have appeared to influence the work
reported in this paper." This is Elsevier's standard boilerplate sentence, required verbatim by
the journal's submission system. Any phrase in it that resembles a tell (e.g. the passive
construction, the hedge "could have appeared to") is the mandated wording, not authored prose,
and is excluded on that basis. Not flagged.

**Data availability**: "The simulator (`odca-des`, MIT licence) and the scripts that produce
every result, table and figure in this paper will be made publicly available at [url] and [url]
on acceptance." Checked for Tier A hits (none), for rule-of-three ("result, table and figure":
three distinct, non-overlapping output types the sentence needs to itemize precisely, not
padding), and for passive voice ("will be made publicly available": methods-register statement
where the actor, the authors, is implied and irrelevant to state). No em-dash, no curly quotes,
no announcement hedge. Not flagged.

## Mechanical checks

- Em-dashes (`—`, `–` as em-dash usage) in the three sections: 0 in both files.
- Curly quotes (`"`, `"`, `'`, `'`) in the three sections: 0 in both files.
- Tier A word list (delve, underscore, showcase, intricate, meticulous, commendable, tapestry,
  realm, pivotal, testament, landscape (figurative), leverage (verb), chatbot residue,
  announcement hedges): 0 hits in the three sections.

## Not flagged

- The CRediT role list's flat, comma-separated structure: required taxonomy form, not a
  rule-of-three pattern.
- The competing-interest sentence's passive construction and hedge: Elsevier's mandated
  standard wording, not the author's discretionary phrasing.
- "will be made publicly available" (passive, actor omitted): standard for a data-availability
  statement, actor is implied and irrelevant to name.
- "every result, table and figure": itemizes three distinct output artifact types the statement
  needs to name individually for the availability claim to be accurate; not synonym cycling or
  padding.

## Conclusion

Nothing to fix in the three declaration sections. The CRediT lines and the competing-interest
sentence are required forms; the data-availability sentence is short, precise, and carries no
excess phrasing. No rewrites proposed.
