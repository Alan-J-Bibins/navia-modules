import spacy
from textstat.textstat import textstat
from pydantic import BaseModel, Field

# Load a lightweight, efficient English pipeline for syntax parsing
nlp = spacy.load("en_core_web_sm")


class ReadabilityAnalysisReport(BaseModel):
    flesch_kincaid_grade: float = Field(
        ..., description="Estimated US school grade level baseline."
    )
    first_readability_index: float = Field(
        ..., description="Autism-specific structural readability index."
    )
    max_sentence_length: int = Field(
        ..., description="Word count of the longest sentence in the story."
    )
    negation_density: float = Field(
        ..., description="Number of logical negations per 100 words."
    )
    passive_voice_count: int = Field(
        ..., description="Count of passive verb structures that strain comprehension."
    )
    pronoun_noun_ratio: float = Field(
        ...,
        description="Ratio of pronouns to nouns; high ratios cause referential ambiguity.",
    )
    passed_all_guardrails: bool = Field(
        ...,
        description="True if text safely satisfies the age-calibrated developmental threshold.",
    )


def readability_analysis(story_text: str, target_age: int) -> ReadabilityAnalysisReport:
    """Runs a lean linguistic audit calibrated dynamically for neurodivergent

    readers across the lifespan (Ages 3 to Adulthood).
    """
    # 1. Anchor the Age Scaling
    # Floor at 3 years old. Cap scaling parameters at 18 to prevent unchecked complexity.
    eval_age = max(3, target_age)
    scaling_age = min(18, eval_age)

    doc = nlp(story_text)

    # 2. Token-Level Structural Parsing
    tokens = [t for t in doc if not t.is_punct and not t.is_space]
    total_words = len(tokens) if tokens else 1

    sentences = list(doc.sents)
    total_sentences = len(sentences) if sentences else 1
    sentence_lengths = [
        len([t for t in sent if not t.is_punct and not t.is_space])
        for sent in sentences
    ]
    max_len = max(sentence_lengths) if sentence_lengths else 0

    # 3. Direct Dependency Feature Extraction (Syntax & Ambiguity)
    neg_count = sum(
        1
        for t in doc
        if t.dep_ == "neg" or t.lower_ in {"never", "without", "except", "unless"}
    )
    neg_density = (neg_count / total_words) * 100

    passive_voice_count = sum(1 for t in doc if t.dep_ == "auxpass")

    noun_count = sum(1 for t in tokens if t.pos_ in {"NOUN", "PROPN"})
    pronoun_count = sum(1 for t in tokens if t.pos_ == "PRON")
    pronoun_ratio = pronoun_count / max(1, noun_count)

    # 4. Readability Indices
    grade = textstat.flesch_kincaid_grade(story_text)

    commas = story_text.count(",")
    paragraphs = len([p for p in story_text.split("\n") if p.strip()])
    syllables = textstat.syllable_count(story_text)

    ci = (10 * commas) / total_words
    pi = (10 * paragraphs) / total_words
    si = syllables / total_words
    sli = total_words / total_sentences
    sttr = len(set([t.lower_ for t in tokens])) / total_words

    first_index = (
        95.43
        - (0.076 * ci)
        + (0.201 * pi)
        - (0.067 * si)
        - (0.073 * sli)
        - (35.202 * sttr)
    )

    # 5. Lifespan Developmental Calibration Matrix
    if scaling_age <= 5:  # Toddler / Early Preschool Tier
        max_allowed_grade = 0.5
        min_required_first = 95.0
        max_allowed_len = 6
        max_passives_allowed = 0
        max_pronoun_ratio = 0.20
        max_neg_density = 1.0
    elif scaling_age <= 9:  # Early Childhood Tier
        max_allowed_grade = float(scaling_age - 5.0)
        min_required_first = 95.0 - (2.5 * (scaling_age - 7))
        max_allowed_len = 12
        max_passives_allowed = 0
        max_pronoun_ratio = 0.35
        max_neg_density = 1.5
    elif scaling_age <= 14:  # Adolescent Tier
        max_allowed_grade = float(scaling_age - 4.0)
        min_required_first = 80.0
        max_allowed_len = 15
        max_passives_allowed = 1
        max_pronoun_ratio = 0.50
        max_neg_density = 2.0
    else:  # Mature Tier (Ages 15 - Adult)
        max_allowed_grade = (
            10.0  # Cap narrative complexity at 10th grade level for universal design
        )
        min_required_first = 70.0
        max_allowed_len = 18
        max_passives_allowed = 2
        max_pronoun_ratio = 0.60
        max_neg_density = 2.5

    # 6. Unified Verification Gate
    passed = all(
        [
            grade <= max_allowed_grade,
            first_index >= min_required_first,
            max_len <= max_allowed_len,
            neg_density <= max_neg_density,
            passive_voice_count <= max_passives_allowed,
            pronoun_ratio <= max_pronoun_ratio,
        ]
    )

    return ReadabilityAnalysisReport(
        flesch_kincaid_grade=round(grade, 2),
        first_readability_index=round(first_index, 2),
        max_sentence_length=max_len,
        negation_density=round(neg_density, 2),
        passive_voice_count=passive_voice_count,
        pronoun_noun_ratio=round(pronoun_ratio, 2),
        passed_all_guardrails=passed,
    )
