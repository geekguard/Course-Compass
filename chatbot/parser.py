"""
parser.py

Extracts useful information from the student's
natural-language responses.
"""

import re
from functools import lru_cache
from difflib import get_close_matches

from data.keywords import (
    INTEREST_KEYWORDS,
    SUBJECT_KEYWORDS,
    SKILL_KEYWORDS,
    PERSONALITY_KEYWORDS,
    CAREER_KEYWORDS,
    SPELLING_CORRECTIONS,
    NATURAL_LANGUAGE_PHRASES,
)


# ==========================================================
# TEXT UTILITIES
# ==========================================================

def clean_text(text: str) -> str:
    """
    Convert text to lowercase, correct common spelling
    mistakes and remove unnecessary punctuation.
    """

    if not isinstance(text, str):
        return ""

    text = text.lower().strip()

    # Correct known spelling mistakes
    text = correct_spelling(text)

    text = re.sub(
        r"[^\w\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def correct_spelling(text: str) -> str:
    """
    Correct common spelling mistakes before keyword extraction.

    First checks the controlled spelling dictionary.
    If no direct correction exists, fuzzy matching is used
    against words already known by Course Compass.
    """

    if not isinstance(text, str):
        return ""

    words = text.split()

    vocabulary = get_known_words()

    corrected_words = []

    for word in words:

        # ----------------------------------------------
        # Remove punctuation temporarily
        # ----------------------------------------------

        punctuation = ""

        while word and not word[-1].isalnum():
            punctuation = word[-1] + punctuation
            word = word[:-1]

        cleaned_word = word.lower()

        # ----------------------------------------------
        # Direct spelling correction
        # ----------------------------------------------

        if cleaned_word in SPELLING_CORRECTIONS:

            corrected_word = SPELLING_CORRECTIONS[
                cleaned_word
            ]

        # ----------------------------------------------
        # Fuzzy spelling correction
        # ----------------------------------------------

        else:

            corrected_word = fuzzy_correct_word(
                cleaned_word,
                vocabulary
            )

        corrected_words.append(
            corrected_word + punctuation
        )

    return " ".join(corrected_words)


COMMON_WORDS = {
    "about", "after", "again", "also", "always", "because", "before",
    "being", "could", "doing", "enjoy", "every", "from", "good", "have",
    "here", "into", "just", "know", "like", "many", "more", "most",
    "much", "never", "only", "other", "patient", "people", "really",
    "should", "since", "some", "than", "that", "their", "them", "then",
    "there", "these", "they", "this", "those", "through", "very",
    "want", "well", "were", "what", "when", "where", "which", "while",
    "with", "would", "your", "creative", "interested", "interest",
    "social", "studies", "study", "economic", "economics", "agriculture",
    "agricultural", "farmer", "farmers", "farming", "crop", "crops",
    "livestock", "society", "science", "health", "career", "goal",
}

def fuzzy_correct_word(word: str, vocabulary: list) -> str:
    """
    Find a close match for a misspelled word.

    Only corrects the word when the match is sufficiently
    close to avoid changing unrelated words.
    """

    if not word:
        return word

    word = word.lower()
    # Avoid rewriting short/common English words into unrelated keywords.
    if len(word) < 5 or word in COMMON_WORDS:
        return word

    matches = get_close_matches(
        word,
        vocabulary,
        n=1,
        cutoff=0.84
    )

    if matches:
        return matches[0]

    return word


@lru_cache(maxsize=1)
def get_known_words():
    """
    Build a list of words that Course Compass already knows.
    """

    vocabulary = set()

    dictionaries = [
        INTEREST_KEYWORDS,
        SUBJECT_KEYWORDS,
        SKILL_KEYWORDS,
        PERSONALITY_KEYWORDS,
        CAREER_KEYWORDS,
    ]

    for dictionary in dictionaries:

        for keywords in dictionary.values():

            for keyword in keywords:

                words = keyword.lower().split()

                for word in words:

                    if len(word) >= 4:
                        vocabulary.add(word)

    return tuple(sorted(vocabulary))



def split_response(text: str):
    """
    Split a response containing commas or 'and'.
    """

    text = clean_text(text)

    text = text.replace(
        " and ",
        ","
    )

    return [
        item.strip()
        for item in text.split(",")
        if item.strip()
    ]


# ==========================================================
# KEYWORD MATCHING
# ==========================================================

def _is_negated_occurrence(text: str, start: int) -> bool:
    """Detect common negation immediately before a matched keyword."""
    prefix = text[:start]
    contrasts = list(re.finditer(r"\b(?:but|however|although|yet)\b", prefix))
    if contrasts:
        prefix = prefix[contrasts[-1].end():]

    negation = re.search(
        r"(?:not interested in|not keen on|no interest in|not a fan of|"
        r"not into|do not like|don t like|does not like|doesn t like|"
        r"do not enjoy|don t enjoy|does not enjoy|doesn t enjoy|"
        r"dislike|hate|do not want to become|don t want to become|"
        r"do not want to be|don t want to be|do not want|don t want|"
        r"never want to|never liked)(?:\s+(?:a|an))?\s*$",
        prefix,
    )
    return negation is not None


def _contains_keyword(text: str, keyword: str) -> bool:
    keyword = clean_text(keyword)
    if not keyword:
        return False

    pattern = re.compile(r"(?<!\w)" + re.escape(keyword) + r"(?!\w)")
    return any(
        not _is_negated_occurrence(text, match.start())
        for match in pattern.finditer(text)
    )


def _extract_keywords(
    text: str,
    keyword_dictionary: dict
):

    text = clean_text(text)

    matches = []

    for category, keywords in keyword_dictionary.items():

        for keyword in keywords:

            if _contains_keyword(
                text,
                keyword
            ):

                if category not in matches:
                    matches.append(category)

                break

    return matches


# ==========================================================
# PHRASE MATCHING
# ==========================================================

def _contains_any_phrase(
    text: str,
    phrases
) -> bool:

    text = clean_text(text)

    for phrase in phrases:

        if _contains_keyword(
            text,
            phrase
        ):
            return True

    return False

def extract_natural_language_interests(text: str):
    """
    Identify interests expressed using natural sentences.
    """

    text = clean_text(text)

    matches = []

    for category, phrases in NATURAL_LANGUAGE_PHRASES.items():

        for phrase in phrases:

            if _contains_keyword(text, phrase):

                if category not in matches:
                    matches.append(category)

                break

    return matches


# ==========================================================
# NAME EXTRACTION
# ==========================================================

def extract_name(text: str):
    """
    Extract a student's name from natural language.

    Examples:

        Aisha
        My name is Aisha
        My nam is Aisha
        My nane is Aisha
        I'm Aisha
        Im Aisha
        I am Aisha
        Call me Aisha
        Name is Aisha
        It's Aisha
    """

    if not isinstance(text, str):
        return ""

    original = text.strip()

    if not original:
        return ""

    # ------------------------------------------------------
    # Common responses that are NOT names
    # ------------------------------------------------------

    invalid_names = {
        "hello",
        "hi",
        "hey",
        "hello there",
        "hi there",
        "yes",
        "no",
        "okay",
        "ok",
        "sure",
        "fine",
        "good",
        "continue",
        "skip",
        "skip this",
        "i dont know",
        "i don't know",
        "not sure",
    }

    cleaned = clean_text(original)

    if cleaned in invalid_names:
        return ""

    # ------------------------------------------------------
    # Prefixes
    #
    # Includes intentional common typing mistakes.
    # ------------------------------------------------------

    patterns = [
        r"\bmy\s+name\s+is\s+(.+)",
        r"\bmy\s+nam\s+is\s+(.+)",
        r"\bmy\s+nane\s+is\s+(.+)",
        r"\bmy\s+name\s+(.+)",
        r"\bmy\s+nam\s+(.+)",
        r"\bname\s+is\s+(.+)",
        r"\bi\s+am\s+(.+)",
        r"\bi'm\s+(.+)",
        r"\bim\s+(.+)",
        r"\bcall\s+me\s+(.+)",
        r"\bit's\s+(.+)",
        r"\bits\s+(.+)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            original,
            re.IGNORECASE
        )

        if match:

            name = match.group(1).strip()

            # Remove common trailing punctuation
            name = re.sub(
                r"[.!?,]+$",
                "",
                name
            ).strip()

            # A name should not be an extremely long sentence
            words = name.split()

            if 1 <= len(words) <= 4:

                if all(
                    re.fullmatch(
                        r"[A-Za-zÀ-ÿ'-]+",
                        word
                    )
                    for word in words
                ):

                    return name.title()

    # ------------------------------------------------------
    # If the student simply types their name
    # ------------------------------------------------------

    simple_name = re.sub(
        r"[.!?,]+$",
        "",
        original
    ).strip()

    words = simple_name.split()

    if 1 <= len(words) <= 4:

        if all(
            re.fullmatch(
                r"[A-Za-zÀ-ÿ'-]+",
                word
            )
            for word in words
        ):

            if clean_text(simple_name) not in invalid_names:

                return simple_name.title()

    return ""


# ==========================================================
# INDIVIDUAL EXTRACTORS
# ==========================================================

def extract_interests(text: str):
    """Extract interest areas while keeping career and personality language separate."""
    if not isinstance(text, str):
        return []

    interest_text = clean_text(text)

    # A career aspiration is not automatically an interest. Keep other
    # explicitly stated interests in the same sentence, if present.
    career_intent = re.search(
        r"\b(?:i want to|i wanted to|i would like to|i hope to|"
        r"i plan to|i aspire to|i dream of|i wish to|my goal is to|"
        r"my career goal is to|i hope i can|i see myself as)\b",
        interest_text,
    ) is not None
    if career_intent:
        # Do not remove activity phrases such as "farming" or "planting crops"
        # from a sentence that also expresses an interest ("I want to be a farmer
        # and I enjoy farming"). Remove occupational labels from the aspiration
        # sentence, but leave activity/subject phrases available to the interest
        # matcher.
        interest_activity_terms = {
            "farming", "farm work", "planting crops", "crop production",
            "livestock production", "animal husbandry", "raising farm animals",
            "crop grower", "agribusiness owner",
        }
        career_terms = sorted(
            {
                clean_text(term)
                for terms in CAREER_KEYWORDS.values()
                for term in terms
                if clean_text(term) and clean_text(term) not in interest_activity_terms
            },
            key=len,
            reverse=True,
        )
        for term in career_terms:
            interest_text = re.sub(
                r"(?<!\w)" + re.escape(term) + r"(?!\w)",
                " ",
                interest_text,
            )

    # Remove personality traits only when they are directly stated as traits.
    # The old broad check for "I am" also triggered on "I am interested in..."
    # and then removed the word "social" from "social studies".
    trait_terms = sorted(
        {clean_text(term) for terms in PERSONALITY_KEYWORDS.values() for term in terms if clean_text(term)},
        key=len,
        reverse=True,
    )
    trait_alternation = "|".join(re.escape(term) for term in trait_terms)
    if trait_alternation:
        personality_clause = re.compile(
            r"\b(?:i am|i'm|im|i consider myself|my personality is|"
            r"i would describe myself as)\s+"
            r"(?:(?:very|quite|really|generally|a|an)\s+)*(?:"
            + trait_alternation
            + r")(?:\s*(?:,|and)\s*(?:(?:very|quite|really)\s+)*(?:"
            + trait_alternation
            + r"))*\b"
        )
        interest_text = personality_clause.sub(" ", interest_text)

    interest_text = re.sub(r"\s+", " ", interest_text).strip()
    matches = _extract_keywords(interest_text, INTEREST_KEYWORDS)
    for category in extract_natural_language_interests(interest_text):
        if category not in matches:
            matches.append(category)
    return matches


def extract_subjects(text: str):

    return _extract_keywords(
        text,
        SUBJECT_KEYWORDS
    )


def extract_skills(text: str):
    """Extract skills while avoiding overlap between coding and writing.

    The phrase "writing code" is a coding skill; the word "writing" alone
    should not also imply communication unless the student states another
    communication-related skill or phrase.
    """
    matches = _extract_keywords(text, SKILL_KEYWORDS)
    cleaned = clean_text(text)

    if "coding" in matches and _contains_keyword(cleaned, "writing code"):
        communication_aliases = [
            alias for alias in SKILL_KEYWORDS.get("communication", [])
            if alias.lower() != "writing"
        ]
        explicit_communication = any(
            _contains_keyword(cleaned, alias)
            for alias in communication_aliases
        )
        if not explicit_communication:
            matches = [item for item in matches if item != "communication"]

    return matches


def extract_personality(text: str):
    """Extract personality traits without treating school subjects as traits.

    In particular, "social studies" and "social sciences" contain the word
    "social", but naming either subject does not mean the student described
    their personality as social.
    """
    if not isinstance(text, str):
        return []

    trait_text = clean_text(text)
    trait_text = re.sub(
        r"\b(?:social studies|social science|social sciences)\b",
        " ",
        trait_text,
    )
    return _extract_keywords(trait_text, PERSONALITY_KEYWORDS)


def extract_career_goals(text: str):
    """Extract career goals without turning every interest activity into a job goal.

    A bare answer such as "farmer" or "farming" is accepted when the bot asks
    for a career. But in a sentence like "I enjoy farming", the wording signals
    an interest rather than a declared career goal.
    """
    if not isinstance(text, str):
        return []

    cleaned = clean_text(text)
    matches = _extract_keywords(cleaned, CAREER_KEYWORDS)
    if not matches:
        return []

    explicit_career_intent = re.search(
        r"\b(?:i want to|i wanted to|i would like to|i hope to|"
        r"i plan to|i aspire to|i dream of|i wish to|my goal is to|"
        r"my career goal is to|i see myself as|my ambition is to|"
        r"as a career|as my profession)\b",
        cleaned,
    ) is not None
    interest_intent = re.search(
        r"\b(?:i like|i enjoy|i love|i am interested in|im interested in|"
        r"i m interested in|i am into|im into|i m into|i am passionate about|"
        r"i enjoy learning about)\b",
        cleaned,
    ) is not None

    if "farmer" in matches and interest_intent and not explicit_career_intent:
        activity_phrases = (
            "farming", "farm work", "planting crops", "growing crops",
            "crop production", "livestock", "animal husbandry",
            "raising farm animals", "raise livestock",
        )
        if any(phrase in cleaned for phrase in activity_phrases):
            matches = [item for item in matches if item != "farmer"]

    # A specific occupational title is more useful than also recording its
    # generic parent category. This avoids a redundant "software engineer and
    # engineer" explanation and duplicate-looking career matches.
    if "software engineer" in matches and "engineer" in matches:
        matches = [item for item in matches if item != "engineer"]

    # Keep the extracted career list stable and unique even if multiple aliases
    # from one category appear in the same sentence.
    return list(dict.fromkeys(matches))


# ==========================================================
# JAMB SCORE
# ==========================================================

def extract_jamb_score(text: str):
    """
    Extract JAMB/UTME score only when the response
    clearly refers to JAMB or UTME.
    """

    if not isinstance(text, str):
        return 0

    cleaned = clean_text(text)

    jamb_phrases = [
        "jamb",
        "utme",
        "score",
        "jamb score",
        "utme score",
        "score in jamb",
        "score in utme",
        "scored in jamb",
        "scored in utme",
        "i scored",
    ]

    if not _contains_any_phrase(
        cleaned,
        jamb_phrases
    ):
        return 0

    numbers = re.findall(
        r"\b\d{1,3}\b",
        cleaned
    )

    if not numbers:
        return 0

    score = int(
        numbers[0]
    )

    if score < 0:
        return 0

    if score > 400:
        return 0

    return score


# ==========================================================
# EXTRACT EVERYTHING
# ==========================================================

def extract_all_information(text: str) -> dict:
    """
    Extract every supported type of information from
    one response.
    """

    if not isinstance(text, str):
        text = ""

    return {
        "interests": extract_interests(text),

        "subjects": extract_subjects(text),

        "skills": extract_skills(text),

        "personality_traits": extract_personality(text),

        "career_goals": extract_career_goals(text),

        "jamb_score": extract_jamb_score(text),
    }


# ==========================================================
# CHECK INFORMATION
# ==========================================================

def has_information(text: str) -> bool:
    """
    Return True when the response contains recognizable
    profile information.
    """

    information = extract_all_information(
        text
    )

    for key, value in information.items():

        if key == "jamb_score":

            if value > 0:
                return True

        elif value:

            return True

    return False

if __name__ == "__main__":

    tests = [
        "I like physcs",
        "I like chemstry",
        "I enjoy biolog",
        "I like enginering",
        "I enjoy programng",
        "I like maths and physics",
    ]

    for test in tests:

        print("Original:", test)
        print("Corrected:", clean_text(test))
        print("Subjects:", extract_subjects(test))
        print("Interests:", extract_interests(test))
        print("-" * 40)