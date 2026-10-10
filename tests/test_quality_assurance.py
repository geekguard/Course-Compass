"""Additional deterministic quality-assurance tests for Course Compass.

These tests use synthetic profiles and the application's Flask test client. They
require no real student participants and do not change the GUI.
"""
import unittest

from chatbot.parser import (
    extract_all_information,
    extract_career_goals,
    extract_interests,
    extract_skills,
)
from chatbot.recommender import RecommendationEngine
from data.courses import COURSES
from models.course import Course
from models.student_profile import StudentProfile


class ParserQualityTests(unittest.TestCase):
    def test_website_interest_is_not_misclassified_as_engineering(self):
        for phrase in (
            "I am interested in building websites",
            "I enjoy creating websites",
            "I like website design",
        ):
            with self.subTest(phrase=phrase):
                interests = extract_interests(phrase)
                self.assertIn("technology", interests)
                self.assertNotIn("engineering", interests)

    def test_building_physical_things_still_matches_engineering(self):
        self.assertIn("engineering", extract_interests("I like building things"))

    def test_problem_solving_and_data_analysis_skill_phrases(self):
        skills = extract_skills("I can solve problems and analyse data")
        self.assertIn("problem solving", skills)
        self.assertIn("analytical", skills)

    def test_writing_code_is_not_automatically_a_communication_skill(self):
        self.assertEqual(extract_skills("I am good at writing code"), ["coding"])
        skills = extract_skills("I am good at writing code and communication")
        self.assertIn("coding", skills)
        self.assertIn("communication", skills)

    def test_specific_software_engineer_goal_is_not_duplicated_as_engineer(self):
        goals = extract_career_goals("I want to become a software engineer")
        self.assertEqual(goals, ["software engineer"])

    def test_parser_handles_non_string_input_safely(self):
        self.assertEqual(extract_interests(None), [])
        self.assertEqual(extract_career_goals(123), [])
        self.assertEqual(extract_all_information(None)["interests"], [])

    def test_mixed_positive_and_negative_interests_keep_only_positive_category(self):
        interests = extract_interests("I do not like medicine but I enjoy farming")
        self.assertIn("agriculture", interests)
        self.assertNotIn("health", interests)
        self.assertNotIn("business", interests)


class RecommendationQualityTests(unittest.TestCase):
    def setUp(self):
        self.engine = RecommendationEngine()

    def test_recommendation_scores_stay_between_zero_and_one_hundred(self):
        profile = StudentProfile(
            interests=["health", "science"],
            favourite_subjects=["biology", "chemistry"],
            skills=["communication", "analytical", "coding"],
            personality_traits=["patient", "analytical", "caring"],
            career_goals=["doctor"],
            jamb_score=400,
        )
        results = self.engine.recommend(profile, top_n=100)
        self.assertTrue(results)
        for result in results:
            with self.subTest(course=result["course"].name):
                self.assertGreaterEqual(result["score"], 0)
                self.assertLessEqual(result["score"], 100)
                self.assertEqual(result["score"], result["percentage"])
                self.assertTrue(result["reasons"])

    def test_recommendations_are_sorted_by_score_then_course_name(self):
        profile = StudentProfile(interests=["agriculture"])
        results = self.engine.recommend(profile, top_n=100)
        pairs = [(item["score"], item["course"].name.casefold()) for item in results]
        self.assertEqual(pairs, sorted(pairs, key=lambda pair: (-pair[0], pair[1])))

    def test_top_n_limits_result_count(self):
        profile = StudentProfile(interests=["health"])
        self.assertLessEqual(len(self.engine.recommend(profile, top_n=2)), 2)
        self.assertEqual(self.engine.recommend(profile, top_n=0), [])

    def test_jamb_score_alone_does_not_produce_recommendations(self):
        profile = StudentProfile(jamb_score=350)
        self.assertEqual(self.engine.recommend(profile), [])

    def test_course_serialization_round_trip_preserves_unknown_cutoff(self):
        medicine = next(course for course in COURSES if course.name == "Medicine and Surgery")
        restored = Course.from_dict(medicine.to_dict())
        self.assertEqual(restored.name, medicine.name)
        self.assertIsNone(restored.jamb_cutoff)
        self.assertEqual(restored.degree, "MBBS")

    def test_unknown_cutoff_is_not_presented_as_a_verified_cutoff(self):
        profile = StudentProfile(career_goals=["doctor"], jamb_score=280)
        result = next(
            item for item in self.engine.recommend(profile, top_n=100)
            if item["course"].name == "Medicine and Surgery"
        )
        self.assertTrue(any("has not been verified" in reason for reason in result["reasons"]))

    def test_clinical_specialties_are_not_separate_undergraduate_recommendations(self):
        names = {course.name for course in COURSES}
        self.assertIn("Medicine and Surgery", names)
        self.assertNotIn("Internal Medicine", names)
        self.assertNotIn("Surgery", names)
        self.assertNotIn("Pediatrics", names)
        self.assertNotIn("Urban & Regional Planning", names)

    def test_course_catalogue_fields_have_expected_types(self):
        for course in COURSES:
            with self.subTest(course=course.name):
                self.assertTrue(course.name.strip())
                self.assertTrue(course.faculty.strip())
                self.assertTrue(course.department.strip())
                self.assertTrue(course.description.strip())
                self.assertIsInstance(course.interests, list)
                self.assertIsInstance(course.subjects, list)
                self.assertIsInstance(course.jamb_subjects, list)
                self.assertTrue(course.degree)
                self.assertTrue(course.duration)

    def test_course_catalogue_does_not_contain_duplicate_names(self):
        names = [course.name.casefold() for course in COURSES]
        self.assertEqual(len(names), len(set(names)))


if __name__ == "__main__":
    unittest.main()

class WebRouteQualityTests(unittest.TestCase):
    """Black-box HTTP checks using Flask's test client (no live users)."""

    @classmethod
    def setUpClass(cls):
        from app import app
        cls.app = app
        cls.app.config.update(TESTING=True, SECRET_KEY="course-compass-qa-test-key")

    def setUp(self):
        self.client = self.app.test_client()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Course Compass", response.data)

    def test_start_route_redirects_to_chat_and_chat_renders(self):
        response = self.client.get("/start", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hi! I&#39;m Course Compass", response.data)

    def test_session_cookie_uses_http_only_and_same_site(self):
        response = self.client.get("/start")
        cookie = response.headers.get("Set-Cookie", "")
        self.assertIn("HttpOnly", cookie)
        self.assertIn("SameSite=Lax", cookie)

    def test_missing_json_payload_is_rejected(self):
        self.client.get("/start")
        response = self.client.post("/message", data="not-json", content_type="text/plain")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.get_json()["success"])

    def test_empty_message_is_rejected(self):
        self.client.get("/start")
        response = self.client.post("/message", json={"message": "   "})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Please enter a message", response.get_json()["error"])

    def test_malformed_saved_state_is_safely_bounded(self):
        from app import _restore_chatbot
        from chatbot.questions import QUESTIONS

        bot = _restore_chatbot({
            "current_question": 99999,
            "finished": False,
            "profile": {
                "name": 42,
                "interests": ["technology", None, 4, "technology"],
                "jamb_score": 999,
            },
        })
        self.assertEqual(bot.current_question, len(QUESTIONS))
        self.assertTrue(bot.finished)
        self.assertEqual(bot.profile.name, "")
        self.assertEqual(bot.profile.interests, ["technology"])
        self.assertEqual(bot.profile.jamb_score, 0)
