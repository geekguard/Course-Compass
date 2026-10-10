from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    g
)

import uuid
import os
import secrets
import re

from chatbot.chatbot_engine import ChatbotEngine
from chatbot.questions import QUESTIONS
from server_session import SQLiteSessionInterface

from chatbot.parser import (
    extract_name,
    extract_interests,
    extract_subjects,
    extract_skills,
    extract_personality,
    extract_career_goals,
    extract_jamb_score,
    extract_all_information
)


app = Flask(__name__)

# Set COURSE_COMPASS_SECRET_KEY in the environment for a stable deployment key.
# A random fallback keeps local development from relying on a hard-coded secret.
app.secret_key = os.environ.get("COURSE_COMPASS_SECRET_KEY") or secrets.token_hex(32)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COURSE_COMPASS_HTTPS", "").lower() in {"1", "true", "yes"},
    MAX_CONTENT_LENGTH=16 * 1024,
)
app.session_interface = SQLiteSessionInterface(
    os.path.join(app.instance_path, "course_compass_sessions.sqlite3")
)

MAX_MESSAGE_LENGTH = 1000
MAX_STORED_MESSAGES = 100


def _profile_list(value):
    """Restore a bounded, normalized list without duplicates or invalid items."""
    if not isinstance(value, list):
        return []

    restored = []
    seen = set()
    for item in value:
        if not isinstance(item, str):
            continue
        normalized = item.strip().lower()
        if normalized and normalized not in seen:
            restored.append(normalized)
            seen.add(normalized)
        if len(restored) >= 100:
            break
    return restored


def _serialize_chatbot(chatbot):
    return {
        "current_question": chatbot.current_question,
        "finished": chatbot.finished,
        "profile": chatbot.profile.to_dict(),
    }


def _restore_chatbot(state):
    """Rebuild the rules-based chatbot from server-side session state."""
    chatbot = ChatbotEngine()
    chatbot.start()

    if not isinstance(state, dict):
        return chatbot

    saved_profile = state.get("profile", {})
    if not isinstance(saved_profile, dict):
        saved_profile = {}

    profile = chatbot.profile
    name = saved_profile.get("name", "")
    profile.name = name.strip() if isinstance(name, str) else ""
    profile.favourite_subjects = _profile_list(saved_profile.get("favourite_subjects"))
    profile.interests = _profile_list(saved_profile.get("interests"))
    profile.hobbies = _profile_list(saved_profile.get("hobbies"))
    profile.skills = _profile_list(saved_profile.get("skills"))
    profile.personality_traits = _profile_list(saved_profile.get("personality_traits"))
    work_style = saved_profile.get("preferred_work_style", "")
    profile.preferred_work_style = work_style if isinstance(work_style, str) else ""
    profile.career_goals = _profile_list(saved_profile.get("career_goals"))
    profile.strengths = _profile_list(saved_profile.get("strengths"))
    profile.weaknesses = _profile_list(saved_profile.get("weaknesses"))

    jamb_score = saved_profile.get("jamb_score", 0)
    if isinstance(jamb_score, int) and 0 <= jamb_score <= 400:
        profile.jamb_score = jamb_score
    profile.calculate_confidence()

    question_index = state.get("current_question", 0)
    if not isinstance(question_index, int):
        question_index = 0
    chatbot.current_question = max(0, min(question_index, len(QUESTIONS)))
    chatbot.finished = bool(state.get("finished", False)) or chatbot.current_question >= len(QUESTIONS)
    return chatbot


@app.after_request
def persist_chatbot_state(response):
    """Save progress after each request that used the chatbot."""
    chatbot = getattr(g, "course_compass_chatbot", None)
    if chatbot is not None and session.get("chat_id"):
        session["chatbot_state"] = _serialize_chatbot(chatbot)
    messages = session.get("messages")
    if isinstance(messages, list) and len(messages) > MAX_STORED_MESSAGES:
        session["messages"] = messages[-MAX_STORED_MESSAGES:]
    return response


def get_chatbot():
    had_existing_chat_id = "chat_id" in session
    if "chat_id" not in session:
        session["chat_id"] = str(uuid.uuid4())

    state = session.get("chatbot_state")
    if isinstance(state, dict):
        chatbot = _restore_chatbot(state)
    else:
        # Never pair an old transcript with a newly reset student profile.
        if had_existing_chat_id:
            session["messages"] = []
        chatbot = ChatbotEngine()
        chatbot.start()

    g.course_compass_chatbot = chatbot
    return chatbot

# ==========================================================
# COMMAND CHECKING
# ==========================================================

def is_skip_command(text):

    text = text.lower().strip()

    commands = [
        "i don't know",
        "i dont know",
        "dont know",
        "don't know",
        "not sure",
        "i'm not sure",
        "im not sure",
        "no idea",
        "i have no idea",
        "skip",
        "skip this",
        "skip question"
    ]

    return text in commands


def is_continue_command(text):

    text = text.lower().strip()

    commands = [
        "continue",
        "next",
        "move on",
        "move on please",
        "go on",
        "next question",
        "continue please"
    ]

    return text in commands


def is_finish_command(text):

    text = text.lower().strip()

    commands = [
        "i'm done",
        "im done",
        "i am done",
        "that's all",
        "thats all",
        "that is all",
        "i'm finished",
        "im finished",
        "i am finished",
        "finish",
        "done",
        "finished",
        "stop",
        "i'm ready",
        "im ready",
        "i am ready"
    ]

    return text in commands


def is_no_command(text):
    text = text.lower().strip()

    commands = [
        "no",
        "nope",
        "nah",
        "nothing",
        "nothing else",
        "no thanks",
        "no thank you",
        "that's all",
        "thats all",
        "that is all",
        "nothing more",
        "nothing else to add",
        "i have nothing else",
        "i don't have anything else",
        "i dont have anything else"
    ]

    return text in commands


def wants_recommendations(text):

    text = re.sub(r"\s+", " ", text.lower().strip())

    # A negative statement must not be mistaken for a request because it
    # contains a phrase such as "want recommendations".
    if re.search(
        r"\b(?:do not|don't|dont|never)\s+(?:want|need)\s+(?:to\s+see\s+)?(?:my\s+)?recommendations?\b",
        text,
    ):
        return False

    phrases = [
        "show my recommendations",
        "show recommendations",
        "show me my recommendations",
        "show me recommendations",
        "i want my recommendations",
        "i want recommendations",
        "give me my recommendations",
        "give me recommendations",
        "view my recommendations",
        "view recommendations",
        "see my recommendations",
        "see recommendations",
        "my recommendations",
        "recommendations",
        "recommendation",
        "what do you recommend",
        "what courses do you recommend",
        "which course do you recommend"
    ]

    return any(
        phrase in text
        for phrase in phrases
    )


# ==========================================================
# EXTRACT INFORMATION FOR CURRENT QUESTION
# ==========================================================

def has_answer_for_question(question_id, text):
    text = text.strip()

    if not text:
        return False

    # A name must still be checked as a name.
    if question_id == "name":
        return bool(extract_name(text))

    # Validate against the category the chatbot asked about. This avoids
    # advancing the interview when an answer only matches a different field.
    if question_id == "interests":
        return bool(extract_interests(text))

    if question_id == "subjects":
        return bool(extract_subjects(text))

    if question_id == "skills":
        return bool(extract_skills(text))

    if question_id == "personality":
        return bool(extract_personality(text))

    if question_id == "career_goal":
        return bool(extract_career_goals(text))

    # Allow a bare JAMB score such as 280.
    if question_id == "jamb_score":
        if text.isdigit():
            score = int(text)
            return 1 <= score <= 400
        return extract_jamb_score(text) > 0

    # The final extra-information question accepts any supported field,
    # including a bare score such as 280.
    if question_id == "additional_information" and text.isdigit():
        score = int(text)
        if 1 <= score <= 400:
            return True
    information = extract_all_information(text)
    return any(
        value > 0 if key == "jamb_score" else bool(value)
        for key, value in information.items()
    )


# ==========================================================
# SKIP CURRENT QUESTION
# ==========================================================

def skip_current_question(chatbot):

    current_id = QUESTIONS[
        chatbot.current_question
    ]["id"]

    # Move to next question
    chatbot.current_question += 1

    # If this was the final question
    if chatbot.current_question >= len(QUESTIONS):

        chatbot.finished = True

        chatbot.profile.calculate_confidence()

    return current_id


# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================================
# START NEW CHAT
# ==========================================================

@app.route("/start")
def start():

    session.clear()

    chat_id = str(
        uuid.uuid4()
    )

    session["chat_id"] = chat_id

    session["messages"] = []

    chatbot = ChatbotEngine()
    chatbot.start()
    session["chatbot_state"] = _serialize_chatbot(chatbot)

    return redirect(
        url_for("chat")
    )


# ==========================================================
# CHAT PAGE
# ==========================================================

@app.route("/chat")
def chat():

    chatbot = get_chatbot()

    messages = session.get(
        "messages",
        []
    )

    if not messages:

        messages.append({
            "sender": "bot",
            "text": (
                "Hi! I'm Course Compass. 🌿\n\n"
                "I'm here to help you find an ATBU "
                "programme that matches your interests, "
                "strengths, subjects and career goals."
            )
        })

        question = chatbot.get_question()

        if question:

            messages.append({
                "sender": "bot",
                "text": question
            })

        session["messages"] = messages

    return render_template(
        "chat.html",
        chatbot=chatbot,
        messages=messages
    )


# ==========================================================
# RECEIVE MESSAGE
# ==========================================================

@app.route(
    "/message",
    methods=["POST"]
)
def message():

    try:

        # Do not process a message if the server-side session has no saved
        # interview state. This prevents answers being assigned to the wrong step.
        chat_id = session.get("chat_id")

        if not chat_id or not isinstance(session.get("chatbot_state"), dict):
            session.clear()
            return jsonify({
                "success": False,
                "reset_chat": True,
                "error": (
                    "Your chat session was interrupted. "
                    "Course Compass will restart the conversation to keep "
                    "your answers matched to the correct questions."
                )
            }), 409

        chatbot = get_chatbot()

        data = request.get_json(
            silent=True
        )

        if not isinstance(data, dict):
            return jsonify({
                "success": False,
                "error": "Please send your message as JSON."
            }), 400

        raw_message = data.get("message", "")
        if not isinstance(raw_message, str):
            return jsonify({
                "success": False,
                "error": "Your message must be text."
            }), 400

        user_message = raw_message.strip()
        if not user_message:
            return jsonify({
                "success": False,
                "error": "Please enter a message."
            }), 400

        if len(user_message) > MAX_MESSAGE_LENGTH:
            return jsonify({
                "success": False,
                "error": f"Please keep each message under {MAX_MESSAGE_LENGTH} characters."
            }), 413


        messages = session.get(
            "messages",
            []
        )


        # ==================================================
        # SAVE USER MESSAGE
        # ==================================================

        messages.append({
            "sender": "user",
            "text": user_message
        })


        # ==================================================
        # RECOMMENDATION REQUEST
        # ==================================================

        if wants_recommendations(
            user_message
        ):

            chatbot.finished = True

            chatbot.profile.calculate_confidence()

            messages.append({
                "sender": "bot",
                "text": (
                    "Of course! 😊\n\n"
                    "I'll use the information you've "
                    "shared so far to show you the "
                    "programmes that match your profile."
                )
            })

            session["messages"] = messages

            return jsonify({
                "success": True,
                "messages": messages[-2:],
                "finished": True,
                "show_results": True
            })


        # ==================================================
        # FINISHED CHAT
        # ==================================================

        if chatbot.finished:

            # User wants to see results
            if wants_recommendations(
                user_message
            ):

                return jsonify({
                    "success": True,
                    "messages": [],
                    "finished": True,
                    "show_results": True
                })


            # ----------------------------------------------
            # Additional information
            # ----------------------------------------------

            result = chatbot.process_answer(
                user_message
            )


            if isinstance(
                result,
                dict
            ):

                if result.get(
                    "updated"
                ):

                    changes = result.get(
                        "changes",
                        []
                    )

                    if changes:

                        change_text = "\n".join(
                            "• " + item
                            for item in changes
                        )

                        bot_text = (
                            "Got it! 😊\n\n"
                            "I added this information "
                            "to your profile:\n\n"
                            f"{change_text}\n\n"
                            "Your confidence score is now "
                            f"{result.get('new_confidence', chatbot.profile.confidence_score)}%."
                        )

                    else:

                        bot_text = (
                            "Got it! 😊 I've updated "
                            "your profile."
                        )

                    messages.append({
                        "sender": "bot",
                        "text": bot_text
                    })

                    messages.append({
                        "sender": "bot",
                        "text": (
                            "Your recommendations have "
                            "also been updated. You can "
                            "add more information or view "
                            "your recommendations."
                        )
                    })

                else:

                    messages.append({
                        "sender": "bot",
                        "text": (
                            "I couldn't find any new "
                            "information in that message. 😊\n\n"
                            "Try telling me about your "
                            "subjects, interests, skills, "
                            "personality, career goals or "
                            "JAMB score."
                        )
                    })

            else:

                messages.append({
                    "sender": "bot",
                    "text": (
                        "I couldn't find any new "
                        "information in that message. 😊\n\n"
                        "Try telling me about your "
                        "subjects, interests, skills, "
                        "personality, career goals or "
                        "JAMB score."
                    )
                })


            session["messages"] = messages

            return jsonify({
                "success": True,
                "messages": messages[-2:],
                "finished": True,
                "show_results": False
            })


        # ==================================================
        # CURRENT QUESTION
        # ==================================================

        if chatbot.current_question >= len(QUESTIONS):
            chatbot.finished = True
            chatbot.profile.calculate_confidence()
            session["messages"] = messages + [{
                "sender": "bot",
                "text": "Your profile is ready. You can view your recommendations now."
            }]
            return jsonify({
                "success": True,
                "messages": session["messages"][-1:],
                "finished": True,
                "show_results": True,
            })

        current_index = chatbot.current_question
        current_question_id = QUESTIONS[current_index]["id"]


        # ==================================================
        # SKIP / I DON'T KNOW
        # ==================================================

        if is_skip_command(
            user_message
        ):

            skip_current_question(
                chatbot
            )

            messages.append({
                "sender": "bot",
                "text": (
                    "That's okay 😊 "
                    "You can skip this one. "
                    "We can continue with the next question."
                )
            })


            if chatbot.finished:

                messages.append({
                    "sender": "bot",
                    "text": (
                        "We've reached the end of "
                        "the questions. 😊\n\n"
                        "You can now view your "
                        "recommendations, or tell me "
                        "anything else you remember."
                    )
                })

            else:

                next_question = chatbot.get_question()

                messages.append({
                    "sender": "bot",
                    "text": next_question
                })


            session["messages"] = messages

            return jsonify({
                "success": True,
                "messages": messages[-3:],
                "finished": chatbot.finished,
                "show_results": chatbot.finished
            })


        # ==================================================
        # CONTINUE / NEXT
        # ==================================================

        if is_continue_command(
            user_message
        ):

            chatbot.current_question += 1


            if chatbot.current_question >= len(
                QUESTIONS
            ):

                chatbot.finished = True

                chatbot.profile.calculate_confidence()

                messages.append({
                    "sender": "bot",
                    "text": (
                        "Alright! 😊 We've finished "
                        "the questions."
                    )
                })

                messages.append({
                    "sender": "bot",
                    "text": (
                        "You can view your recommendations "
                        "now, or tell me anything else "
                        "you remember about yourself."
                    )
                })

                session["messages"] = messages

                return jsonify({
                    "success": True,
                    "messages": messages[-2:],
                    "finished": True,
                    "show_results": True
                })


            next_question = chatbot.get_question()

            messages.append({
                "sender": "bot",
                "text": next_question
            })

            session["messages"] = messages

            return jsonify({
                "success": True,
                "messages": messages[-1:],
                "finished": False,
                "show_results": False
            })


        # ==================================================
        # FINISH EARLY
        # ==================================================

        if is_finish_command(
            user_message
        ):

            chatbot.finished = True

            chatbot.profile.calculate_confidence()

            messages.append({
                "sender": "bot",
                "text": (
                    "No problem! 😊\n\n"
                    "I'll stop the questions here and "
                    "use the information you've shared "
                    "so far."
                )
            })

            messages.append({
                "sender": "bot",
                "text": (
                    "Before viewing your recommendations, "
                    "you can still tell me anything you "
                    "forgot to mention.\n\n"
                    "For example:\n"
                    "• I'm also good at Mathematics.\n"
                    "• I enjoy programming.\n"
                    "• I want to become an engineer.\n"
                    "• My JAMB score was 280.\n\n"
                    "Or you can continue to your recommendations."
                )
            })

            session["messages"] = messages

            return jsonify({
                "success": True,
                "messages": messages[-2:],
                "finished": True,
                "show_results": True
            })
        # ==================================================
        # NO MORE INFORMATION
        # ==================================================

        if (
            chatbot.current_question < len(QUESTIONS)
            and QUESTIONS[chatbot.current_question]["id"] == "additional_information"
            and is_no_command(user_message)
        ):
            chatbot.finished = True

            chatbot.profile.calculate_confidence()

            messages.append({
                "sender": "bot",
                "text": (
                    "Alright! 😊\n\n"
                    "That's completely fine. "
                    "I have enough information to work with."
                )
            })

            messages.append({
                "sender": "bot",
                "text": (
                    "Your profile is ready. 🌿\n\n"
                    "Click \"View My Recommendations\" "
                    "to see the ATBU programmes that "
                    "match you best."
                )
            })

            session["messages"] = messages

            return jsonify({
                "success": True,
                "messages": messages[-2:],
                "finished": True,
                "show_results": True
        })

        # ==================================================
        # CHECK WHETHER ANSWER MAKES SENSE
        # ==================================================

        if not has_answer_for_question(
            current_question_id,
            user_message
        ):

            messages.append({
                "sender": "bot",
                "text": (
                    "Sorry, I didn't quite understand "
                    "that. 😊\n\n"
                    "Please try answering the question "
                    "again, or type \"continue\" to move "
                    "to the next question."
                )
            })

            session["messages"] = messages

            return jsonify({
                "success": True,
                "messages": messages[-1:],
                "finished": False,
                "show_results": False
            })

        # ==================================================
        # NORMAL ANSWER
        # ==================================================

        # --------------------------------------------------
        # JAMB SCORE
        # --------------------------------------------------
        # If the student enters only a number such as 220,
        # convert it into a format the existing parser
        # already understands.
        # --------------------------------------------------

        message_for_engine = user_message

        if current_question_id == "jamb_score":

            if user_message.isdigit():

                score = int(user_message)

                if 1 <= score <= 400:
                    message_for_engine = (
                        f"JAMB {score}"
                    )

        # --------------------------------------------------
        # Process using the existing chatbot engine
        # --------------------------------------------------

        result = chatbot.process_answer(
            message_for_engine
        )


        natural_responses = {

            "name": (
                f"Nice to meet you, "
                f"{chatbot.profile.name}! 😊"
            ),

            "interests":
                "Oh, interesting! 🌿",

            "subjects":
                "Got it. 👍",

            "skills":
                "Nice! 😊",

            "personality":
                "I see. That's helpful.",

            "career_goal":
                "That's interesting! 😊",

            "jamb_score":
                "Got it! 🎓"
        }


        response = natural_responses.get(
            current_question_id
        )


        if response:

            messages.append({
                "sender": "bot",
                "text": response
            })

        # ==================================================
        # INTERVIEW COMPLETED
        # ==================================================

        if chatbot.finished:
            messages.append({
                "sender": "bot",
                "text": (
                    "Perfect! 😊\n\n"
                    "I've finished getting to know your profile."
                )
            })

            messages.append({
                "sender": "bot",
                "text": (
                    "You can still tell me anything you forgot "
                    "to mention, such as another subject, "
                    "interest, skill, career goal or your JAMB score.\n\n"
                    "When you're ready, click "
                    "\"View My Recommendations\" to see the "
                    "ATBU programmes that match your profile. 🌿"
                )
            })

            session["messages"] = messages

            return jsonify({
                "success": True,
                "messages": messages[-2:],
                "finished": True,
                "show_results": True
            })


        # ==================================================
        # NEXT QUESTION
        # ==================================================

        next_question = chatbot.get_question()

        if next_question:

            messages.append({
                "sender": "bot",
                "text": next_question
            })


        session["messages"] = messages


        return jsonify({
            "success": True,
            "messages": messages[-2:],
            "finished": chatbot.finished,
            "show_results": False
        })


    # ======================================================
    # ERROR
    # ======================================================

    except Exception:
        app.logger.exception("An error occurred while processing a Course Compass message")
        return jsonify({
            "success": False,
            "error": "Something went wrong while processing your message. Please try again."
        }), 500


# ==========================================================
# RESULTS
# ==========================================================

@app.route("/results")
def results():

    chatbot = get_chatbot()

    recommendations = (
        chatbot.get_recommendations()
    )

    profile = chatbot.get_profile()

    return render_template(
        "results.html",
        recommendations=recommendations,
        profile=profile
    )


# ==========================================================
# RESTART
# ==========================================================

@app.route("/restart")
def restart():

    session.clear()

    return redirect(
        url_for("start")
    )


@app.errorhandler(413)
def request_too_large(_error):
    if request.path == "/message":
        return jsonify({
            "success": False,
            "error": f"Please keep each message under {MAX_MESSAGE_LENGTH} characters."
        }), 413
    return "Request is too large.", 413


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=os.environ.get("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"}
    )