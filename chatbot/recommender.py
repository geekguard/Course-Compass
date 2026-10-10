"""
recommender.py

Generates course recommendations based on a student's profile.

Course Compass uses a rules-based recommendation approach.
The engine compares the student's information with the
attributes stored for each course and produces both a score
and human-readable reasons for the recommendation.
"""

from data.courses import COURSES


class RecommendationEngine:
    """
    Matches a student's profile with available courses.
    """

    def __init__(self):
        self.courses = COURSES

    # ==========================================================
    # HELPER: FORMAT LIST
    # ==========================================================

    @staticmethod
    def _format_items(items):
        """
        Convert a list of values into readable text.

        Example:
            ["biology", "chemistry"]
        becomes:
            "Biology and Chemistry"
        """

        if not items:
            return ""

        formatted = [
            item.replace("_", " ").title()
            for item in items
        ]

        if len(formatted) == 1:
            return formatted[0]

        if len(formatted) == 2:
            return f"{formatted[0]} and {formatted[1]}"

        return (
            ", ".join(formatted[:-1])
            + f", and {formatted[-1]}"
        )

    # ==========================================================
    # CALCULATE SCORE
    # ==========================================================

    def _calculate_score(self, profile, course):
        """
        Calculate a course match score out of 100.

        Weighting:
            Career goals : 30
            Subjects     : 20
            Interests    : 20
            Skills       : 15
            Personality  : 10
            JAMB score   : 5
        """

        score = 0
        reasons = []
        match_details = []

        # ======================================================
        # 1. CAREER GOAL - 30 POINTS
        # ======================================================

        career_matches = [
            goal
            for goal in profile.career_goals
            if course.matches_career(goal)
        ]

        if career_matches:
            score += 30

            career_text = self._format_items(career_matches)

            reasons.append(
                f"Your career goal of becoming a {career_text} "
                f"aligns closely with this programme and its "
                f"career path."
            )

            match_details.append(
                f"career goal ({career_text})"
            )

        # ======================================================
        # 2. FAVOURITE SUBJECTS - 20 POINTS
        # ======================================================

        subject_matches = [
            subject
            for subject in profile.favourite_subjects
            if course.matches_subject(subject)
        ]

        if subject_matches:
            subject_points = min(
                len(subject_matches) * 10,
                20
            )

            score += subject_points

            subject_text = self._format_items(subject_matches)

            reasons.append(
                f"Your favourite subject choice of {subject_text} gives you a "
                f"good academic connection with this programme."
            )

            match_details.append(
                f"subject match ({subject_text})"
            )

        # ======================================================
        # 3. INTERESTS - 20 POINTS
        # ======================================================

        interest_matches = [
            interest
            for interest in profile.interests
            if course.matches_interest(interest)
        ]

        if interest_matches:
            interest_points = min(
                len(interest_matches) * 10,
                20
            )

            score += interest_points

            interest_text = self._format_items(interest_matches)

            reasons.append(
                f"Your interest in {interest_text} fits well "
                f"with the focus of this programme."
            )

            match_details.append(
                f"interest match ({interest_text})"
            )

        # ======================================================
        # 4. SKILLS - 15 POINTS
        # ======================================================

        skill_matches = [
            skill
            for skill in profile.skills
            if course.matches_skill(skill)
        ]

        if skill_matches:
            skill_points = min(
                len(skill_matches) * 5,
                15
            )

            score += skill_points

            skill_text = self._format_items(skill_matches)

            reasons.append(
                f"Your {skill_text} {('skill' if len(skill_matches) == 1 else 'skills')} "
                f"can be useful in this field."
            )

            match_details.append(
                f"skill match ({skill_text})"
            )

        # ======================================================
        # 5. PERSONALITY - 10 POINTS
        # ======================================================

        personality_matches = []

        for trait in profile.personality_traits:
            try:
                matched = course.matches_personality(trait)
            except AttributeError:
                matched = trait.lower() in getattr(
                    course,
                    "personality_traits",
                    []
                )

            if matched:
                personality_matches.append(trait)

        if personality_matches:
            personality_points = min(
                len(personality_matches) * 5,
                10
            )

            score += personality_points

            personality_text = self._format_items(
                personality_matches
            )

            reasons.append(
                f"Your {personality_text} approach to work and learning "
                f"also fits the demands of this programme."
            )

            match_details.append(
                f"personality match ({personality_text})"
            )

        # ======================================================
        # 6. JAMB SCORE - 5 POINTS
        # ======================================================

        if profile.jamb_score > 0:
            if course.jamb_cutoff is None:
                reasons.append(
                    "A current programme-specific JAMB cut-off has not been "
                    "verified in this dataset. Confirm the current requirement "
                    "with ATBU and JAMB before making an application decision."
                )
            elif profile.jamb_score >= course.jamb_cutoff:
                score += 5

                reasons.append(
                    f"Your JAMB score of {profile.jamb_score} "
                    f"meets or exceeds the stored reference cut-off of "
                    f"{course.jamb_cutoff}. This is not a guarantee of admission."
                )

                match_details.append("stored JAMB reference cut-off met")

            else:
                reasons.append(
                    f"Your JAMB score of {profile.jamb_score} "
                    f"is below the stored reference cut-off of {course.jamb_cutoff}. "
                    f"This does not remove the programme from consideration, "
                    f"but you should verify current requirements before applying."
                )

        # ======================================================
        # 7. COMBINED PROFILE REASONING
        # ======================================================

        total_profile_matches = (
            len(career_matches)
            + len(subject_matches)
            + len(interest_matches)
            + len(skill_matches)
            + len(personality_matches)
        )

        if total_profile_matches >= 5:
            reasons.append(
                "Several important parts of your profile point "
                "toward this same field, making it one of your "
                "stronger matches."
            )

        elif career_matches and (
            subject_matches or interest_matches
        ):
            reasons.append(
                "Your career direction and academic or personal "
                "interests are pointing toward the same field."
            )

        elif subject_matches and skill_matches:
            reasons.append(
                "Your academic interests and strengths complement "
                "each other well for this programme."
            )

        elif interest_matches and personality_matches:
            reasons.append(
                "What you enjoy and the way you naturally approach "
                "tasks both fit this programme."
            )

        # ======================================================
        # 8. OVERALL EXPLANATION
        # ======================================================

        if match_details:
            if len(match_details) == 1:
                overall_reason = (
                    "This recommendation is mainly supported by your "
                    + match_details[0]
                    + "."
                )
            elif len(match_details) == 2:
                overall_reason = (
                    "This recommendation is supported by your "
                    + match_details[0]
                    + " and "
                    + match_details[1]
                    + "."
                )
            else:
                overall_reason = (
                    "This recommendation is supported by your "
                    + ", ".join(match_details[:-1])
                    + ", and "
                    + match_details[-1]
                    + "."
                )

            reasons.insert(0, overall_reason)

        # ======================================================
        # 9. NO MATCH
        # ======================================================

        if not reasons:
            reasons.append(
                "There was not enough matching information to identify "
                "a strong specific connection between your profile and "
                "this programme."
            )

        # ======================================================
        # 10. KEEP SCORE IN RANGE
        # ======================================================

        score = max(0, min(score, 100))

        return score, reasons

    # ==========================================================
    # RECOMMEND COURSES
    # ==========================================================

    def recommend(self, profile, top_n=5):
        """Return the best programmes with at least one profile-based match.

        A JAMB score alone is not enough to claim that a programme suits a
        student. The score is therefore used as supporting evidence only after
        a career, subject, interest, skill, or personality match exists.
        """
        recommendations = []

        for course in self.courses:
            profile_match = (
                any(course.matches_career(goal) for goal in profile.career_goals)
                or any(course.matches_subject(subject) for subject in profile.favourite_subjects)
                or any(course.matches_interest(interest) for interest in profile.interests)
                or any(course.matches_skill(skill) for skill in profile.skills)
                or any(course.matches_personality(trait) for trait in profile.personality_traits)
            )

            if not profile_match:
                continue

            score, reasons = self._calculate_score(profile, course)
            recommendations.append({
                "course": course,
                "score": score,
                "percentage": score,
                "reasons": reasons,
            })

        recommendations.sort(
            key=lambda item: (-item["score"], item["course"].name.casefold())
        )
        return recommendations[:max(0, int(top_n))]
