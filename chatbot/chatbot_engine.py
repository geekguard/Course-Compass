"""
chatbot_engine.py

Controls the Course Compass interview and
recommendation process.
"""

from chatbot.questions import QUESTIONS

from chatbot.parser import (
    extract_name,
    has_information,
    extract_interests,
    extract_subjects,
    extract_skills,
    extract_personality,
    extract_career_goals,
    extract_jamb_score,
    extract_all_information

)

from chatbot.recommender import RecommendationEngine
from models.student_profile import StudentProfile


class ChatbotEngine:
    """
    Controls the conversation between the student
    and Course Compass.
    """

    def __init__(self):

        self.profile = StudentProfile()

        self.recommender = RecommendationEngine()

        self.current_question = 0

        self.finished = False

    # ==========================================================
    # START
    # ==========================================================

    def start(self):

        self.profile.reset()

        self.current_question = 0

        self.finished = False

    # ==========================================================
    # QUESTION CONTROL
    # ==========================================================

    def has_more_questions(self):

        return (
            not self.finished
            and self.current_question < len(QUESTIONS)
        )

    # ==========================================================
    # FINISH KEYWORDS
    # ==========================================================

    @staticmethod
    def _is_finish_request(answer):
        """
        Check whether the student wants to stop the
        interview and see their recommendations.

        The matching is intentionally simple because
        Course Compass is a rules-based chatbot.
        """

        if not isinstance(answer, str):

            return False

        text = answer.lower().strip()

        finish_phrases = [
            "that's all",
            "that is all",
            "thats all",
            "i'm done",
            "im done",
            "i am done",
            "i'm finished",
            "im finished",
            "i am finished",
            "finish",
            "done",
            "finished",
            "that's enough",
            "that is enough",
            "thats enough",
            "no more questions",
            "show me my recommendations",
            "show my recommendations",
            "show me the recommendations",
            "give me my recommendations",
            "give me the recommendations",
            "let me see my recommendations",
            "i want my recommendations",
            "i want to see my recommendations",
            "can i get my recommendations",
            "can i see my recommendations",
            "recommend now",
            "recommend courses",
            "let's see the courses",
            "lets see the courses",
        ]

        return text in finish_phrases

    # ==========================================================
    # SKIP KEYWORDS
    # ==========================================================

    @staticmethod
    def _is_skip_request(answer):
        """
        Check whether the student does not know an answer
        or wants to skip the current question.
        """

        if not isinstance(answer, str):

            return False

        text = answer.lower().strip()

        skip_phrases = [
            "i don't know",
            "i dont know",
            "i am not sure",
            "i'm not sure",
            "im not sure",
            "not sure",
            "i don't know yet",
            "i dont know yet",
            "no idea",
            "skip",
            "skip this",
            "i can't answer that",
            "i cant answer that",
            "i'd rather skip",
            "id rather skip",
        ]

        return text in skip_phrases

    # ==========================================================
    # CONTINUE / MOVE ON KEYWORDS
    # ==========================================================

    @staticmethod
    def _is_continue_request(answer):
        """
        Check whether the student wants to continue
        without answering the current question.
        """

        if not isinstance(answer, str):
            return False

        text = answer.lower().strip()

        continue_phrases = [
            "continue",
            "next",
            "move on",
            "move to the next",
            "next question",
            "go on",
            "skip",
            "skip this",
            "i want to continue",
            "let's continue",
            "lets continue",
        ]

        return text in continue_phrases

    # ==========================================================
    # SKIP RESPONSE
    # ==========================================================

    def _get_skip_response(self, question_id):
        """
        Return a natural response when the student does not
        know an answer or wants to skip the question.
        """

        responses = {

            "name": (
                "No worries 😊 We can continue without your name."
            ),

            "interests": (
                "That's okay 😊 Let's try something else."
            ),

            "subjects": (
                "No problem. We can come back to that if you "
                "remember later."
            ),

            "skills": (
                "That's okay 😊 Let's keep going."
            ),

            "personality": (
                "No worries. Let's move on."
            ),

            "career_goal": (
                "That's completely fine 😊 You don't have to "
                "have your career figured out yet."
            ),

            "jamb_score": (
                "No problem 😊 You can add your JAMB score "
                "later if you have it."
            ),

            "additional_information": (
                "That's okay 😊"
            )
        }

        return responses.get(
            question_id,
            "No worries 😊 Let's keep going."
        )

    # ==========================================================
    # GET CURRENT QUESTION
    # ==========================================================

    def get_question(self):

        if self.finished:

            return (
                "If you remember anything else about yourself, "
                "just tell me. 😊\n\n"
                "For example:\n"
                "• I'm also good at Mathematics.\n"
                "• I enjoy Programming.\n"
                "• I want to become an Engineer.\n"
                "• My JAMB score was 280."
            )

        if self.current_question >= len(QUESTIONS):

            return None

        return QUESTIONS[
            self.current_question
        ]["question"]

    # ==========================================================
    # PROCESS ANSWER
    # ==========================================================

    def process_answer(self, answer):

        # ------------------------------------------------------
        # Ignore invalid input
        # ------------------------------------------------------

        if not isinstance(answer, str):

            return None

        answer = answer.strip()

        if not answer:

            return None

        # ------------------------------------------------------
        # Additional information after interview
        # ------------------------------------------------------

        if self.finished:

            return self.update_profile(answer)

        # ------------------------------------------------------
        # Allow the student to finish early
        # ------------------------------------------------------

        if self._is_finish_request(answer):

            self.finished = True

            self.profile.calculate_confidence()

            return None

        # ------------------------------------------------------
        # Final additional-information question
        # ------------------------------------------------------

        if (
                self.current_question < len(QUESTIONS)
                and QUESTIONS[self.current_question]["id"]
                == "additional_information"
        ):

            no_more_information = [
                "no",
                "nope",
                "nothing",
                "nothing else",
                "nothing more",
                "no thanks",
                "that's all",
                "thats all",
                "that is all",
                "i have nothing else",
                "i don't have anything else",
                "i dont have anything else",
                "nothing to add",
                "i have nothing to add"
            ]

            if answer.lower().strip() in no_more_information:
                self.current_question += 1

                self.finished = True

                self.profile.calculate_confidence()

                return {
                    "type": "finished"
                }
        # ------------------------------------------------------
        # Current interview question
        # ------------------------------------------------------

        if self.current_question >= len(QUESTIONS):

            self.finished = True

            self.profile.calculate_confidence()

            return None

        question_id = QUESTIONS[
            self.current_question
        ]["id"]

        # ------------------------------------------------------
        # FINAL QUESTION: no more information
        # ------------------------------------------------------

        if question_id == "additional_information":

            text = answer.lower().strip()

            no_more_information = [
                "no",
                "nope",
                "nothing",
                "nothing else",
                "nothing more",
                "no thanks",
                "that's all",
                "thats all",
                "that is all",
                "i have nothing else",
                "i don't have anything else",
                "i dont have anything else",
                "nothing to add",
                "i have nothing to add"
            ]

            if (
                    text in no_more_information
                    or self._is_continue_request(answer)
                    or self._is_finish_request(answer)
            ):
                self.finished = True

                self.profile.calculate_confidence()

                return {
                    "type": "finished",
                    "message": (
                        "Perfect! 😊\n\n"
                        "I have everything I need from you. "
                        "You can now view your course recommendations."
                    )
                }
        # ------------------------------------------------------
        # Allow "I don't know", "skip", or "continue"
        # ------------------------------------------------------

        if (
            self._is_skip_request(answer)
            or self._is_continue_request(answer)
        ):

            self.current_question += 1

            if self.current_question >= len(QUESTIONS):

                self.finished = True

                self.profile.calculate_confidence()

            return {
                "type": "skipped"
            }

        # ------------------------------------------------------
        # Check whether the answer contains useful information
        # ------------------------------------------------------

        # Validate against the question currently being asked. This prevents,
        # for example, a career title from being accepted as an interest answer.
        if question_id != "name":
            if question_id == "interests":
                answer_is_valid = bool(extract_interests(answer))
            elif question_id == "subjects":
                answer_is_valid = bool(extract_subjects(answer))
            elif question_id == "skills":
                answer_is_valid = bool(extract_skills(answer))
            elif question_id == "personality":
                answer_is_valid = bool(extract_personality(answer))
            elif question_id == "career_goal":
                answer_is_valid = bool(extract_career_goals(answer))
            elif question_id == "jamb_score":
                if answer.isdigit():
                    answer_is_valid = 1 <= int(answer) <= 400
                else:
                    answer_is_valid = extract_jamb_score(answer) > 0
            elif question_id == "additional_information":
                answer_is_valid = (
                    answer.isdigit() and 1 <= int(answer) <= 400
                ) or has_information(answer)
            else:
                answer_is_valid = has_information(answer)

            if not answer_is_valid:
                return {
                    "type": "unclear",
                    "message": (
                        "Sorry, I didn't quite understand that. 😊\n\n"
                        "Please try answering the question again, "
                        "or type \"continue\" if you'd like to "
                        "move to the next question."
                    )
                }

        # The interview asks about one category at a time, so only store the
        # category that belongs to the current question. The final
        # additional-information question is the exception: it accepts any
        # supported profile information.
        if question_id == "additional_information":
            information = extract_all_information(answer)
            if answer.isdigit() and 1 <= int(answer) <= 400:
                information["jamb_score"] = int(answer)
            self.profile.update_information(
                interests=information["interests"],
                subjects=information["subjects"],
                skills=information["skills"],
                personality=information["personality_traits"],
                careers=information["career_goals"]
            )
            if information["jamb_score"] > 0:
                self.profile.update_jamb_score(information["jamb_score"])

        # ------------------------------------------------------
        # Extract information for the current question
        # ------------------------------------------------------

        if question_id == "name":

            name = extract_name(answer)

            if not name:

                return {
                    "type": "unclear",
                    "message": (
                        "Sorry, I couldn't quite understand "
                        "your name. 😊\n\n"
                        "Please try entering your name again, "
                        "or type \"continue\" if you'd rather "
                        "skip this question."
                    )
                }

            self.profile.name = name


        elif question_id == "interests":

            new_interests = extract_interests(
                answer
            )

            self.profile.add_items(
                "interests",
                new_interests
            )

        elif question_id == "subjects":

            new_subjects = extract_subjects(
                answer
            )

            self.profile.add_items(
                "favourite_subjects",
                new_subjects
            )

        elif question_id == "skills":

            new_skills = extract_skills(
                answer
            )

            self.profile.add_items(
                "skills",
                new_skills
            )

        elif question_id == "personality":

            new_personality = extract_personality(
                answer
            )

            self.profile.add_items(
                "personality_traits",
                new_personality
            )

        elif question_id == "career_goal":

            new_careers = extract_career_goals(
                answer
            )

            self.profile.add_items(
                "career_goals",
                new_careers
            )

        elif question_id == "jamb_score":

            # A number by itself is a valid JAMB answer
            if answer.isdigit():

                jamb_score = int(answer)

                if 1 <= jamb_score <= 400:
                    self.profile.update_jamb_score(
                        jamb_score
                    )

            else:

                jamb_score = extract_jamb_score(
                    answer
                )

                if jamb_score > 0:
                    self.profile.update_jamb_score(
                        jamb_score
                    )

        # ------------------------------------------------------
        # Move to next question
        # ------------------------------------------------------

        self.current_question += 1

        # ------------------------------------------------------
        # Interview finished
        # ------------------------------------------------------

        # Keep the displayed profile-completeness score current after every
        # accepted answer, including the name field which does not use add_items().
        self.profile.calculate_confidence()

        if self.current_question >= len(QUESTIONS):

            self.finished = True

            self.profile.calculate_confidence()

        return None

    # ==========================================================
    # UPDATE PROFILE WITH NEW INFORMATION
    # ==========================================================

    def update_profile(self, answer):

        old_confidence = (
            self.profile.confidence_score
        )

        # ------------------------------------------------------
        # Extract possible new information once
        # ------------------------------------------------------

        information = extract_all_information(answer)
        new_interests = information["interests"]
        new_subjects = information["subjects"]
        new_skills = information["skills"]
        new_personality = information["personality_traits"]
        new_careers = information["career_goals"]
        new_jamb = information["jamb_score"]

        if answer.isdigit() and 1 <= int(answer) <= 400:
            new_jamb = int(answer)

        # ------------------------------------------------------
        # Save old information
        # ------------------------------------------------------

        old_interests = set(
            self.profile.interests
        )

        old_subjects = set(
            self.profile.favourite_subjects
        )

        old_skills = set(
            self.profile.skills
        )

        old_personality = set(
            self.profile.personality_traits
        )

        old_careers = set(
            self.profile.career_goals
        )

        old_jamb = self.profile.jamb_score

        # ------------------------------------------------------
        # Merge new information
        # ------------------------------------------------------

        self.profile.add_items(
            "interests",
            new_interests
        )

        self.profile.add_items(
            "favourite_subjects",
            new_subjects
        )

        self.profile.add_items(
            "skills",
            new_skills
        )

        self.profile.add_items(
            "personality_traits",
            new_personality
        )

        self.profile.add_items(
            "career_goals",
            new_careers
        )

        # ------------------------------------------------------
        # Update JAMB only if a valid score was detected
        # ------------------------------------------------------

        if new_jamb > 0:

            self.profile.update_jamb_score(
                new_jamb
            )

        # ------------------------------------------------------
        # Recalculate confidence
        # ------------------------------------------------------

        self.profile.calculate_confidence()

        new_confidence = (
            self.profile.confidence_score
        )

        # ------------------------------------------------------
        # Find exactly what changed
        # ------------------------------------------------------

        added_interests = [
            item
            for item in self.profile.interests
            if item not in old_interests
        ]

        added_subjects = [
            item
            for item in self.profile.favourite_subjects
            if item not in old_subjects
        ]

        added_skills = [
            item
            for item in self.profile.skills
            if item not in old_skills
        ]

        added_personality = [
            item
            for item in self.profile.personality_traits
            if item not in old_personality
        ]

        added_careers = [
            item
            for item in self.profile.career_goals
            if item not in old_careers
        ]

        jamb_changed = (
            new_jamb > 0
            and new_jamb != old_jamb
        )

        # ------------------------------------------------------
        # Human-readable summary
        # ------------------------------------------------------

        changes = []

        if added_interests:

            changes.append(
                "interests: "
                + ", ".join(added_interests)
            )

        if added_subjects:

            changes.append(
                "subjects: "
                + ", ".join(added_subjects)
            )

        if added_skills:

            changes.append(
                "skills: "
                + ", ".join(added_skills)
            )

        if added_personality:

            changes.append(
                "personality: "
                + ", ".join(added_personality)
            )

        if added_careers:

            changes.append(
                "career goals: "
                + ", ".join(added_careers)
            )

        if jamb_changed:

            changes.append(
                f"JAMB score: {new_jamb}"
            )

        # ------------------------------------------------------
        # Recalculate recommendations
        # ------------------------------------------------------

        recommendations = (
            self.get_recommendations()
        )

        # ------------------------------------------------------
        # Return structured result
        # ------------------------------------------------------

        return {
            "updated": bool(changes),
            "changes": changes,
            "old_confidence": old_confidence,
            "new_confidence": new_confidence,
            "confidence_increased": (
                new_confidence > old_confidence
            ),
            "recommendations": recommendations
        }

    # ==========================================================
    # GET RECOMMENDATIONS
    # ==========================================================

    def get_recommendations(self):

        return self.recommender.recommend(
            self.profile
        )

    # ==========================================================
    # GET PROFILE
    # ==========================================================

    def get_profile(self):

        return self.profile

    # ==========================================================
    # CHECK COMPLETION
    # ==========================================================

    def is_complete(self):

        return self.finished

    # ==========================================================
    # RESET
    # ==========================================================

    def reset(self):

        self.start()