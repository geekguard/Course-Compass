import os
import unittest
from flask import Flask, jsonify, session

from chatbot.chatbot_engine import ChatbotEngine
from chatbot.parser import (
    extract_all_information,
    extract_career_goals,
    extract_interests,
    extract_jamb_score,
    extract_subjects,
)
from chatbot.questions import QUESTIONS
from data.courses import COURSES
from models.student_profile import StudentProfile
from chatbot.recommender import RecommendationEngine


class ParserAndProfileTests(unittest.TestCase):
    def test_career_goal_does_not_become_interest(self):
        self.assertEqual(extract_career_goals("I wanted to become a doctor"), ["doctor"])
        self.assertNotIn("health", extract_interests("I wanted to become a doctor"))

    def test_explicit_interest_is_preserved_with_career_goal(self):
        self.assertIn("art", extract_interests("I want to become a doctor and I enjoy drawing"))
        self.assertNotIn("health", extract_interests("I want to become a doctor and I enjoy drawing"))

    def test_interest_statement_still_extracts_health(self):
        self.assertIn("health", extract_interests("I enjoy medicine"))

    def test_negative_interest_is_not_recorded(self):
        self.assertNotIn("health", extract_interests("I am not interested in medicine"))
        self.assertNotIn("business", extract_interests("I do not like business"))
        self.assertNotIn("doctor", extract_career_goals("I don't want to be a doctor"))

    def test_name_answer_updates_profile_completeness_immediately(self):
        bot = ChatbotEngine()
        bot.start()
        bot.process_answer("Amina")
        self.assertEqual(bot.profile.confidence_score, 5)

    def test_personality_description_does_not_create_interests(self):
        self.assertEqual(extract_interests("I am creative and patient"), [])
        self.assertIn("creative", extract_all_information("I am creative and patient")["personality_traits"])

    def test_fuzzy_spelling_still_recognizes_subject(self):
        self.assertIn("physics", extract_subjects("I like physcs"))

    def test_invalid_jamb_score_is_not_clamped_to_400(self):
        self.assertEqual(extract_jamb_score("I got 450 in JAMB"), 0)

    def test_zero_is_not_accepted_as_a_completed_jamb_score(self):
        bot = ChatbotEngine()
        bot.start()
        bot.current_question = next(i for i, q in enumerate(QUESTIONS) if q["id"] == "jamb_score")
        result = bot.process_answer("0")
        self.assertEqual(result["type"], "unclear")
        self.assertEqual(bot.profile.jamb_score, 0)
        self.assertEqual(QUESTIONS[bot.current_question]["id"], "jamb_score")

    def test_interview_stores_subject_without_making_it_interest(self):
        bot = ChatbotEngine()
        bot.start()
        bot.process_answer("Amina")
        bot.process_answer("drawing")
        bot.process_answer("Biology")
        self.assertIn("biology", bot.profile.favourite_subjects)
        self.assertNotIn("science", bot.profile.interests)

    def test_teacher_is_a_valid_career_match(self):
        bot = ChatbotEngine()
        bot.start()
        bot.process_answer("Amina")
        bot.process_answer("drawing")
        bot.process_answer("English")
        bot.process_answer("communication")
        bot.process_answer("creative")
        bot.process_answer("I want to be a teacher")
        self.assertEqual(bot.profile.name, "Amina")
        self.assertIn("teacher", bot.profile.career_goals)
        recommendations = bot.get_recommendations()
        self.assertTrue(recommendations)
        self.assertTrue(any("teacher" in " ".join(r["course"].careers) for r in recommendations))

    def test_confidence_rises_when_a_new_subject_is_added_later(self):
        bot = ChatbotEngine()
        bot.start()
        bot.profile.name = "Amina"
        bot.profile.interests = ["art"]
        bot.profile.favourite_subjects = ["biology"]
        bot.profile.skills = ["communication"]
        bot.profile.calculate_confidence()
        old_confidence = bot.profile.confidence_score
        result = bot.update_profile("I am also good at mathematics")
        self.assertTrue(result["updated"])
        self.assertGreater(result["new_confidence"], old_confidence)

    def test_no_profile_match_means_no_arbitrary_recommendations(self):
        profile = StudentProfile(jamb_score=300)
        recommendations = RecommendationEngine().recommend(profile)
        self.assertEqual(recommendations, [])

    def test_course_data_has_unique_names_and_valid_cutoffs(self):
        names = [course.name for course in COURSES]
        self.assertEqual(len(names), len(set(names)))
        self.assertTrue(all(
            course.jamb_cutoff is None or 0 <= course.jamb_cutoff <= 400
            for course in COURSES
        ))


class WebFlowRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from app import app
        cls.app = app
        cls.app.config.update(TESTING=True, SECRET_KEY="test-course-compass")

    def setUp(self):
        self.client = self.app.test_client()
        self.client.get("/start")
        self.client.get("/chat")

    def send(self, text):
        return self.client.post("/message", json={"message": text})

    def test_full_interview_keeps_profile_categories_separate(self):
        for answer in [
            "Amina", "drawing", "Biology", "communication", "creative",
            "I want to become a doctor", "280", "nothing else",
        ]:
            response = self.send(answer)
            self.assertEqual(response.status_code, 200, response.get_data(as_text=True))

        with self.client.session_transaction() as saved_session:
            state = saved_session["chatbot_state"]
        from app import _restore_chatbot
        chatbot = _restore_chatbot(state)
        self.assertEqual(chatbot.profile.name, "Amina")
        self.assertEqual(chatbot.profile.interests, ["art"])
        self.assertEqual(chatbot.profile.favourite_subjects, ["biology"])
        self.assertEqual(chatbot.profile.skills, ["communication"])
        self.assertEqual(chatbot.profile.career_goals, ["doctor"])
        self.assertNotIn("health", chatbot.profile.interests)
        self.assertEqual(chatbot.profile.jamb_score, 280)
        self.assertTrue(chatbot.finished)
        results_response = self.client.get("/results")
        self.assertEqual(results_response.status_code, 200)
        self.assertIn("UTME/JAMB Subject Combination", results_response.get_data(as_text=True))

    def test_chatbot_state_survives_request_by_request_restoration(self):
        self.send("Amina")
        self.send("drawing")
        # Each request reconstructs the engine from the saved server-side state.
        response = self.send("Biology")
        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as saved_session:
            self.assertEqual(saved_session["chatbot_state"]["current_question"], 3)
            self.assertEqual(saved_session["chatbot_state"]["profile"]["favourite_subjects"], ["biology"])

    def test_saved_session_can_be_loaded_by_a_new_app_instance(self):
        self.send("Amina")
        self.send("drawing")
        cookie = self.client.get_cookie("session")
        self.assertIsNotNone(cookie)

        from app import app as original_app
        from server_session import SQLiteSessionInterface

        restored_app = Flask(
            "course_compass_session_restore_test",
            instance_path=original_app.instance_path,
            instance_relative_config=True,
        )
        restored_app.session_interface = SQLiteSessionInterface(
            os.path.join(original_app.instance_path, "course_compass_sessions.sqlite3")
        )

        @restored_app.get("/saved-state")
        def saved_state():
            return jsonify(session.get("chatbot_state", {}))

        restored_client = restored_app.test_client()
        restored_client.set_cookie("session", cookie.value)
        response = restored_client.get("/saved-state")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["current_question"], 2)
        self.assertEqual(response.get_json()["profile"]["name"], "Amina")

    def test_missing_state_is_rejected_instead_of_assigning_answer_to_name(self):
        self.send("Amina")
        self.send("drawing")
        with self.client.session_transaction() as saved_session:
            saved_session.pop("chatbot_state", None)
        response = self.send("teacher")
        self.assertEqual(response.status_code, 409)
        self.assertTrue(response.get_json()["reset_chat"])
        self.assertNotIn("Nice to meet you, Teacher", str(response.get_json()))

    def test_no_does_not_end_interview_mid_question(self):
        for answer in ["Amina", "drawing", "Biology", "communication", "creative"]:
            self.send(answer)
        response = self.send("no")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.get_json()["finished"])
        with self.client.session_transaction() as saved_session:
            self.assertEqual(saved_session["chatbot_state"]["current_question"], 5)

    def test_negative_recommendation_request_does_not_finish_early(self):
        self.send("Amina")
        response = self.send("I don't want recommendations")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.get_json()["finished"])
        self.assertFalse(response.get_json()["show_results"])

    def test_chat_template_escapes_user_html(self):
        self.send("Amina")
        payload = "<script>alert('xss')</script>"
        self.send(payload)
        page = self.client.get("/chat").get_data(as_text=True)
        self.assertNotIn("<script>alert('xss')</script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_non_text_and_oversized_messages_are_rejected(self):
        non_text = self.client.post("/message", json={"message": 123})
        self.assertEqual(non_text.status_code, 400)
        too_long = self.send("x" * 1001)
        self.assertEqual(too_long.status_code, 413)

    def test_bare_jamb_score_is_accepted_as_additional_information(self):
        for answer in ["Amina", "drawing", "Biology", "communication", "creative", "teacher", "280", "250"]:
            response = self.send(answer)
            self.assertEqual(response.status_code, 200, response.get_data(as_text=True))
        # The final bare number is accepted as additional JAMB information.
        with self.client.session_transaction() as saved_session:
            self.assertEqual(saved_session["chatbot_state"]["profile"]["jamb_score"], 250)


if __name__ == "__main__":
    unittest.main()
