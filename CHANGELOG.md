# CHANGELOG: paper-odca-des
> One line per merged PR, newest version first, written by `/putdown` at merge time from the PR
> title and number. A version is a manuscript state that left Kerem's hands (sent to advisors, a seminar, the journal); the repo merges by direct commit, there are no PRs before 2026-09-19. Unreleased work sits under `## Unreleased (revision 1, waiting for Kerem's review)
- PR #10: Number each revision's baseline and diff (2026-09-20)
- PR #9: Close the wall-time assumption as D-2026-09-20-2 (2026-09-20)
- PR #8: Rerun every experiment and restate the manuscript from the fresh outputs (2026-09-20, closes N11)
- PR #7: Name the seed sets in config.py, write the diagnostics to figures/ (2026-09-20, closes N9, N10)
- PR #6: Run the scripts on SimulationResult, odca.experiment and odca.viewer; add the demo trajectory figure (2026-09-19, closes N5, N6, N7 paper side)
- PR #5: Use the odca-des driver split in the scripts (2026-09-19, closes N4)
- PR #4: Use the odca-des trait sampler in the demand sweep and FD diagnostic (2026-09-19, closes N3)
- PR #3: Load configs from YAML, named OD demand with per-lane ends, incidents as config (2026-09-19)
- PR #2: Switch to the odca-des package, fix paper-side bugs, record restatement workstream (2026-09-19)
- PR #1: Retrofit architecture docs: ARCHITECTURE, DECISIONS, HANDOVER (2026-09-19)
- 2026-05-09 `1b47d05`: drop `tables/`; commit multi-seed runners, scalability and sensitivity scripts, revision 1 manuscript.
- 2026-05-09 `83a5cf4`: standardise project docs, add `review/`.
- 2026-04-19 `c705ccb`: gitignore HANDOFF.md renamed to STATUS.md.

## Seminar version (2026-03-27)
- 2026-03-28 `1587642`: AVs make no discretionary lane changes (D-2026-03-28-1), results rerun, seminar slides.
- 2026-03-26 `e4dc209`: Pygame viewer; zero-speed deadlock fixed with a creep speed (D-2026-03-26-1).
- 2026-03-26 `39cbc65`: incident scenario with a baseline run; paper files renamed.
- 2026-03-25 `e1e2f4c`: repository README.

## Advisor draft (sent 2026-03-14)
- 2026-03-14 `44556f5`, `bd1be28`: combined time-space figure, draft clean-up, Claude files untracked.
- 2026-03-14 `e6133bb`: initial commit.
