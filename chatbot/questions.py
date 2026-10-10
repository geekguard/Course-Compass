"""
questions.py

Stores the interview questions used by Course Compass.

The questions are intentionally conversational. The chatbot
will add a natural response after each student answer before
moving to the next question.
"""


QUESTIONS = [

    # ==========================================================
    # BASIC INFORMATION
    # ==========================================================

    {
        "id": "name",
        "question": (
            "Before we get started, what's your name? 😊"
        )
    },

    # ==========================================================
    # INTERESTS
    # ==========================================================

    {
        "id": "interests",
        "question": (
            "Now tell me about the things you genuinely enjoy.\n\n"
            "What kinds of things do you like doing, learning "
            "about or talking about?\n\n"
            "You can mention several things. For example: "
            "technology, medicine, science, business, art, "
            "helping people, nature or anything else you enjoy."
        )
    },

    # ==========================================================
    # SCHOOL SUBJECTS
    # ==========================================================

    {
        "id": "subjects",
        "question": (
            "What school subjects do you enjoy the most?\n\n"
            "You can mention more than one, such as Mathematics, "
            "Biology, Chemistry, Physics, English, Computer "
            "Science or Economics."
        )
    },

    # ==========================================================
    # SKILLS
    # ==========================================================

    {
        "id": "skills",
        "question": (
            "Your interests tell me what you enjoy, but "
            "your strengths tell me what you can actually do well.\n\n"
            "What skills are you confident in?\n\n"
            "For example: problem solving, coding, communication, "
            "leadership, teamwork, creativity, analysis or "
            "organization."
        )
    },

    # ==========================================================
    # PERSONALITY
    # ==========================================================

    {
        "id": "personality",
        "question": (
            "We're getting closer to your course profile. 😊\n\n"
            "How would you describe yourself when you work or "
            "learn?\n\n"
            "For example, are you analytical, creative, social, "
            "independent, organized, patient or confident?"
        )
    },

    # ==========================================================
    # CAREER GOAL
    # ==========================================================

    {
        "id": "career_goal",
        "question": (
            "There's one more thing I want to understand about "
            "your direction.\n\n"
            "If you could choose any career, what would you "
            "love to become?\n\n"
            "And don't worry if your answer doesn't perfectly "
            "match your hobbies or interests. People can have "
            "many different interests and still have a clear "
            "career goal."
        )
    },

    # ==========================================================
    # JAMB SCORE
    # ==========================================================

    {
        "id": "jamb_score",
        "question": (
            "Almost there! 🎓\n\n"
            "What is your JAMB score?\n\n"
            "Type 'skip' if you haven't written JAMB yet."
        )
    },

    # ==========================================================
    # ADDITIONAL INFORMATION
    # ==========================================================

    {
        "id": "additional_information",
        "question": (
            "Before I calculate your course recommendations, "
            "let's make sure I haven't missed anything important.\n\n"
            "Is there anything you forgot to tell me earlier?\n\n"
            "You could add another interest, subject, skill, "
            "personality trait or career goal.\n\n"
            "If you've already told me everything, just type "
            "'No' or 'That's all'."
        )
    }
]
