# Course Compass — Automated Testing and Evaluation Guide

This evaluation is software-focused and **does not require real student participants**. It uses unit/regression tests, Flask test-client checks, a synthetic labelled parser benchmark, boundary cases and structural checks of the course catalogue.

## Test methods

1. **Unit testing:** check parsing, profile updates, course matching and score calculations individually.
2. **Integration testing:** check that the parser, profile, chatbot engine and recommender work together during a synthetic interview.
3. **System/black-box testing:** use Flask's test client to check the web routes, session restoration, input validation, results flow and HTML escaping without manually recruiting users.
4. **Regression testing:** rerun all tests after code changes to confirm previous behaviours remain correct.
5. **Synthetic benchmark evaluation:** compare extracted categories against a manually labelled set of varied example phrases. The labels are a small controlled benchmark, not a representative sample of real students.
6. **Boundary and invalid-input testing:** check out-of-range JAMB scores, empty/non-text/oversized messages, malformed saved state and unknown cut-offs.

## Run checks on Windows / PyCharm

From the `CourseCompass` project root, with its virtual environment and requirements installed:

```powershell
& ".\.venv\Scripts\python.exe" -m unittest discover -s tests -v
& ".\.venv\Scripts\python.exe" evaluation\run_evaluation.py
& ".\.venv\Scripts\python.exe" -m compileall -q app.py chatbot data models tests evaluation server_session.py
```

A helper script is also included at `scripts/run_quality_checks.ps1`. It runs the same checks and saves the console output to `quality_check_results.txt`.

## Measures

- **Automated test pass rate** = passed test cases ÷ executed test cases × 100.
- **Exact category-match rate** = benchmark examples whose predicted category set exactly equals the expected set ÷ all benchmark examples × 100.
- **Precision** = TP ÷ (TP + FP), where TP is a correct category assignment and FP is an incorrect extra category.
- **Recall** = TP ÷ (TP + FN), where FN is an expected category that was missed.
- **F1 score** = 2 × precision × recall ÷ (precision + recall), when defined.

The report must state the denominator and benchmark size alongside every percentage. The evaluation script reports metrics for the synthetic labelled set only.

## Current result snapshot

The latest recorded run completed **56 automated tests with 0 failures**. The 61-example synthetic benchmark achieved 61/61 exact category matches (100% micro precision, recall and F1 for that benchmark). Python compilation also passed. These results are reproducible checks on the included test set, not a guarantee of perfect behaviour on every possible phrase.

## Limitations

- The synthetic cases are manually authored and limited in number.
- Keyword rules may miss unfamiliar, ambiguous or locally phrased answers.
- The course data needs ongoing verification against current ATBU/JAMB sources, especially reference cut-offs, subject combinations, degree awards and duration.
- This evaluation does not measure real student satisfaction or prove that recommendations are objectively appropriate for every individual.
