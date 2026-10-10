# Course Compass

Course Compass is a rules-based chatbot that gathers a student's interests, favourite subjects, skills, personality traits, career goals and JAMB score, then compares that profile with the programme data in `data/courses.py`.

## Run locally on Windows / PyCharm

1. Open the folder containing `app.py` and `requirements.txt` in PyCharm.
2. Choose a project Python interpreter. A new virtual environment is recommended.
3. Open **View → Tool Windows → Terminal**.
4. Install the web application's dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Start the app:

   ```powershell
   python app.py
   ```

6. Open the local address printed in the terminal, usually `http://127.0.0.1:5000`.

If PowerShell reports that the wrong Python is being used, run the install command with the exact interpreter path selected in **File → Settings → Project → Python Interpreter**, for example:

```powershell
& ".\.venv3\Scripts\python.exe" -m pip install -r requirements.txt
& ".\.venv3\Scripts\python.exe" app.py
```

## Run regression tests

With the project dependencies installed, run:

```powershell
python -m unittest discover -s tests -v
```

The tests cover interview category separation, common parsing edge cases, additional information, recommendation matching, server-side session persistence, request validation and HTML escaping.

## Session and security notes

- Conversation history and chatbot progress are stored in a local SQLite database under `instance/`, not in the browser cookie. This lets the app restore progress between requests and app-process restarts.
- `instance/` is runtime data and should not be committed or shared between unrelated users.
- Set `COURSE_COMPASS_SECRET_KEY` to a long random value for a deployed environment. The local fallback is generated at startup for development.
- If the deployed site uses HTTPS, set `COURSE_COMPASS_HTTPS=1` so the session cookie is marked secure.
- Debug mode is off by default. Set `FLASK_DEBUG=1` only during local development.
- For a production deployment, use a production WSGI server and configure HTTPS, backups and the database path appropriately.

## Important data limitation

The recommendation rules are explainable, but their quality depends on the accuracy of `data/courses.py`. Course names, degree awards, programme duration, JAMB cut-offs and UTME subject combinations must be checked against current ATBU and JAMB IBASS information before the app is used as an official admissions guide. The interface already advises students to verify current JAMB requirements; do not describe the stored cut-offs as guaranteed admission cut-offs. See `DATA_AUDIT_NOTES.md` for the latest catalogue review and sources.

## Keyword parser evaluation

Course Compass includes a small synthetic evaluation set for its rules-based parser.
Run these commands from the project root after installing the requirements:

```powershell
python evaluation/run_evaluation.py
python -m unittest tests.test_keyword_evaluation -v
```

Read `EVALUATION_GUIDE.md` for the software-only evaluation method. It uses automated tests and synthetic labelled cases; it does not require real student participants. The synthetic score is not a claim of perfect real-world understanding.

## Quality assurance helper

On Windows, after installing the dependencies, run the complete automated checks from PowerShell:

```powershell
.\scripts\run_quality_checks.ps1
```

The script writes the test output to `quality_check_results.txt`. Review this output before reporting results in your documentation.
