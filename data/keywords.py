"""
keywords.py

Keyword dictionaries used by CourseGuide AI to extract
information from a student's responses.
"""

# ==========================================================
# INTEREST KEYWORDS
# ==========================================================

INTEREST_KEYWORDS = {

    "technology": [
        "technology",
        "tech",
        "computer",
        "computers",
        "computer science",
        "ict",
        "information technology",
        "software",
        "programming",
        "coding",
        "developer",
        "software development",
        "web development",
        "website",
        "websites",
        "website design",
        "building websites",
        "creating websites",
        "designing websites",
        "app development",
        "artificial intelligence",
        "ai",
        "robotics",
        "cybersecurity",
        "machine learning",
        "data science"
    ],

    "engineering": [
        "engineering",
        "engineer",
        "machines",
        "construction",
        "mechanical",
        "electrical",
        "electronics",
        "civil",
        "chemical",
        "petroleum",
        "mechatronics"
    ],

    "health": [
        "health",
        "healthcare",
        "medicine",
        "medical",
        "doctor",
        "hospital",
        "nursing",
        "pharmacy",
        "patient",
        "patients",
        "saving lives",
        "treating people"
    ],

    "science": [
        "science",
        "scientist",
        "research",
        "researching",
        "experiment",
        "laboratory",
        "biology",
        "chemistry",
        "physics"
    ],

    "business": [
        "business",
        "entrepreneur",
        "entrepreneurship",
        "marketing",
        "finance",
        "accounting",
        "economics",
        "economic",
        "economic issues",
        "studying economies",
        "management",
        "sales"
    ],

    "art": [
        "art",
        "drawing",
        "painting",
        "music",
        "design",
        "creative",
        "graphics",
        "acting"
    ],

    "communication": [
        "communication",
        "writing",
        "journalism",
        "broadcasting",
        "media",
        "public speaking",
        "presenting"
    ],

    "community": [
        "community",
        "helping people",
        "volunteering",
        "charity",
        "public service",
        "social work"
    ],

    "environment": [
        "environment",
        "nature",
        "wildlife",
        "climate",
        "ecosystem",
        "plants",
        "conservation"


    ],
    # Reading and learning
    "reading": [
        "reading books",
        "reading novels",
        "reading stories",
        "reading articles",
        "reading for fun",
        "enjoy reading",
    ],

    "research_and_discovery": [
        "scientific discovery",
        "discovering new things",
        "conducting research",
        "investigating things",
        "finding out how things work",
    ],

    # Digital and recreational interests
    "gaming": [
        "video games",
        "playing video games",
        "mobile games",
        "computer games",
        "game development",
        "gaming",
    ],

    "sports": [
        "playing football",
        "football",
        "basketball",
        "volleyball",
        "athletics",
        "sports",
        "physical fitness",
    ],

    "fashion": [
        "fashion",
        "fashion design",
        "clothing design",
        "styling clothes",
        "fashion trends",
    ],

    "beauty_and_cosmetics": [
        "beauty",
        "cosmetics",
        "makeup",
        "skincare",
        "beauty products",
    ],

    "cooking": [
        "cooking",
        "baking",
        "preparing food",
        "trying recipes",
        "food preparation",
    ],

    "travel_and_tourism": [
        "travel",
        "travelling",
        "traveling",
        "tourism",
        "exploring new places",
        "learning about different cultures",
    ],

    "crafts": [
        "crafts",
        "handicrafts",
        "making handmade items",
        "bead making",
        "knitting",
        "sewing",
    ],

    "gardening": [
        "gardening",
        "growing flowers",
        "growing vegetables",
        "planting flowers",
        "taking care of plants",
    ],

    # Public affairs and society
    "law_and_justice": [
        "law",
        "legal matters",
        "justice",
        "human rights",
        "crime and justice",
    ],

    "politics_and_governance": [
        "politics",
        "governance",
        "public policy",
        "political affairs",
        "government affairs",
    ],

    "history_and_culture": [
        "history",
        "historical events",
        "culture",
        "cultural heritage",
        "traditional culture",
    ],

    # Environment and the natural world
    "wildlife_and_conservation": [
        "wildlife",
        "wildlife conservation",
        "animal conservation",
        "protecting animals",
        "nature conservation",
    ],

    "astronomy_and_space": [
        "astronomy",
        "space exploration",
        "planets",
        "stars",
        "the universe",
        "space science",
    ],

    # Community and personal development
    "volunteering": [
        "volunteering",
        "volunteer work",
        "community volunteering",
        "helping the community",
    ],

    "mentoring": [
        "mentoring",
        "guiding others",
        "coaching people",
        "helping people improve",
    ],

    "personal_development": [
        "personal development",
        "self improvement",
        "self-improvement",
        "learning new skills",
        "personal growth",
    ],

    # These are separate interest areas so that an answer such as
    # "economics, agriculture and social studies" is not reduced to
    # an unrelated category by keyword overlap.
    "agriculture": [
        "agriculture",
        "agricultural science",
        "farming",
        "farmer",
        "farmers",
        "farm work",
        "crop production",
        "growing crops",
        "planting crops",
        "livestock",
        "animal husbandry",
        "raising farm animals",
        "farm management",
        "agribusiness",
        "soil management",
        "horticulture",
        "agricultural economics",
    ],

    "social_sciences": [
        "social studies",
        "social science",
        "social sciences",
        "society",
        "social issues",
        "human behaviour",
        "human behavior",
        "how society works",
        "community issues",
        "cultural issues",
    ],
}

# Economics remains compatible with existing course records tagged as
# "business", while agriculture and social sciences now have their own
# explicit categories.

# ==========================================================
# SUBJECT KEYWORDS
# ==========================================================

SUBJECT_KEYWORDS = {

    "mathematics": [
        "math",
        "maths",
        "mathematics",
        "algebra",
        "calculus"
    ],

    "english": [
        "english",
        "grammar"
    ],

    "physics": [
        "physics"
    ],

    "chemistry": [
        "chemistry"
    ],

    "biology": [
        "biology",
        "life science",
        "life sciences"
    ],

    "computer science": [
        "computer",
        "computer science",
        "ict",
        "information technology",
        "programming"
    ],

    "economics": [
        "economics"
    ],

    "government": [
        "government",
        "civic education"
    ],

    "literature": [
        "literature",
        "literature in english"
    ],

    "geography": [
        "geography"
    ],

    "agricultural science": [
        "agriculture",
        "agricultural science"
    ],

    # Additional science subjects
    "further_mathematics": [
        "further mathematics",
        "further maths",
        "additional mathematics",
        "additional maths",
        "further math",
    ],

    "statistics": [
        "statistics",
        "statistical methods",
        "statistical analysis",
    ],

    "agricultural_economics": [
        "agricultural economics",
        "agric economics",
        "farm economics",
    ],

    "animal_husbandry": [
        "animal husbandry",
        "livestock production",
        "animal production",
    ],

    "crop_science": [
        "crop science",
        "crop production",
        "crop farming",
    ],

    "basic_science": [
        "basic science",
        "integrated science",
    ],

    "basic_technology": [
        "basic technology",
        "introductory technology",
    ],

    # Additional commercial and social science subjects
    "civic_education": [
        "civic education",
        "civic studies",
        "citizenship education",
    ],

    "social_studies": [
        "social studies",
        "social science studies",
    ],

    "accounting": [
        "accounting",
        "financial accounting",
        "principles of accounting",
    ],

    "business_studies": [
        "business studies",
        "business education",
        "introductory business",
    ],

    "insurance": [
        "insurance",
        "insurance studies",
    ],

    # Additional language subjects
    "arabic": [
        "arabic",
        "arabic language",
    ],

    "literature_in_english": [
        "literature in english",
        "english literature",
    ],

    # Additional vocational and practical subjects
    "home_economics": [
        "home economics",
        "home management",
    ],

    "technical_education": [
        "technical education",
        "technical studies",
    ],

    "building_construction": [
        "building construction",
        "construction studies",
    ],

    "woodwork": [
        "woodwork",
        "woodworking",
        "woodwork technology",
    ],

    "metalwork": [
        "metalwork",
        "metal work",
        "metalworking",
    ],

    "computer_applications": [
        "computer applications",
        "application packages",
        "computer applications studies",
    ],

    "information_technology": [
        "information technology",
        "it studies",
        "information and communication technology",
    ],

    "drama": [
        "drama",
        "dramatic arts",
        "theatre arts",
    ],

    "government_and_politics": [
        "political science",
        "politics",
        "political studies",
    ],
}

# ==========================================================
# SKILL KEYWORDS
# ==========================================================

SKILL_KEYWORDS = {

    "problem solving": [
        "problem solving",
        "problem solver",
        "solve problems",
        "solving problems",
        "critical thinking",
        "logical thinking",
        "analysis",
        "analysing",
        "reasoning"
    ],

    "coding": [
        "coding",
        "code",
        "write code",
        "writing code",
        "programming",
        "software development",
        "web development",
        "developer",
        "building apps",
        "build apps",
    ],

    "communication": [
        "communication",
        "communicate",
        "communicating",
        "communicate clearly",
        "speaking",
        "presentation",
        "public speaking",
        "explaining",
        "writing"
    ],

    "leadership": [
        "leadership",
        "leader",
        "leading",
        "management",
        "managing"
    ],

    "creativity": [
        "creative",
        "creativity",
        "innovation",
        "design",
        "drawing"
    ],

    "teamwork": [
        "teamwork",
        "collaboration",
        "working with others",
        "work in teams",
        "working in teams",
        "team player",
        "team players",
        "group work",
        "cooperation"
    ],

    "analytical": [
        "analytical",
        "analysis",
        "analyze data",
        "analyse data",
        "data analysis",
        "research"
    ],

    "organization": [
        "organized",
        "planning",
        "discipline",
        "time management"
    ]
}

# ==========================================================
# PERSONALITY KEYWORDS
# ==========================================================

PERSONALITY_KEYWORDS = {

    "analytical": [
        "analytical",
        "logical",
        "observant",
        "curious",
        "careful",
        "detail oriented"
    ],

    "creative": [
        "creative",
        "imaginative",
        "innovative",
        "artistic",
        "original"
    ],

    "social": [
        "social",
        "friendly",
        "outgoing",
        "talkative",
        "interactive",
        "people person"
    ],

    "independent": [
        "independent",
        "self motivated",
        "self-driven",
        "work alone",
        "individual"
    ],

    "organized": [
        "organized",
        "disciplined",
        "responsible",
        "punctual",
        "well organized"
    ],

    "patient": [
        "patient",
        "calm",
        "understanding",
        "tolerant"
    ],

    "confident": [
        "confident",
        "bold",
        "fearless",
        "courageous"
    ],
    # Analytical and academic skills
    "critical_thinking": [
        "critical thinking",
        "think critically",
        "evaluate information",
        "analyse arguments",
        "analyze arguments",
    ],

    "decision_making": [
        "decision making",
        "decision-making",
        "making decisions",
        "choosing the best option",
    ],

    "mathematical_reasoning": [
        "mathematical reasoning",
        "numerical reasoning",
        "working with numbers",
        "solving mathematical problems",
    ],

    "observation": [
        "observation skills",
        "observing details",
        "careful observation",
        "noticing small details",
    ],

    "documentation": [
        "documentation",
        "writing reports",
        "report writing",
        "recording findings",
    ],

    # Communication and interpersonal skills
    "negotiation": [
        "negotiation",
        "negotiating",
        "negotiation skills",
    ],

    "conflict_resolution": [
        "conflict resolution",
        "resolving conflicts",
        "settling disagreements",
        "mediation",
    ],

    "customer_service": [
        "customer service",
        "customer support",
        "helping customers",
        "handling customer complaints",
    ],

    "persuasion": [
        "persuasion",
        "persuading people",
        "convincing people",
        "influencing others",
    ],

    # Organisation and work habits
    "time_management": [
        "time management",
        "managing my time",
        "meeting deadlines",
        "working within deadlines",
    ],

    "planning": [
        "planning",
        "planning activities",
        "setting goals",
        "organising tasks",
        "organizing tasks",
    ],

    "adaptability": [
        "adaptability",
        "adapting to change",
        "adjusting to new situations",
        "learning new ways of working",
    ],

    "self_management": [
        "self management",
        "self-management",
        "working without supervision",
        "managing myself",
        "self discipline",
        "self-discipline",
    ],

    # Business and practical skills
    "marketing": [
        "marketing",
        "promoting products",
        "promoting services",
        "digital marketing",
        "market research",
    ],

    "sales": [
        "sales",
        "selling products",
        "selling services",
        "sales techniques",
    ],

    "financial_management": [
        "financial management",
        "budgeting",
        "managing money",
        "preparing budgets",
    ],

    "entrepreneurship": [
        "entrepreneurship",
        "starting a business",
        "running a business",
        "business planning",
    ],

    # Creative and practical skills
    "craftsmanship": [
        "craftsmanship",
        "making things by hand",
        "handcrafting",
        "working with materials",
    ],

    "cooking": [
        "cooking",
        "baking",
        "food preparation",
        "preparing meals",
    ],

    "sewing": [
        "sewing",
        "tailoring",
        "making clothes",
        "clothing construction",
    ],

    "video_production": [
        "video production",
        "producing videos",
        "filming",
        "creating video content",
    ],

    "public_relations": [
        "public relations",
        "managing public image",
        "handling public communication",
        "media relations",
    ],

    # Health and care
    "first_aid": [
        "first aid",
        "basic first aid",
        "emergency first aid",
    ],

    "caregiving": [
        "caregiving",
        "caring for children",
        "caring for elderly people",
        "looking after vulnerable people",
    ],
}


# ==========================================================
# CAREER KEYWORDS
# ==========================================================

CAREER_KEYWORDS = {

    "software engineer": [
        "software engineer",
        "software developer",
        "programmer",
        "developer",
        "web developer",
        "app developer",
        "computer programmer"
    ],

    "doctor": [
        "doctor",
        "medical doctor",
        "physician",
        "surgeon"
    ],

    "nurse": [
        "nurse",
        "nursing"
    ],

    "pharmacist": [
        "pharmacist",
        "pharmacy"
    ],

    "engineer": [
        "engineer",
        "civil engineer",
        "mechanical engineer",
        "electrical engineer",
        "chemical engineer",
        "petroleum engineer",
        "mechatronics engineer"
    ],

    "architect": [
        "architect",
        "architecture"
    ],

    "accountant": [
        "accountant",
        "accounting",
        "auditor"
    ],

    "business owner": [
        "business owner",
        "entrepreneur",
        "ceo",
        "startup founder"
    ],

    "teacher": [
        "teacher",
        "lecturer",
        "professor",
        "educator"
    ],

    "scientist": [
        "scientist",
        "research scientist",
        "researcher"
    ],

    "data analyst": [
        "data analyst",
        "analyst",
        "data scientist"
    ],

    "public health officer": [
        "public health",
        "public health officer",
        "health officer"
    ],
    "farmer": [
        "farmer",
        "farmers",
        "farming",
        "farm work",
        "crop farmer",
        "livestock farmer",
        "farm manager",
        "manage a farm",
        "farm management",
        "farm owner",
        "raise livestock",
        "raising livestock",
        "raising farm animals",
        "agriculturist",
        "agriculturalist",
        "agronomist",
        "crop grower",
        "livestock producer",
        "planting crops",
        "crop production",
        "animal husbandry",
        "agribusiness owner",
    ]
}


# ==========================================================
# SPELLING CORRECTIONS
# ==========================================================

SPELLING_CORRECTIONS = {

    # Subjects
    "maths": "mathematics",
    "math": "mathematics",
    "physcs": "physics",
    "phyics": "physics",
    "physic": "physics",
    "chemstry": "chemistry",
    "chemistr": "chemistry",
    "biolog": "biology",
    "biolgy": "biology",
    "englsh": "english",
    "geograpy": "geography",
    "economcs": "economics",
    "goverment": "government",

    # Technology
    "programng": "programming",
    "programmng": "programming",
    "programing": "programming",
    "codng": "coding",
    "technlogy": "technology",
    "technolgy": "technology",
    "computr": "computer",
    "computerscience": "computer science",

    # Engineering
    "enginering": "engineering",
    "engneering": "engineering",
    "mechancal": "mechanical",
    "electrcal": "electrical",
    "electroncs": "electronics",
    "constructon": "construction",

    # Business
    "busines": "business",
    "entreprenuer": "entrepreneur",
    "marketng": "marketing",
    "finace": "finance",
    "accountng": "accounting",

    # Health
    "medcine": "medicine",
    "medcal": "medical",
    "nursng": "nursing",
    "pharmacy": "pharmacy",
    "hosptial": "hospital",

    # General words
    "analysing": "analysis",
    "analyzing": "analysis",
    "organised": "organized",
    "organised": "organized",
    "creativty": "creativity",
    "communcation": "communication",
    "leadrship": "leadership",
    "teamwrk": "teamwork",
}


# ==========================================================
# NATURAL LANGUAGE PHRASES
# ==========================================================

NATURAL_LANGUAGE_PHRASES = {

    "technology": [
        "i like technology",
        "i like tech",
        "i enjoy technology",
        "i enjoy tech",
        "i am interested in technology",
        "i am interested in tech",
        "i love computers",
        "i like computers",
        "i enjoy computers",
        "i like working with computers",
        "i am interested in building websites",
        "i enjoy creating websites",
        "i like website design",
        "i enjoy coding",
        "i like coding",
        "i love coding",
        "i enjoy programming",
        "i like programming",
        "i am into programming",
        "i like building apps",
        "i enjoy building apps",
        "i like software",
        "i am interested in artificial intelligence",
        "i am interested in ai",
        "i like robotics",
        "i am interested in cybersecurity",
    ],

    "engineering": [
        "i like engineering",
        "i enjoy engineering",
        "i am interested in engineering",
        "i like machines",
        "i enjoy working with machines",
        "i like building things",
        "i enjoy building things",
        "i like construction",
        "i am interested in construction",
    ],

    "health": [
        "i like medicine",
        "i enjoy medicine",
        "i am interested in medicine",
        "i like healthcare",
        "i enjoy healthcare",
        "i want to help patients",
        "i like helping sick people",
        "i want to save lives",
        "i am interested in health",
    ],

    "science": [
        "i like science",
        "i enjoy science",
        "i am interested in science",
        "i love experiments",
        "i enjoy experiments",
        "i like doing research",
        "i enjoy research",
        "i am interested in research",
        "i like laboratory work",
        "i enjoy laboratory work",
    ],

    "business": [
        "i like business",
        "i enjoy business",
        "i am interested in business",
        "i want to start a business",
        "i want to own a business",
        "i like selling things",
        "i enjoy marketing",
        "i am interested in finance",
    ],

    "art": [
        "i like art",
        "i enjoy art",
        "i am interested in art",
        "i like drawing",
        "i enjoy drawing",
        "i like painting",
        "i enjoy painting",
        "i like designing",
        "i enjoy designing",
        "i like being creative",
        "i enjoy being creative",
    ],

    "communication": [
        "i like writing",
        "i enjoy writing",
        "i like speaking",
        "i enjoy speaking",
        "i like public speaking",
        "i enjoy public speaking",
        "i like presenting",
        "i enjoy presenting",
        "i like talking to people",
    ],

    "community": [
        "i like helping people",
        "i enjoy helping people",
        "i like helping others",
        "i enjoy helping others",
        "i like volunteering",
        "i enjoy volunteering",
        "i want to help my community",
        "i care about my community",
    ],

    "environment": [
        "i like nature",
        "i enjoy nature",
        "i love nature",
        "i like animals",
        "i enjoy wildlife",
        "i care about the environment",
        "i am interested in the environment",
        "i like plants",
    ],

    "agriculture": [
        "i like agriculture",
        "i enjoy agriculture",
        "i am interested in agriculture",
        "i enjoy farming",
        "i like farming",
        "i want to grow crops",
        "i enjoy growing crops",
        "i like working on a farm",
        "i enjoy working with farm animals",
        "i am interested in livestock",
        "i like agricultural science",
        "i am interested in agribusiness",
    ],

    "social_sciences": [
        "i like social studies",
        "i enjoy social studies",
        "i am interested in social studies",
        "i like learning about society",
        "i enjoy learning about society",
        "i am interested in social issues",
        "i like learning about people and society",
    ],
}