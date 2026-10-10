"""
courses.py

Course dataset used by Course Compass.

The data below contains the undergraduate courses used
by the recommendation engine.
"""

from models.course import Course


COURSES = [

    # =====================================================
    # FACULTY OF AGRICULTURE & AGRICULTURAL TECHNOLOGY
    # =====================================================

    Course(
        name="Agricultural Economics",
        faculty="Agriculture & Agricultural Technology",
        department="Agricultural Economics",
        description= "Learn how economics and business ideas are used in farming and agriculture.",
        interests=["business", "science", "agriculture"],
        subjects=["mathematics"],
        skills=["analytical"],
        personality_traits=["analytical", "organized", "detail-oriented"],
        careers=["agricultural economist"],
        jamb_subjects=['English Language', 'Mathematics', 'Economics', 'Biology/Agricultural Science'],
        jamb_cutoff=160,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Agricultural Extension and Rural Development",
        faculty="Agriculture & Agricultural Technology",
        department="Agricultural Extension",
        description="Learn how to help farmers improve their farming methods and support rural communities.",
        interests=["community", "science", "agriculture"],
        subjects=["biology"],
        skills=["communication"],
        personality_traits=["social", "patient", "helpful"],
        careers=["extension officer"],
        jamb_subjects=['English Language', 'Biology/Agricultural Science', 'Chemistry', 'Economics'],
        jamb_cutoff=160,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Animal Production",
        faculty="Agriculture & Agricultural Technology",
        department="Animal Production",
        description= "Learn about raising, breeding, feeding and managing farm animals.",
        interests=["science", "agriculture"],
        subjects=["biology"],
        skills=["analytical"],
        personality_traits=["patient", "observant", "analytical"],
        careers=["animal scientist"],
        jamb_subjects=['English Language', 'Biology/Agricultural Science', 'Chemistry', 'Physics'],
        jamb_cutoff=160,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Crop Production",
        faculty="Agriculture & Agricultural Technology",
        department="Crop Production",
        description="Learn how crops are grown, managed and produced for food and other uses.",
        interests=["science", "agriculture"],
        subjects=["biology"],
        skills=["analytical"],
        personality_traits=["patient", "observant", "practical"],
        careers=["agronomist"],
        jamb_subjects=['English Language', 'Biology/Agricultural Science', 'Chemistry', 'Physics'],
        jamb_cutoff=160,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Soil Science",
        faculty="Agriculture & Agricultural Technology",
        department="Soil Science",
        description="Learn about soil, its fertility and how to manage land for better crop production.",
        interests=["science", "environment", "agriculture"],
        subjects=["chemistry"],
        skills=["analytical"],
        personality_traits=["analytical", "observant", "patient"],
        careers=["soil scientist"],
        jamb_subjects=['English Language', 'Chemistry', 'Physics', 'Biology/Agricultural Science'],
        jamb_cutoff=160,
        duration="5 Years",
        degree="B.Tech."
    ),

    # =====================================================
    # FACULTY OF ALLIED HEALTH SCIENCES
    # =====================================================

    Course(
        name="Nursing Science",
        faculty="Allied Health Sciences",
        department="Nursing Science",
        description="Learn how to care for patients, prevent illness and support people during treatment.",
        interests=["health"],
        subjects=["biology"],
        skills=["communication"],
        personality_traits=["patient", "caring", "social"],
        careers=["nurse"],
        jamb_subjects=['English Language', 'Biology', 'Chemistry', 'Physics'],
        jamb_cutoff=280,
        duration="5 Years",
        degree="B.NSc."
    ),

    Course(
        name="Public Health",
        faculty="Allied Health Sciences",
        department="Public Health",
        description="Learn how to prevent diseases and improve the health of communities.",
        interests=["health", "community"],
        subjects=["biology"],
        skills=["analytical"],
        personality_traits=["social", "helpful", "analytical"],
        careers=["public health officer"],
        jamb_subjects=['English Language', 'Biology', 'Chemistry', 'Physics'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    # =====================================================
    # FACULTY OF BASIC MEDICAL SCIENCES
    # =====================================================

    Course(
        name="Medical Biochemistry",
        faculty="Basic Medical Sciences",
        department="Biochemistry",
        description="Learn about the chemical processes that happen inside the human body.",
        interests=["health", "science"],
        subjects=["chemistry"],
        skills=["analytical"],
        personality_traits=["analytical", "detail-oriented", "curious"],
        careers=["scientist"],
        jamb_subjects=['English Language', 'Biology', 'Chemistry', 'Physics'],
        jamb_cutoff=200,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Human Anatomy",
        faculty="Basic Medical Sciences",
        department="Human Anatomy",
        description="Learn about the structure and parts of the human body.",
        interests=["health"],
        subjects=["biology"],
        skills=["analytical"],
        personality_traits=["observant", "detail-oriented", "patient"],
        careers=["anatomist"],
        jamb_subjects=['English Language', 'Biology', 'Chemistry', 'Physics'],
        jamb_cutoff=200,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Human Physiology",
        faculty="Basic Medical Sciences",
        department="Human Physiology",
        description= "Learn how the different parts of the human body work.",
        interests=["health"],
        subjects=["biology"],
        skills=["analytical"],
        personality_traits=["curious", "analytical", "detail-oriented"],
        careers=["physiologist"],
        jamb_subjects=['English Language', 'Biology', 'Chemistry', 'Physics'],
        jamb_cutoff=200,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Chemical Pathology",
        faculty="Basic Clinical Sciences",
        department="Chemical Pathology",
        description= "Learn how laboratory tests can help detect and understand diseases.",
        interests=["health", "science"],
        subjects=["biology", "chemistry"],
        skills=["analytical", "detail-oriented"],
        personality_traits=["analytical", "detail-oriented", "patient"],
        careers=["chemical pathologist"],
        jamb_subjects=['English', 'Biology', 'Chemistry', 'Physics'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Haematology",
        faculty="Basic Clinical Sciences",
        department="Haematology",
        description="Learn about blood, blood cells and diseases that affect the blood.",
        interests=["health", "science"],
        subjects=["biology", "chemistry"],
        skills=["analytical", "detail-oriented"],
        personality_traits=["analytical", "observant", "patient"],
        careers=["haematologist"],
        jamb_subjects=['English', 'Biology', 'Chemistry', 'Physics'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Histopathology",
        faculty="Basic Clinical Sciences",
        department="Histopathology",
        description="Learn how diseased tissues and cells are examined to help diagnose diseases.",
        interests=["health", "science"],
        subjects=["biology", "chemistry"],
        skills=["analytical", "detail-oriented"],
        personality_traits=["analytical", "observant", "patient"],
        careers=["histopathologist"],
        jamb_subjects=['English', 'Biology', 'Chemistry', 'Physics'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Medical Microbiology",
        faculty="Basic Clinical Sciences",
        department="Medical Microbiology",
        description="Learn about microorganisms that cause diseases and infections in humans.",
        interests=["health", "science"],
        subjects=["biology", "chemistry"],
        skills=["analytical"],
        personality_traits=["curious", "observant", "analytical"],
        careers=["medical microbiologist"],
        jamb_subjects=['English', 'Biology', 'Chemistry', 'Physics'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Pharmacology",
        faculty="Basic Clinical Sciences",
        department="Pharmacology",
        description="Learn how medicines work, their effects and how they interact with the body.",
        interests=["health", "science"],
        subjects=["biology", "chemistry"],
        skills=["analytical"],
        personality_traits=["analytical", "detail-oriented", "patient"],
        careers=["pharmacologist"],
        jamb_subjects=['English', 'Biology', 'Chemistry', 'Physics'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),
    # =====================================================
    # FACULTY OF CLINICAL SCIENCES
    # =====================================================

    Course(
        name="Medicine and Surgery",
        faculty="Clinical Sciences",
        department="Medicine and Surgery",
        description="Study the prevention, diagnosis and treatment of human illness, including supervised clinical training.",
        interests=["health"],
        subjects=["biology", "chemistry"],
        skills=["communication", "problem solving"],
        personality_traits=["patient", "caring", "analytical"],
        careers=["doctor"],
        jamb_subjects=["English Language", "Biology", "Chemistry", "Physics"],
        jamb_cutoff=None,
        duration="7 Years",
        degree="MBBS"
    ),

    # =====================================================
    # FACULTY OF COMPUTING
    # =====================================================

    Course(
        name="Computer Science",
        faculty="Computing",
        department="Computer Science",
        description="Learn about programming, software, artificial intelligence and computer systems.",
        interests=["technology"],
        subjects=["computer science", "mathematics"],
        skills=["coding", "problem solving"],
        careers=["software engineer"],
        jamb_subjects=['English Language', 'Mathematics', 'Physics', 'Chemistry'],
        jamb_cutoff=220,
        duration="5 Years",
        degree="B.Tech."
    ),

    # =====================================================
    # FACULTY OF ENGINEERING & ENGINEERING TECHNOLOGY
    # =====================================================

    Course(
        name="Chemical Engineering",
        faculty="Engineering & Engineering Technology",
        department="Chemical Engineering",
        description="Learn how chemical processes are designed and used to produce useful products.",
        interests=["engineering"],
        subjects=["chemistry", "mathematics"],
        skills=["problem solving"],
        personality_traits=["analytical", "patient", "detail-oriented"],
        careers=["engineer"],
        jamb_subjects=['English Language', 'Mathematics', 'Physics', 'Chemistry'],
        jamb_cutoff=240,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Civil Engineering",
        faculty="Engineering & Engineering Technology",
        department="Civil Engineering",
        description="Learn how buildings, roads, bridges and other infrastructure are designed and constructed.",
        interests=["engineering"],
        subjects=["mathematics", "physics"],
        skills=["problem solving"],
        personality_traits=["analytical", "patient", "detail-oriented"],
        careers=["engineer"],
        jamb_subjects=['English Language', 'Mathematics', 'Physics', 'Chemistry'],
        jamb_cutoff=220,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Electrical/Electronics Engineering",
        faculty="Engineering & Engineering Technology",
        department="Electrical/Electronics Engineering",
        description="Learn about electricity, electronics, power systems and electronic devices.",
        interests=["engineering", "technology"],
        subjects=["physics", "mathematics"],
        skills=["problem solving"],
        personality_traits=["analytical", "patient", "detail-oriented"],
        careers=["engineer"],
        jamb_subjects=['English Language', 'Mathematics', 'Physics', 'Chemistry'],
        jamb_cutoff=230,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Mechanical/Production Engineering",
        faculty="Engineering & Engineering Technology",
        department="Mechanical/Production Engineering",
        description="Learn how machines and production systems are designed, built and maintained.",
        interests=["engineering"],
        subjects=["physics", "mathematics"],
        skills=["problem solving"],
        personality_traits=["analytical", "patient", "detail-oriented"],
        careers=["engineer"],
        jamb_subjects=['English Language', 'Mathematics', 'Physics', 'Chemistry'],
        jamb_cutoff=230,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Mechatronics and Systems Engineering",
        faculty="Engineering & Engineering Technology",
        department="Mechatronics and Systems Engineering",
        description="Learn how mechanical, electronic and intelligent systems work together.",
        interests=["engineering", "technology"],
        subjects=["physics", "computer science"],
        skills=["coding", "problem solving"],
        careers=["engineer"],
        jamb_subjects=['English Language', 'Mathematics', 'Physics', 'Chemistry'],
        jamb_cutoff=240,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Petroleum Engineering",
        faculty="Engineering & Engineering Technology",
        department="Petroleum Engineering",
        description= "Learn about the exploration, drilling and production of petroleum resources.",
        interests=["engineering"],
        subjects=["chemistry", "physics"],
        skills=["analytical"],
        personality_traits=["analytical", "practical", "observant"],
        careers=["engineer"],
        jamb_subjects=['English Language', 'Mathematics', 'Physics', 'Chemistry'],
        jamb_cutoff=260,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Computer & Communication Engineering",
        faculty="Engineering & Engineering Technology",
        department="Computer & Communication Engineering",
        description="Engineering of computer hardware, communication systems and related technologies.",
        interests=["engineering", "technology", "computing"],
        subjects=["mathematics", "physics", "computer science"],
        skills=["coding", "problem solving", "analytical"],
        personality_traits=["analytical", "curious", "practical"],
        careers=["computer engineer", "communication engineer", "network engineer"],
        jamb_subjects=[],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Agriculture & Bio-Resource Engineering",
        faculty="Engineering & Engineering Technology",
        department="Agriculture & Bio-Resource Engineering",
        description="Learn how engineering is applied to agriculture and biological resources.",
        interests=["engineering", "agriculture", "science"],
        subjects=["mathematics", "physics", "biology"],
        skills=["problem solving", "analytical"],
        personality_traits=["practical", "analytical", "creative"],
        careers=["agricultural engineer", "bio-resource engineer"],
        jamb_subjects=[],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    # =====================================================
    # FACULTY OF ENVIRONMENTAL TECHNOLOGY
    # =====================================================

    Course(
        name="Architecture",
        faculty="Environmental Technology",
        department="Architecture",
        description="Learn how to design buildings and plan spaces for people to use.",
        interests=["art", "engineering"],
        subjects=["mathematics"],
        skills=["creativity"],
        personality_traits=["creative", "detail-oriented", "visual"],
        careers=["architect"],
        jamb_subjects=['English Language', 'Mathematics', 'Physics', 'Chemistry'],
        jamb_cutoff=220,
        duration="5 Years",
        degree="B.Tech."
    ),

    # Urban & Regional Planning is intentionally excluded from this project's
    # recommendation catalogue per the project scope; this is not a claim that
    # ATBU has no department by that name.

    Course(
        name="Quantity Surveying",
        faculty="Environmental Technology",
        department="Quantity Surveying",
        description="Construction cost estimation and project management.",
        interests=["engineering", "business"],
        subjects=["mathematics"],
        skills=["analytical"],
        personality_traits=["analytical", "organized", "detail-oriented"],
        careers=["quantity surveyor"],
        jamb_subjects=['English Language', 'Mathematics', 'Physics', 'Economics'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Building",
        faculty="Environmental Technology",
        department="Building",
        description="Learn about building construction, materials and methods used in construction.",
        interests=["construction", "engineering"],
        subjects=["mathematics", "physics"],
        skills=["problem solving", "analytical"],
        personality_traits=["practical", "organized", "detail-oriented"],
        careers=["building technologist", "construction manager"],
        jamb_subjects=['English', 'Mathematics', 'Physics', 'Chemistry'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Environmental Management Technology",
        faculty="Environmental Technology",
        department="Environmental Management Technology",
        description="Learn how to protect, manage and use environmental resources responsibly.",
        interests=["environment", "science"],
        subjects=["biology", "geography"],
        skills=["analytical"],
        personality_traits=["observant", "analytical", "responsible"],
        careers=["environmental management officer"],
        jamb_subjects=['English', 'Biology', 'Chemistry', 'Geography'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Estate Management and Valuation",
        faculty="Environmental Technology",
        department="Estate Management and Valuation",
        description="Learn how properties are managed, valued and developed.",
        interests=["business", "property"],
        subjects=["mathematics", "economics"],
        skills=["analytical", "communication"],
        personality_traits=["organized", "social", "detail-oriented"],
        careers=["estate manager", "property manager"],
        jamb_subjects=['English', 'Mathematics', 'Economics', 'Geography'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Industrial Design",
        faculty="Environmental Technology",
        department="Industrial Design",
        description="Learn how to design useful and attractive products.",
        interests=["art", "design", "technology"],
        subjects=["art", "technical drawing"],
        skills=["creativity", "problem solving"],
        personality_traits=["creative", "curious", "detail-oriented"],
        careers=["industrial designer", "product designer"],
        jamb_subjects=['English', 'Mathematics', 'Physics', 'Fine Art'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Survey & Geo-Informatics",
        faculty="Environmental Technology",
        department="Survey & Geo-Informatics",
        description="Learn about land surveying, mapping and geographic information systems.",
        interests=["technology", "environment"],
        subjects=["mathematics", "geography", "physics"],
        skills=["analytical", "problem solving"],
        personality_traits=["analytical", "observant", "precise"],
        careers=["surveyor", "GIS specialist"],
        jamb_subjects=['English', 'Mathematics', 'Physics', 'Geography'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    # =====================================================
    # FACULTY OF MANAGEMENT SCIENCES
    # =====================================================

    Course(
        name="Accounting and Finance",
        faculty="Management Sciences",
        department="Accounting and Finance",
        description="Learn how money, financial records and business finances are managed.",
        interests=["business"],
        subjects=["mathematics", "economics"],
        skills=["analytical"],
        personality_traits=["organized", "detail-oriented", "analytical"],
        careers=["accountant"],
        jamb_subjects=['English Language', 'Mathematics', 'Economics', 'Government'],
        jamb_cutoff=220,
        duration="5 Years",
        degree="B.Sc."
    ),

    Course(
        name="Management Information Technology",
        faculty="Management Sciences",
        department="Management Information Technology",
        description="Learn how technology and information systems are used to support businesses.",
        interests=["business", "technology"],
        subjects=["computer science", "mathematics"],
        skills=["analytical"],
        personality_traits=["analytical", "organized", "adaptable"],
        careers=["data analyst"],
        jamb_subjects=['English Language', 'Mathematics', 'Economics', 'Physics'],
        jamb_cutoff=200,
        duration="5 Years",
        degree="B.Sc."
    ),

    # =====================================================
    # FACULTY OF SCIENCE
    # =====================================================

    Course(
        name="Biochemistry",
        faculty="Science",
        department="Biochemistry",
        description="Learn about the chemical processes that happen in living organisms.",
        interests=["science"],
        subjects=["chemistry", "biology"],
        skills=["analytical"],
        personality_traits=["curious", "analytical", "observant"],
        careers=["scientist"],
        jamb_subjects=['English Language', 'Biology', 'Chemistry', 'Physics'],
        jamb_cutoff=200,
        duration="5 Years",
        degree="B.Sc."
    ),

    Course(
        name="Biological Sciences",
        faculty="Science",
        department="Biological Sciences",
        description="Learn about living organisms, their structures and how they function.",
        interests=["science"],
        subjects=["biology"],
        skills=["analytical"],
        personality_traits=["curious", "analytical", "observant"],
        careers=["scientist"],
        jamb_subjects=['English Language', 'Biology', 'Chemistry', 'Physics'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Ecology",
        faculty="Science",
        department="Ecology",
        description= "Learn how living organisms interact with each other and their environment.",
        interests=["science", "environment"],
        subjects=["biology"],
        skills=["analytical"],
        personality_traits=["curious", "analytical", "observant"],
        careers=["scientist"],
        jamb_subjects=['English Language', 'Biology', 'Chemistry', 'Physics'],
        jamb_cutoff=160,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Applied Geology",
        faculty="Science",
        department="Applied Geology",
        description="Learn about the Earth, rocks, minerals and natural resources.",
        interests=["science", "environment"],
        subjects=["geography"],
        skills=["analytical"],
        personality_traits=["curious", "analytical", "observant"],
        careers=["scientist"],
        jamb_subjects=['English Language', 'Mathematics', 'Physics', 'Chemistry'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Mathematical Sciences",
        faculty="Science",
        department="Mathematical Sciences",
        description="Learn advanced mathematics, statistics and mathematical modelling.",
        interests=["science"],
        subjects=["mathematics"],
        skills=["problem solving"],
        personality_traits=["analytical", "patient", "detail-oriented"],
        careers=["scientist"],
        jamb_subjects=['English Language', 'Mathematics', 'Physics', 'Economics'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Statistics",
        faculty="Science",
        department="Statistics",
        description="Learn how to collect, analyse and understand data.",
        interests=["science", "technology"],
        subjects=["mathematics"],
        skills=["analytical"],
        personality_traits=["analytical", "organized", "adaptable"],
        careers=["data analyst"],
        jamb_subjects=['English Language', 'Mathematics', 'Physics', 'Economics'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Microbiology",
        faculty="Science",
        department="Microbiology",
        description="Learn about microorganisms such as bacteria, fungi and other microbes.",
        interests=["science"],
        subjects=["biology"],
        skills=["analytical"],
        personality_traits=["curious", "analytical", "observant"],
        careers=["scientist"],
        jamb_subjects=['English Language', 'Biology', 'Chemistry', 'Physics'],
        jamb_cutoff=200,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Physics",
        faculty="Science",
        department="Physics",
        description= "Learn about matter, energy, forces and the laws that explain how nature works.",
        interests=["science"],
        subjects=["physics", "mathematics"],
        skills=["analytical"],
        personality_traits=["curious", "analytical", "observant"],
        careers=["scientist"],
        jamb_subjects=['English Language', 'Physics', 'Mathematics', 'Chemistry'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Chemistry",
        faculty="Science",
        department="Chemistry",
        description="Learn about matter, its properties, composition and chemical reactions.",
        interests=["science"],
        subjects=["chemistry"],
        skills=["analytical"],
        personality_traits=["analytical", "curious", "detail-oriented"],
        careers=["chemist", "laboratory scientist"],
        jamb_subjects=['English', 'Chemistry', 'Mathematics', 'Physics'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),


# =====================================================
# FACULTY OF TECHNOLOGY EDUCATION
# =====================================================

    Course(
        name="Library and Information Science",
        faculty="Technology Education",
        department="Library and Information Science",
        description="Learn how information and library resources are organized, managed and provided to people.",
        interests=["education", "information", "technology", "social_sciences"],
        subjects=["english", "computer science"],
        skills=["communication", "organization"],
        personality_traits=["organized", "helpful", "detail-oriented"],
        careers=["librarian", "information specialist"],
        jamb_subjects=['English','Literature','Government','Economics'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Science Education",
        faculty="Technology Education",
        department="Science Education",
        description= "Learn how to teach science subjects and help students understand scientific ideas.",
        interests=["education", "science"],
        subjects=["biology", "chemistry", "physics", "mathematics"],
        skills=["communication", "teaching"],
        personality_traits=["patient", "social", "helpful"],
        careers=["science teacher", "education officer"],
        jamb_subjects=['English', 'Biology', 'Chemistry', 'Physics'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Vocational Education",
        faculty="Technology Education",
        department="Vocational Education",
        description="Education and training focused on practical and vocational skills.",
        interests=["education", "practical"],
        subjects=["technical drawing"],
        skills=["communication", "practical"],
        personality_traits=["patient", "practical", "helpful"],
        careers=["vocational teacher", "training officer"],
        jamb_subjects=['English', 'Mathematics', 'Economics', 'Government'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Educational Foundations",
        faculty="Technology Education",
        department="Educational Foundations",
        description="Learn about the basic theories, principles and practices of education.",
        interests=["education", "community", "social_sciences"],
        subjects=["english"],
        skills=["communication", "analysis"],
        personality_traits=["patient", "social", "organized"],
        careers=["education officer", "educational administrator"],
        jamb_subjects=['English', 'Government', 'Economics', 'CRS/IRS'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Construction Technology Education",
        faculty="Technology Education",
        department="Construction Technology Education",
        description="Learn how construction technology and building skills can be taught and applied.",
        interests=["education", "construction", "engineering"],
        subjects=["mathematics", "physics", "technical drawing"],
        skills=["practical", "problem solving"],
        personality_traits=["practical", "patient", "organized"],
        careers=["construction technology teacher", "technical instructor"],
        jamb_subjects=['English', 'Mathematics', 'Physics', 'Chemistry'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Educational Psychology and Counselling",
        faculty="Technology Education",
        department="Educational Psychology and Counselling",
        description="Learn about learning, student development and how to support students through counselling.",
        interests=["education", "community", "health", "social_sciences"],
        subjects=["biology", "english"],
        skills=["communication", "problem solving"],
        personality_traits=["patient", "empathetic", "social"],
        careers=["school counsellor", "educational psychologist"],
        jamb_subjects=['English', 'Biology', 'Government', 'Economics'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Electrical Electronics Technology Education",
        faculty="Technology Education",
        department="Electrical Electronics Technology Education",
        description="Learn how electrical and electronic technology can be taught and applied.",
        interests=["education", "technology", "engineering"],
        subjects=["physics", "mathematics"],
        skills=["problem solving", "practical"],
        personality_traits=["practical", "analytical", "patient"],
        careers=["electrical technology teacher", "technical instructor"],
        jamb_subjects=['English', 'Mathematics', 'Physics', 'Chemistry'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

    Course(
        name="Mechanical Technology Education",
        faculty="Technology Education",
        department="Mechanical Technology Education",
        description="Learn how mechanical and technical skills can be taught and applied.",
        interests=["education", "engineering", "technology"],
        subjects=["physics", "mathematics"],
        skills=["problem solving", "practical"],
        personality_traits=["practical", "patient", "analytical"],
        careers=["mechanical technology teacher", "technical instructor"],
        jamb_subjects=['English', 'Mathematics', 'Physics', 'Chemistry'],
        jamb_cutoff=180,
        duration="5 Years",
        degree="B.Tech."
    ),

Course(
    name="Veterinary Medicine",
    faculty="Veterinary Medicine",
    department="Veterinary Medicine",
    description="Learn how to prevent, diagnose and treat diseases in animals and keep them healthy.",
    interests=["health", "science", "animals"],
    subjects=["biology", "chemistry"],
    skills=["problem solving", "communication"],
    personality_traits=["patient", "caring", "observant"],
    careers=["veterinary doctor"],
    jamb_subjects=['English Language', 'Biology', 'Chemistry', 'Physics'],
    jamb_cutoff=200,
    duration="6 Years",
    degree="DVM"
),

]


def get_all_courses():
    """
    Return the complete list of available courses.
    """
    return COURSES
