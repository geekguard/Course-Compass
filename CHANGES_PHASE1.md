# Course Compass — Phase 1 reliability fixes

The existing visual interface was preserved. The CSS, HTML templates, and logo files were not changed.

## Updated files
- `chatbot/parser.py`: avoids classifying a career-goal statement such as “I wanted to become a doctor” as a health interest, while preserving explicitly stated interests in the same sentence.
- `chatbot/chatbot_engine.py`: validates and stores interview answers in the category being asked about; the final additional-information question still accepts multiple information categories.
- `app.py`: validates answers against the current question and prevents a plain “no” from ending the interview before the final additional-information question. Adds a guard for lost in-memory chat state so an answer cannot silently be assigned to the wrong question.
- `static/js/script.js`: prevents duplicate submissions while a message is being processed and restarts safely if the server reports that the chat state was lost. No visual styling was changed.
- `tests/test_regressions.py`: adds regression tests for these behaviours.

## Checks run
- Python compilation: passed.
- 10 regression tests: passed.
- Flask test-client interview flow and `/results` page: passed.
- Confirmed unchanged: `static/css/style.css`, all three HTML templates, and both logo files.

## Important limitation
The app currently keeps chatbot progress in a process-local in-memory dictionary. This phase adds a safety guard against silently using an empty profile after that state is lost; it does not provide seamless recovery across server restarts or multiple Gunicorn workers. Shared persistence can be addressed as a separate, carefully tested phase if needed.
