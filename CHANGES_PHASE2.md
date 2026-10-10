# Course Compass — Phase 2 reliability review

## Conversation and state reliability

- Replaced the process-local chatbot dictionary and client-side transcript storage with SQLite-backed server-side sessions.
- Saved chatbot progress and profile data between requests, so the app can restore a conversation after a process restart or when another worker handles the next request.
- Added bounded restoration checks for saved profile fields and question index.
- Kept a safeguard that refuses to process a message if saved interview state is missing, rather than assigning the answer to the wrong question.
- Limited stored transcript history to the latest 100 messages per session.

## Parsing and recommendation logic

- Improved common negation handling so statements such as "I am not interested in medicine" and "I do not like business" do not create positive interests.
- Prevented personality descriptions such as "I am creative and patient" from automatically becoming interests.
- Cached and sorted the keyword vocabulary for repeat parsing efficiency and made fuzzy spelling correction more conservative for common words.
- Added teacher/engineer/scientist/analyst category matching to specific career titles without making a human-doctor goal match veterinary-doctor careers.
- Avoided returning arbitrary zero-match programmes or recommendations based only on a JAMB score.
- Made profile completeness rise gradually when additional distinct items are added, while keeping it capped at 100. The score represents profile completeness, not the probability that a recommendation is correct.
- Rejected out-of-range JAMB scores instead of converting a score above 400 into 400; zero remains the internal marker for “no score provided”.
- Accepted a bare valid JAMB score during the final additional-information step.
- Kept the profile-completeness score current immediately after the name answer.
- Made recommendation sorting deterministic when scores tie.
- Updated the displayed Agriculture faculty label to the full name used in the project's ATBU faculty list.

## Web security and request handling

- Removed the hard-coded Flask secret key; the app reads `COURSE_COMPASS_SECRET_KEY` or creates a random development fallback.
- Added HttpOnly and SameSite cookie settings, plus an opt-in secure-cookie setting for HTTPS deployments.
- Disabled Flask debug mode by default.
- Added request-size and message-length limits and validation for non-text or malformed message payloads.
- Kept detailed exception information in server logs instead of returning it to the browser.
- Fixed unsafe HTML rendering in the chat transcript. User text is escaped by the template; CSS preserves line breaks without marking the text as trusted HTML.
- Kept UTME/JAMB subject combinations visible even when a student has entered a JAMB score.

## GUI preservation

No layout, colour, font, button, chat-bubble style, page structure or logo redesign was made. The CSS change only preserves message line breaks after removing unsafe HTML rendering. The results-template change ensures the existing subject-combination section is not hidden for students who already entered a score. The existing JavaScript, landing-page template and logo assets are unchanged.

## Verification

- Python compilation: passed.
- Regression tests: **23 passed**.
- Covered career/interest separation, negative statements, spelling correction, teacher career matches, confidence increases, invalid JAMB scores, no-match results, full interview flow, session restoration through a separate app instance, request validation and HTML escaping.

## Remaining data-quality limitation

The programme data is preserved rather than guessed at. See `DATA_AUDIT_NOTES.md` for the programme-name, duration, cut-off and subject-combination details that still need verification against current ATBU/JAMB sources before the application is presented as an official admissions guide.
