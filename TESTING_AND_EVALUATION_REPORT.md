# Course Compass — Software Testing and Evaluation Report

**Project:** ATBU Course Recommendation Chatbot System (Course Compass)  
**Evaluation date:** 10 October 2026  
**Evaluation type:** Software-only testing using automated, synthetic and black-box test methods  
**Human participants:** None. No real-student testing was performed or required for this evaluation.

## 1. Purpose

This evaluation examines whether Course Compass's rules-based parser, student profile, recommendation engine and Flask web flow behave according to their specified rules. It focuses on functional correctness, common input edge cases, saved-session handling, recommendation output constraints and regression protection. It does not claim to measure student satisfaction or establish that every recommendation is objectively suitable.

## 2. Test methods

- **Unit tests:** test parsing, category separation, profile updates, score handling, course matching and recommendation scoring.
- **Integration tests:** execute a synthetic interview through the chatbot engine and confirm that profile categories remain separate and recommendations can be generated.
- **System/black-box tests:** use Flask's test client to exercise HTTP routes, session persistence, malformed input handling, results flow and HTML escaping without opening a browser or involving real users.
- **Regression tests:** preserve known fixes and rerun them after changes.
- **Synthetic labelled benchmark:** compare predicted parser categories against manually labelled expected categories across 61 authored examples.
- **Boundary and invalid-input tests:** cover out-of-range JAMB scores, empty/non-text/oversized messages, malformed session data, unknown cut-offs and no-match profiles.

## 3. Test environment

The automated checks ran under Python 3.13.5 with Flask 3.1.3 and Werkzeug 3.1.8 available to the test runner. The project `requirements.txt` pins Flask 3.1.0 and Gunicorn 23.0.0; rerunning in the final Windows/PyCharm virtual environment remains advisable because the test runner's Flask patch version differs from the pinned version.

Reproduce from the project root on Windows:

```powershell
& ".\.venv\Scripts\python.exe" -m unittest discover -s tests -v
& ".\.venv\Scripts\python.exe" evaluation\run_evaluation.py
& ".\.venv\Scripts\python.exe" -m compileall -q app.py chatbot data models tests evaluation server_session.py
```

Alternatively, run `scripts/run_quality_checks.ps1`; the script writes its console output to `quality_check_results.txt`.

## 4. Results summary

| Check | Result | Interpretation |
|---|---:|---|
| Full automated suite | **56 passed, 0 failed** | All 56 unit, integration, system-route and regression tests in the included suite passed in the recorded run. |
| Parser synthetic benchmark | **61/61 exact matches (100%)** | Every example in the authored benchmark matched its expected category set. |
| Micro-precision | **100%** | No extra category labels were produced on the benchmark. |
| Micro-recall | **100%** | All expected category labels in the benchmark were recovered. |
| Micro-F1 | **100%** | Precision and recall were both 100% on the benchmark. |
| Python compilation | **Passed** | No compilation errors were reported for the checked source folders/files. |
| GUI asset comparison | **Unchanged** | CSS, JavaScript, HTML templates and logo assets match the preceding optimized archive byte-for-byte. |

The 100% benchmark result applies only to the 61 manually authored cases. The benchmark is small and not a random sample of all possible student wording. It must not be described as 100% real-world accuracy.

## 5. Test coverage by area

| Area | Tests | Result examples |
|---|---:|---|
| Keyword/parser regression | 11 | Interest/category separation, farmer career phrasing, negation, spelling variants and full synthetic interview. |
| Existing parser/profile/web regression suite | 23 | Profile updates, JAMB score boundaries, full interview, SQLite-backed session restoration, request validation and HTML escaping. |
| Additional quality assurance | 22 | Website vs engineering classification, skills overlap, recommendation score range/order, unknown cut-off behaviour, catalogue structure and Flask route checks. |
| **Total** | **56** | **All passed.** |

## 6. Representative black-box/system cases

| ID | Input/action | Expected result | Recorded result |
|---|---|---|---|
| ST01 | Open home route | Page returns HTTP 200 | PASS |
| ST02 | Start a session and open chat | Chat page renders with first prompt | PASS |
| ST03 | Submit economics, agriculture and social studies | Expected categories are separated; health is not added without evidence | PASS |
| ST04 | State “I want to become a farmer” | Farmer career goal is extracted and relevant agriculture programmes can match | PASS |
| ST05 | Enter “I am interested in building websites” | Technology is identified without a false engineering category | PASS |
| ST06 | Enter “I am good at writing code” as skills | Coding is identified without automatically adding communication | PASS |
| ST07 | Submit empty, non-text or oversized message | Request is rejected with a suitable client error | PASS |
| ST08 | Submit HTML/script text as a chat message | User content is escaped rather than rendered as trusted HTML | PASS |
| ST09 | Restore malformed session data | Lists are normalized, duplicate entries removed and question index bounded | PASS |
| ST10 | Use a JAMB score without profile matches | No arbitrary recommendations are generated | PASS |
| ST11 | Check recommendation scores and ordering | Scores remain within 0–100 and sorting is deterministic | PASS |
| ST12 | Use Medicine and Surgery with an unknown stored cut-off | No cut-off bonus is added and the explanation advises verification | PASS |

These results come from automated tests/test-client checks, not from real student sessions.

## 7. Recommendation and course-data safeguards

- The recommendation engine only returns courses with at least one profile-based match; a JAMB score alone is insufficient.
- Recommendation scores are bounded to 0–100 and results are sorted deterministically by score, then course name.
- The Medicine and Surgery programme is represented as one undergraduate programme rather than separate recommendations for Clinical Sciences departments such as Surgery or Internal Medicine.
- Medicine and Surgery's JAMB cut-off is stored as unknown, so the system does not award a cut-off bonus or state that an unverified threshold has been met.
- Urban & Regional Planning is excluded from this project's recommendation catalogue in accordance with the specified project scope. ATBU's official website lists a department by that name, so this exclusion is a scope decision, not a claim that the department does not exist.
- Other stored programme degree awards, durations, UTME subject combinations and numeric reference cut-offs require programme-by-programme verification before the application is used as official admissions guidance.

## 8. Metrics

- **Automated test pass rate:** passed test cases ÷ executed test cases × 100 = 56 ÷ 56 × 100 = **100%** for the included suite in this run.
- **Exact category-match rate:** exact matches ÷ labelled examples × 100 = 61 ÷ 61 × 100 = **100%** for this synthetic benchmark.
- **Precision:** TP ÷ (TP + FP).
- **Recall:** TP ÷ (TP + FN).
- **F1:** 2 × precision × recall ÷ (precision + recall), when defined.

TP means true positive, FP means false positive, and FN means false negative. The parser metrics are calculated only from the benchmark examples and should not be conflated with recommendation usefulness.

## 9. Limitations and remaining checks

1. The synthetic benchmark is manually authored and limited to 61 cases; it cannot represent all natural-language input.
2. Rule-based keyword matching can miss ambiguous phrases, unfamiliar spelling and local expressions.
3. The exact pinned Flask 3.1.0 environment should be rerun in the user's Windows/PyCharm virtual environment before final hand-in.
4. Programme-level degree awards, durations, subject combinations and numeric JAMB reference cut-offs need current source verification. The stored values are not guarantees of admission.
5. No real-student usability or satisfaction claim is made because no participants were involved. This report intentionally uses a software-only evaluation method.

## 10. Conclusion

The latest recorded software-only run passed all 56 included automated tests, achieved 61/61 exact category matches on the synthetic benchmark and passed Python compilation. The existing GUI assets were preserved. These results provide repeatable evidence that the tested behaviours work as expected within the included test scope. They do not guarantee that every external-supervisor test or every possible student input will pass, and they do not replace verification of current ATBU/JAMB programme data.

## 11. Sources for catalogue review

- ATBU official faculties and departments: https://atbu.edu.ng/sitemap/ and https://atbu.edu.ng/faculties-and-colleges/
- ATBU recruitment page listing Clinical Sciences departments: https://recruitment.atbu.edu.ng/adverts
- National Universities Commission accreditation report for ATBU's Medicine & Surgery programme: https://www.nuc.edu.ng/accreditation-tech-report-view/entry/16055/
- JAMB Integrated Brochure and Syllabus System: https://ibass.jamb.gov.ng/brochure-by-programme
