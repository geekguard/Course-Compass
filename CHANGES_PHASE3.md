# Course Compass — Phase 3 reliability and evaluation refinements

## GUI preservation

No HTML templates, CSS, JavaScript, logo assets, page layouts, colours, fonts, buttons or chat-bubble styling were changed in this phase.

## Code and data refinements

- Avoided classifying website-building interest as engineering solely because the phrase contained the generic word `building`.
- Added website-related technology phrases and common problem-solving/data-analysis skill wording.
- Prevented `writing code` from automatically being classified as a communication skill unless the answer also contains a separate communication signal.
- Removed the redundant generic `engineer` career tag when the same answer already matches the more specific `software engineer` goal.
- Normalized restored profile lists and removed duplicates from saved session state.
- Allowed an unknown programme-specific JAMB cut-off to be represented as `None`. The recommender does not award a JAMB-score bonus or claim a threshold is met when the cut-off is unknown.
- Consolidated Clinical Sciences specialty/department records into a single Medicine and Surgery (MBBS) undergraduate recommendation.
- Excluded Urban & Regional Planning from the recommendation catalogue in line with the project's scope instruction. This is not a claim that ATBU lacks a department by that name.
- Added 15 quality-assurance tests and expanded the synthetic labelled parser benchmark from 41 to 61 cases.

## Verification results

- Full automated suite: **56 passed, 0 failed**.
- Synthetic labelled parser benchmark: **61/61 exact category matches**.
- Synthetic benchmark micro precision, recall and F1: **100% each**.
- Python compilation: passed.
- UI assets/templates/CSS/JavaScript: unchanged compared with the preceding optimized project archive.

The metrics apply to the included test cases only. They do not guarantee that every possible input will be parsed correctly or that every programme detail is current. See `TESTING_AND_EVALUATION_REPORT.md` and `DATA_AUDIT_NOTES.md`.
