from textstat.textstat import textstat
from pydantic import BaseModel, Field


class AlgorithmicAnalysisReport(BaseModel):
    flesch_reading_ease: float = Field(
        ..., description="0-100 score. Higher means easier to read."
    )
    flesch_kincaid_grade: float = Field(
        ..., description="Estimated US school grade level of the text."
    )
    dale_chall_score: float = Field(
        ...,
        description="Readability score based on a lookup framework of 3,000 familiar words.",
    )
    standard_ttr: float = Field(
        ..., description="Raw Type-Token Ratio. Highly vulnerable to text length bias."
    )
    moving_window_ttr: float = Field(
        ...,
        description="Length-agnostic localized lexical variation over a 20-word frame.",
    )
    sentence_length_variance: float = Field(
        ...,
        description="Statistical variance of word count per sentence. Lower means more rhythmic stability.",
    )
    tier2_passed: bool = Field(
        ...,
        description="True if text parameters cross all strict clinical layout thresholds.",
    )


def calculate_moving_window_ttr(text: str, window_size: int = 20) -> float:
    """
    Calculates the length-agnostic vocabulary repetition rate across a sliding window.
    Filters out noise characters to focus entirely on core text predictability.
    """
    tokens = [word.lower() for word in text.split() if word.isalnum()]
    total_tokens = len(tokens)

    if total_tokens == 0:
        return 0.0

    # Fallback to standard TTR if the entire story is shorter than the window frame
    if total_tokens < window_size:
        return len(set(tokens)) / total_tokens

    ttr_scores = []
    for i in range(total_tokens - window_size + 1):
        window = tokens[i : i + window_size]
        ttr_scores.append(len(set(window)) / window_size)

    return sum(ttr_scores) / len(ttr_scores)


def algorithmic_analysis(
    story_text: str, target_age: int
) -> AlgorithmicAnalysisReport:
    """
    Executes a complete local, deterministic NLP audit on the narrative structure,
    vocabulary profile, and cognitive processing friction.
    """
    # 1. Core Readability Engine Calculations
    ease = textstat.flesch_reading_ease(story_text)
    grade = textstat.flesch_kincaid_grade(story_text)
    dale_chall = textstat.dale_chall_readability_score(story_text)

    # 2. Standard vs. Moving Window Lexical Diversity Data
    all_words = [w.lower() for w in story_text.split() if w.isalnum()]
    total_words = len(all_words)
    standard_ttr = (len(set(all_words)) / total_words) if total_words > 0 else 0.0
    mwttr = calculate_moving_window_ttr(story_text, window_size=20)

    # 3. Sentence Length Variance Calculation
    # Normalize punctuation and capture true structural sentences
    sentences = [
        s.strip()
        for s in story_text.replace("!", ".").replace("?", ".").split(".")
        if s.strip()
    ]
    sentence_lengths = [len(s.split()) for s in sentences]

    if len(sentence_lengths) > 1:
        mean_length = sum(sentence_lengths) / len(sentence_lengths)
        variance = sum((x - mean_length) ** 2 for x in sentence_lengths) / len(
            sentence_lengths
        )
    else:
        variance = 0.0

    # 4. Evaluation Matrix Guardrails
    # TODO: Dynamically clamp language exposure down based on chronological age limits
    max_allowed_dale_chall = 4.9 if target_age < 9 else 5.9
    max_allowed_grade = 4.0 if target_age < 9 else 6.0

    has_valid_readability = ease >= 80.0 and grade <= max_allowed_grade
    has_valid_lexicon = dale_chall <= max_allowed_dale_chall
    has_valid_density = 0.40 <= mwttr <= 0.65
    has_stable_rhythm = variance <= 15.0

    tier2_passed = all(
        [has_valid_readability, has_valid_lexicon, has_valid_density, has_stable_rhythm]
    )

    return AlgorithmicAnalysisReport(
        flesch_reading_ease=round(ease, 2),
        flesch_kincaid_grade=round(grade, 2),
        dale_chall_score=round(dale_chall, 2),
        standard_ttr=round(standard_ttr, 2),
        moving_window_ttr=round(mwttr, 2),
        sentence_length_variance=round(variance, 2),
        tier2_passed=tier2_passed,
    )
