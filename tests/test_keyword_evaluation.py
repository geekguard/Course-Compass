"""Regression tests for common, varied and potentially ambiguous student inputs."""
import unittest

from chatbot.parser import (
    extract_all_information,
    extract_career_goals,
    extract_interests,
    extract_personality,
    extract_subjects,
)
from chatbot.chatbot_engine import ChatbotEngine
from data.courses import COURSES
from models.student_profile import StudentProfile
from chatbot.recommender import RecommendationEngine


class KeywordCoverageTests(unittest.TestCase):
    def test_economics_agriculture_social_studies_are_not_health(self):
        answers = [
            "economics agriculture and social studies",
            "I like economics, agriculture and social studies",
            "I am interested in economics, agriculture and social studies",
            "I enjoy studying economics and I like farming and social studies",
            "My interests are economic issues, crop farming, and society",
        ]
        for answer in answers:
            with self.subTest(answer=answer):
                interests = extract_interests(answer)
                self.assertIn("business", interests)
                self.assertIn("agriculture", interests)
                self.assertIn("social_sciences", interests)
                self.assertNotIn("health", interests)
                self.assertNotIn("social", extract_personality(answer))

    def test_subject_phrase_social_studies_is_not_personality_social(self):
        self.assertIn("social_studies", extract_subjects("Social Studies"))
        self.assertNotIn("social", extract_personality("Social Studies"))
        self.assertNotIn("social", extract_personality("I am interested in social studies"))

    def test_farmer_career_synonyms_are_recognized(self):
        examples = [
            "farmer",
            "I want to be a farmer",
            "I want to become a farmer",
            "I would like to become a farmer",
            "I hope to work as a crop farmer",
            "I want to manage a farm",
            "I want to be an agriculturist",
            "I want to be an agronomist",
            "I want to work in farming",
            "I want to raise livestock",
        ]
        for answer in examples:
            with self.subTest(answer=answer):
                self.assertIn("farmer", extract_career_goals(answer))

    def test_farmer_career_goal_does_not_automatically_become_interest(self):
        self.assertNotIn("agriculture", extract_interests("I want to become a farmer"))
        self.assertIn("agriculture", extract_interests("I want to become a farmer and I enjoy farming"))

    def test_farmer_goal_matches_agriculture_programmes(self):
        profile = StudentProfile(career_goals=["farmer"])
        recommendations = RecommendationEngine().recommend(profile)
        self.assertTrue(recommendations)
        self.assertTrue(any(
            item["course"].faculty == "Agriculture & Agricultural Technology"
            or "agriculture" in item["course"].interests
            for item in recommendations
        ))

    def test_farmer_goal_does_not_match_when_negated_or_only_as_an_interest(self):
        self.assertNotIn("farmer", extract_career_goals("I don't want to be a farmer"))
        self.assertNotIn("farmer", extract_career_goals("I do not want to become a farmer"))
        self.assertNotIn("farmer", extract_career_goals("I enjoy crop science"))
        self.assertNotIn("farmer", extract_career_goals("I enjoy farming"))
        self.assertIn("farmer", extract_career_goals("I want to work in farming"))

    def test_general_helping_people_is_not_automatically_health(self):
        interests = extract_interests("I enjoy helping people")
        self.assertIn("community", interests)
        self.assertNotIn("health", interests)

    def test_common_spelling_variants(self):
        self.assertIn("economics", extract_subjects("economcs"))
        self.assertIn("agricultural science", extract_subjects("agricultural science"))
        self.assertIn("agriculture", extract_interests("agriclture"))

    def test_personality_traits_are_not_interests(self):
        for answer in ["I am creative and patient", "I am very analytical", "I consider myself social"]:
            with self.subTest(answer=answer):
                self.assertEqual(extract_interests(answer), [])

    def test_career_goal_doctor_does_not_become_health_interest(self):
        self.assertEqual(extract_career_goals("I want to become a doctor"), ["doctor"])
        self.assertNotIn("health", extract_interests("I want to become a doctor"))

    def test_full_interview_stores_interest_and_career_in_separate_fields(self):
        bot = ChatbotEngine()
        bot.start()
        for answer in [
            "Amina",
            "economics agriculture and social studies",
            "Economics, Agricultural Science and Social Studies",
            "communication",
            "patient",
            "I want to become a farmer",
            "280",
            "nothing else",
        ]:
            result = bot.process_answer(answer)
            self.assertFalse(isinstance(result, dict) and result.get("type") == "unclear", (answer, result))

        self.assertIn("business", bot.profile.interests)
        self.assertIn("agriculture", bot.profile.interests)
        self.assertIn("social_sciences", bot.profile.interests)
        self.assertNotIn("health", bot.profile.interests)
        self.assertIn("farmer", bot.profile.career_goals)
        self.assertEqual(bot.profile.jamb_score, 280)


if __name__ == "__main__":
    unittest.main()
