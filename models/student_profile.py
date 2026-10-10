"""
student_profile.py

Stores and manages information collected from a student
during the Course Compass conversation.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class StudentProfile:
    """
    Represents the student's personal, academic and
    career information.

    The profile can be updated throughout the conversation,
    including when the student remembers additional information.
    """

    # ==========================================================
    # BASIC INFORMATION
    # ==========================================================

    name: str = ""

    # ==========================================================
    # ACADEMIC INFORMATION
    # ==========================================================

    favourite_subjects: List[str] = field(default_factory=list)
    jamb_score: int = 0

    # ==========================================================
    # INTERESTS AND SKILLS
    # ==========================================================

    interests: List[str] = field(default_factory=list)
    hobbies: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)

    # ==========================================================
    # PERSONALITY
    # ==========================================================

    personality_traits: List[str] = field(default_factory=list)
    preferred_work_style: str = ""

    # ==========================================================
    # CAREER
    # ==========================================================

    career_goals: List[str] = field(default_factory=list)

    # ==========================================================
    # SELF-ASSESSMENT
    # ==========================================================

    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)

    # ==========================================================
    # CONFIDENCE
    # ==========================================================

    confidence_score: int = 0

    # ==========================================================
    # NORMALIZATION
    # ==========================================================

    def __post_init__(self):
        """
        Normalize list values when the profile is created.
        """

        self.interests = self._normalize(self.interests)

        self.favourite_subjects = self._normalize(
            self.favourite_subjects
        )

        self.skills = self._normalize(
            self.skills
        )

        self.personality_traits = self._normalize(
            self.personality_traits
        )

        self.career_goals = self._normalize(
            self.career_goals
        )

        self.hobbies = self._normalize(
            self.hobbies
        )

        self.strengths = self._normalize(
            self.strengths
        )

        self.weaknesses = self._normalize(
            self.weaknesses
        )

        self.calculate_confidence()

    # ==========================================================
    # NORMALIZATION HELPER
    # ==========================================================

    @staticmethod
    def _normalize(items: List[str]) -> List[str]:
        """
        Convert values to lowercase and remove duplicates
        while preserving their original order.
        """

        seen = set()
        cleaned = []

        for item in items:

            if not isinstance(item, str):
                continue

            value = item.strip().lower()

            if value and value not in seen:

                cleaned.append(value)

                seen.add(value)

        return cleaned

    # ==========================================================
    # ADD INFORMATION
    # ==========================================================

    def add_items(
        self,
        field_name: str,
        items: List[str]
    ):
        """
        Add new information to one of the profile's list fields.

        Existing information is kept.

        Returns the number of genuinely new items added.
        """

        if not hasattr(self, field_name):

            return 0

        current = getattr(
            self,
            field_name
        )

        if not isinstance(current, list):

            return 0

        added = 0

        for item in items:

            if not isinstance(item, str):
                continue

            value = item.strip().lower()

            if value and value not in current:

                current.append(value)

                added += 1

        # Recalculate confidence whenever
        # new information is added.

        self.calculate_confidence()

        return added

    # ==========================================================
    # UPDATE MULTIPLE PROFILE FIELDS
    # ==========================================================

    def update_information(
        self,
        interests=None,
        subjects=None,
        skills=None,
        personality=None,
        careers=None
    ):
        """
        Merge newly discovered information into the student's
        existing profile.

        Existing information is preserved and duplicate values
        are ignored.
        """

        if interests:
            self.add_items(
                "interests",
                interests
            )

        if subjects:
            self.add_items(
                "favourite_subjects",
                subjects
            )

        if skills:
            self.add_items(
                "skills",
                skills
            )

        if personality:
            self.add_items(
                "personality_traits",
                personality
            )

        if careers:
            self.add_items(
                "career_goals",
                careers
            )

        self.calculate_confidence()

    # ==========================================================
    # UPDATE JAMB SCORE
    # ==========================================================

    def update_jamb_score(
        self,
        score: int
    ):
        """
        Update the student's JAMB score.
        """

        if not isinstance(score, int):

            return

        if score < 1 or score > 400:
            return

        self.jamb_score = score

        self.calculate_confidence()

    # ==========================================================
    # CONFIDENCE CALCULATION
    # ==========================================================

    def calculate_confidence(self) -> int:
        """Estimate profile completeness, not the probability of a correct match.

        Each category has a fixed maximum weight. Additional distinct items in a
        category improve completeness gradually, so useful information added
        after the interview can raise the score even when that category already
        contained one answer. The total is always capped at 100.
        """

        def capped_items(items, first_item_points, extra_item_points, maximum):
            if not items:
                return 0
            return min(maximum, first_item_points + (len(items) - 1) * extra_item_points)

        score = 0
        if self.name:
            score += 5

        score += capped_items(self.favourite_subjects, 10, 5, 20)
        score += capped_items(self.interests, 10, 5, 20)
        score += capped_items(self.skills, 8, 4, 15)
        score += capped_items(self.personality_traits, 5, 3, 10)
        score += capped_items(self.career_goals, 12, 4, 20)

        if self.jamb_score > 0:
            score += 10

        self.confidence_score = max(0, min(score, 100))
        return self.confidence_score

    # ==========================================================
    # RESET
    # ==========================================================

    def reset(self):
        """
        Clear all student information so a new recommendation
        can begin.
        """

        self.name = ""

        self.jamb_score = 0

        self.preferred_work_style = ""

        self.favourite_subjects.clear()

        self.interests.clear()

        self.hobbies.clear()

        self.skills.clear()

        self.personality_traits.clear()

        self.career_goals.clear()

        self.strengths.clear()

        self.weaknesses.clear()

        self.confidence_score = 0

    # ==========================================================
    # PROFILE SUMMARY
    # ==========================================================

    def get_summary(self) -> dict:
        """
        Return the information collected from the student.
        """

        return {
            "name": self.name,

            "favourite_subjects":
                self.favourite_subjects,

            "interests":
                self.interests,

            "skills":
                self.skills,

            "personality_traits":
                self.personality_traits,

            "career_goals":
                self.career_goals,

            "jamb_score":
                self.jamb_score,

            "confidence_score":
                self.confidence_score,
        }

    # ==========================================================
    # CONVERT TO DICTIONARY
    # ==========================================================

    def to_dict(self) -> dict:
        """
        Convert the complete profile into a dictionary.
        """

        return {

            "name":
                self.name,

            "favourite_subjects":
                self.favourite_subjects,

            "jamb_score":
                self.jamb_score,

            "interests":
                self.interests,

            "hobbies":
                self.hobbies,

            "skills":
                self.skills,

            "personality_traits":
                self.personality_traits,

            "preferred_work_style":
                self.preferred_work_style,

            "career_goals":
                self.career_goals,

            "strengths":
                self.strengths,

            "weaknesses":
                self.weaknesses,

            "confidence_score":
                self.confidence_score,
        }

    # ==========================================================
    # COMPLETION
    # ==========================================================

    def completion_percentage(self) -> int:
        """
        Estimate how much of the main student profile
        has been completed.
        """

        fields = [

            self.name,

            self.favourite_subjects,

            self.interests,

            self.skills,

            self.personality_traits,

            self.career_goals,

            self.jamb_score,
        ]

        completed = sum(
            bool(field)
            for field in fields
        )

        return round(
            (completed / len(fields)) * 100
        )


    # ==========================================================
    # STRING REPRESENTATION
    # ==========================================================

    def __str__(self):

        interests = (
            ", ".join(self.interests)
            if self.interests
            else "None"
        )

        subjects = (
            ", ".join(self.favourite_subjects)
            if self.favourite_subjects
            else "None"
        )

        skills = (
            ", ".join(self.skills)
            if self.skills
            else "None"
        )

        career_goals = (
            ", ".join(self.career_goals)
            if self.career_goals
            else "None"
        )

        return (
            f"{self.name} | "
            f"Interests: {interests} | "
            f"Subjects: {subjects} | "
            f"Skills: {skills} | "
            f"Career Goals: {career_goals} | "
            f"Confidence: {self.confidence_score}%"
        )

    # ==========================================================
    # DEVELOPER REPRESENTATION
    # ==========================================================

    def __repr__(self):

        return (

            f"StudentProfile("

            f"name='{self.name}', "

            f"subjects={self.favourite_subjects}, "

            f"interests={self.interests}, "

            f"skills={self.skills}, "

            f"career_goals={self.career_goals}, "

            f"confidence_score={self.confidence_score})"
        )