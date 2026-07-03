import re
from typing import Literal
from pydantic import BaseModel, Field
from activities.social_story.model import SocialStorySchema
from activities.social_story.utils import extract_story_text
from wrappers.text_gen.llm import call_llm


class SentenceEntry(BaseModel):
    id: int = Field(description="1-Indexed id of the sentence. Do not start from 0")
    text: str = Field(description="Exactly one sentence of prose for the social story.")
    type: Literal["Descriptive", "Coaching", "INVALID"] = Field(
        description="The clinical classification according to the 10.4 framework: ONLY Descriptive or Coaching."
    )


class SentenceListResponse(BaseModel):
    sentences: list[SentenceEntry]


class DeterministicAnalysisReport(BaseModel):
    second_person_pronouns: bool = Field(
        ..., description="Checks for Criterion 5 (No Second Person)"
    )
    absolute_constraints: bool = Field(
        ..., description="Checks for Criterion 5 (No Authoritarian Commands)"
    )
    sentence_ratio_criteria: bool = Field(
        ..., description="Checks for Criterion 8 (Descriptive/Coaching Ratio)"
    )
    sentence_type_criteria: bool = Field(
        ..., description="Checks if any sentences were classified as INVALID"
    )
    story_rating: float
    tier1_passed: bool


def annotate_sentences(story: str) -> SentenceListResponse | None:
    prompt = f"""
    You are an expert clinical linguist specializing in Carol Gray's authentic 10.4 Social Story Framework. 
    Your sole task is to analyze the provided text line-by-line and classify each sentence.

    CRITICAL 10.4 CLASSIFICATION GUIDELINES:
    1. DESCRIPTIVE sentences are objective, observable facts. This category now completely includes descriptions of internal states (thoughts, feelings, motivations of others) and affirmative phrases. If a sentence doesn't direct action, it is DESCRIPTIVE. The story title is always a descriptive sentence.
    2. COACHING sentences gently suggest self-determined strategies, structured responses, or caregiver support options (e.g., "I can ask for help" or "An individual may choose to step away").
    3. INVALID sentences are sentences that break formatting rules or violate core framework conventions.
    
    STORY TO BE ANALYZED:
    {story}
    """
    response = call_llm(
        prompt=prompt, model="gemini", response_schema=SentenceListResponse
    )
    return response if isinstance(response, SentenceListResponse) else None


def deterministic_analysis(
    story: str | SocialStorySchema,
) -> DeterministicAnalysisReport:
    if isinstance(story, SocialStorySchema):
        story_text = extract_story_text(story)
    else:
        story_text = story

    pronoun_patterns = [r"\byou\b", r"\byour\b", r"\byours\b"]
    constraint_patterns = [r"\bmust\b", r"\bshould\b", r"\balways\b", r"\bnever\b"]

    has_pronouns = any(
        bool(re.search(pattern, story_text, re.IGNORECASE))
        for pattern in pronoun_patterns
    )
    has_constraints = any(
        bool(re.search(pattern, story_text, re.IGNORECASE))
        for pattern in constraint_patterns
    )

    obeys_sentence_ratio = False
    obeys_sentence_type = False
    story_rating = -1.0

    annotate_sentences_response = annotate_sentences(story_text)

    if annotate_sentences_response is not None:
        annotated_sentences = annotate_sentences_response.sentences
        descriptive_sentence_count = sum(
            1 for s in annotated_sentences if s.type == "Descriptive"
        )
        coaching_sentence_count = sum(
            1 for s in annotated_sentences if s.type == "Coaching"
        )
        invalid_sentence_count = sum(
            1 for s in annotated_sentences if s.type == "INVALID"
        )

        obeys_sentence_type = invalid_sentence_count == 0

        if coaching_sentence_count == 0:
            obeys_sentence_ratio = True
            story_rating = float("inf")
        else:
            story_rating = descriptive_sentence_count / coaching_sentence_count
            obeys_sentence_ratio = (story_rating >= 4.0) and (
                coaching_sentence_count <= 1
            )

    has_passed_tier1 = all(
        [
            not has_pronouns,
            not has_constraints,
            obeys_sentence_ratio,
            obeys_sentence_type,
        ]
    )

    return DeterministicAnalysisReport(
        second_person_pronouns=has_pronouns,
        absolute_constraints=has_constraints,
        sentence_ratio_criteria=obeys_sentence_ratio,
        sentence_type_criteria=obeys_sentence_type,
        story_rating=story_rating,
        tier1_passed=has_passed_tier1,
    )
