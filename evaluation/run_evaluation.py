"""Run a small deterministic evaluation set for Course Compass parsing.

This is a synthetic regression evaluation, not a substitute for testing with
real ATBU students. It measures exact category matches on manually labelled
examples and is intended to catch regressions before user tryouts.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Make `python evaluation/run_evaluation.py` work from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from chatbot.parser import (
    extract_interests,
    extract_subjects,
    extract_skills,
    extract_personality,
    extract_career_goals,
)

CASES = [
    ("interests", "I like coding", {"technology"}),
    ("interests", "I enjoy computers and robotics", {"technology"}),
    ("interests", "I enjoy medicine", {"health"}),
    ("interests", "I want to become a doctor", set()),
    ("interests", "I like drawing and painting", {"art"}),
    ("interests", "I enjoy business and marketing", {"business"}),
    ("interests", "I like economics", {"business"}),
    ("interests", "I am interested in economic issues", {"business"}),
    ("interests", "I like agriculture", {"agriculture"}),
    ("interests", "I enjoy farming", {"agriculture"}),
    ("interests", "I like growing crops", {"agriculture"}),
    ("interests", "I am interested in livestock", {"agriculture"}),
    ("interests", "I like social studies", {"social_sciences"}),
    ("interests", "I enjoy helping people", {"community"}),
    ("interests", "I enjoy farming", {"agriculture"}),
    ("interests", "I am interested in social studies", {"social_sciences"}),
    ("interests", "economics agriculture and social studies", {"business", "agriculture", "social_sciences"}),
    ("interests", "I am interested in economics, agriculture and social studies", {"business", "agriculture", "social_sciences"}),
    ("interests", "I am creative and patient", set()),
    ("interests", "I don't like medicine", set()),
    ("interests", "I enjoy nature and wildlife", {"environment", "wildlife_and_conservation"}),
    ("interests", "I like fashion and sewing", {"fashion", "crafts"}),
    ("subjects", "Maths and physcs", {"mathematics", "physics"}),
    ("subjects", "Economics and social studies", {"economics", "social_studies"}),
    ("subjects", "Agricultural science and biology", {"agricultural science", "biology"}),
    ("subjects", "English and literature in English", {"english", "literature", "literature_in_english"}),
    ("skills", "I am good at problem solving", {"problem solving"}),
    ("skills", "I can code and build apps", {"coding"}),
    ("skills", "I communicate well and work in teams", {"communication", "teamwork"}),
    ("personality", "I am creative and patient", {"creative", "patient"}),
    ("personality", "I consider myself analytical and independent", {"analytical", "independent"}),
    ("personality", "I am interested in social studies", set()),
    ("career", "I want to be a farmer", {"farmer"}),
    ("career", "I want to become a teacher", {"teacher"}),
    ("career", "I hope to become a software developer", {"software engineer"}),
    ("career", "I would like to be a nurse", {"nurse"}),
    ("career", "I don't want to be a doctor", set()),
    ("career", "I want to work as a crop farmer", {"farmer"}),
    ("career", "I enjoy farming", set()),
    ("career", "I want to become an accountant", {"accountant"}),
    ("career", "I want to be an engineer", {"engineer"}),
    ("interests", "I am interested in building websites", {"technology"}),
    ("interests", "I enjoy creating websites", {"technology"}),
    ("interests", "I like building things", {"engineering"}),
    ("interests", "I do not enjoy farming", set()),
    ("interests", "I love animals and wildlife", {"environment", "wildlife_and_conservation"}),
    ("interests", "I like helping my community", {"community"}),
    ("interests", "I do not like medicine but I enjoy farming", {"agriculture"}),
    ("interests", "I want to become a doctor and I enjoy drawing", {"art"}),
    ("subjects", "I enjoy chemistry and physics", {"physics", "chemistry"}),
    ("subjects", "I like biology and mathematics", {"mathematics", "biology"}),
    ("subjects", "English language and government", {"english", "government"}),
    ("skills", "I can solve problems and analyse data", {"problem solving", "analytical"}),
    ("skills", "I communicate clearly and work in teams", {"communication", "teamwork"}),
    ("skills", "I am good at writing code", {"coding"}),
    ("personality", "I am patient, curious and analytical", {"analytical", "patient"}),
    ("personality", "I am independent and organized", {"independent", "organized"}),
    ("career", "I want to become a software engineer", {"software engineer"}),
    ("career", "I want to become a civil engineer", {"engineer"}),
    ("career", "I do not want to become a teacher", set()),
    ("career", "I want to become a farmer and I enjoy farming", {"farmer"}),
]

EXTRACTORS = {
    "interests": extract_interests,
    "subjects": extract_subjects,
    "skills": extract_skills,
    "personality": extract_personality,
    "career": extract_career_goals,
}


def main():
    total = len(CASES)
    exact_matches = 0
    true_positive = false_positive = false_negative = 0
    failures = []

    for field, text, expected in CASES:
        predicted = set(EXTRACTORS[field](text))
        expected = set(expected)
        if predicted == expected:
            exact_matches += 1
        else:
            failures.append((field, text, sorted(expected), sorted(predicted)))
        true_positive += len(expected & predicted)
        false_positive += len(predicted - expected)
        false_negative += len(expected - predicted)

    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 1.0
    recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    print(f"Cases: {total}")
    print(f"Exact category matches: {exact_matches}/{total} ({exact_matches / total:.1%})")
    print(f"Micro precision: {precision:.1%}")
    print(f"Micro recall:    {recall:.1%}")
    print(f"Micro F1:        {f1:.1%}")
    if failures:
        print("\nMismatches:")
        for field, text, expected, predicted in failures:
            print(f"- [{field}] {text!r}: expected={expected}, predicted={predicted}")
    else:
        print("\nAll labelled examples matched exactly.")


if __name__ == "__main__":
    main()
