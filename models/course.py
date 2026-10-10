"""
course.py

Course model used by CourseCompass.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Course:
    """
    Represents a degree programme at ATBU.
    """

    name: str
    faculty: str
    department: str
    description: str

    # ==========================================================
    # COURSE MATCHING INFORMATION
    # ==========================================================

    interests: List[str] = field(default_factory=list)
    subjects: List[str] = field(default_factory=list)

    jamb_subjects: List[str] = field(default_factory=list)

    skills: List[str] = field(default_factory=list)
    personality_traits: List[str] = field(default_factory=list)
    careers: List[str] = field(default_factory=list)

    # ==========================================================
    # ADMISSION INFORMATION
    # ==========================================================

    jamb_cutoff: Optional[int] = 180

    # ATBU undergraduate default
    duration: str = "5 Years"

    degree: str = "B.Tech."

    # ==========================================================
    # NORMALIZATION
    # ==========================================================

    def __post_init__(self):

        self.interests = [
            i.lower()
            for i in self.interests
        ]

        self.subjects = [
            i.lower()
            for i in self.subjects
        ]

        self.jamb_subjects = [
            i.lower()
            for i in self.jamb_subjects
        ]

        self.skills = [
            i.lower()
            for i in self.skills
        ]

        self.personality_traits = [
            i.lower()
            for i in self.personality_traits
        ]

        self.careers = [
            i.lower()
            for i in self.careers
        ]

    # ==========================================================
    # MATCHING METHODS
    # ==========================================================

    def matches_interest(self, value):

        return value.lower() in self.interests

    def matches_subject(self, value):

        return value.lower() in self.subjects

    def matches_skill(self, value):

        return value.lower() in self.skills

    def matches_personality(self, value):
        return value.lower() in self.personality_traits

    def matches_career(self, value):
        """Match a career category to a specific career stored for the course.

        For example, a goal of "teacher" can match "science teacher" or
        "vocational teacher" without relying on fragile substring matching.
        "Software engineer" still matches its full phrase as expected.
        """
        if not isinstance(value, str):
            return False

        normalized = value.strip().lower()
        if not normalized:
            return False

        if normalized in self.careers:
            return True

        # Generic occupational categories can match a specific title, but keep
        # "doctor" exact so a human-doctor goal does not imply veterinary work.
        if normalized in {"teacher", "engineer", "scientist", "analyst"}:
            return any(normalized in career.split() for career in self.careers)

        # A student who wants to become a farmer may be interested in several
        # agriculture programmes, not just a course literally named "Farmer".
        # Match only courses explicitly tagged as agriculture or in ATBU's
        # Agriculture & Agricultural Technology faculty.
        if normalized == "farmer":
            return (
                "agriculture" in self.interests
                or self.faculty.strip().lower() == "agriculture & agricultural technology"
            )

        return False

    # ==========================================================
    # CONVERT TO DICTIONARY
    # ==========================================================

    def to_dict(self):

        return {

            "name": self.name,

            "faculty": self.faculty,

            "department": self.department,

            "description": self.description,

            "interests": self.interests,

            "subjects": self.subjects,

            "jamb_subjects": self.jamb_subjects,

            "skills": self.skills,

            "personality_traits": self.personality_traits,

            "careers": self.careers,

            "jamb_cutoff": self.jamb_cutoff,

            "duration": self.duration,

            "degree": self.degree

        }

    # ==========================================================
    # CREATE FROM DICTIONARY
    # ==========================================================

    @classmethod
    def from_dict(cls, data):

        return cls(

            name=data["name"],

            faculty=data["faculty"],

            department=data["department"],

            description=data["description"],

            interests=data.get(
                "interests",
                []
            ),

            subjects=data.get(
                "subjects",
                []
            ),

            jamb_subjects=data.get(
                "jamb_subjects",
                []
            ),

            skills=data.get(
                "skills",
                []
            ),

            personality_traits=data.get(
                "personality_traits",
                []
            ),

            careers=data.get(
                "careers",
                []
            ),

            jamb_cutoff=data.get(
                "jamb_cutoff",
                180
            ),

            duration=data.get(
                "duration",
                "5 Years"
            ),

            degree=data.get(
                "degree",
                "B.Tech."
            )

        )

    # ==========================================================
    # STRING REPRESENTATION
    # ==========================================================

    def __str__(self):

        return f"{self.name} ({self.degree})"