import re
from pydantic import BaseModel

from activities.social_story.model import SentenceItem, SocialStorySchema
from activities.social_story.utils import extract_story_text
from wrappers.text_gen.llm import call_llm

from pydantic import BaseModel


class SentenceListResponse(BaseModel):
    sentences: list[SentenceItem]


class DeterministicAnalysisReport(BaseModel):
    second_person_pronouns: bool
    absolute_constraints: bool
    sentence_ratio_criteria: bool
    story_rating: float
    tier1_passed: bool


def annotate_sentences(story: str | SocialStorySchema) -> SentenceListResponse | None:
    if isinstance(story, SocialStorySchema):
        sentence_list: list[SentenceItem] = []
        for page in story.pages:
            for sentence_item in page.sentences:
                sentence_list.append(sentence_item)

        return SentenceListResponse(sentences=sentence_list)
    else:
        prompt = f"""
        You are an expert clinical linguist specializing in Carol Gray's 10.4 Social Story Framework. 
        Your sole task is to analyze the provided social story line-by-line and classify each sentence.

        CRITICAL CLASSIFICATION GUIDELINES FOR ADVANCED TEXTS:
        1. COACHING sentences suggest self-determined strategies. In advanced or third-person text, look for conditional options rather than just "I can" statements (e.g., "An individual may choose to step away" is COACHING).
        2. PERSPECTIVE sentences describe internal states (feelings, thoughts, beliefs, motivations) of other people. Look for advanced emotional indicators (e.g., "Supervisors feel apprehensive" is PERSPECTIVE).
        3. COOPERATIVE sentences detail what others will do to assist. Look for supportive professional roles (e.g., "The HR team ensures accommodations are met" is COOPERATIVE).
        4. DESCRIPTIVE sentences are objective, observable facts. If a sentence contains no internal states or behavioral instructions, default to DESCRIPTIVE. The story title is considered a descriptive sentence.
        
        STORY TO BE ANALYZED: {story}
        """

        response = call_llm(
            prompt=prompt, model="gemini", response_schema=SentenceListResponse
        )

        if isinstance(response, SentenceListResponse):
            return response
        return None


def deterministic_analysis(
    story: str | SocialStorySchema,
) -> DeterministicAnalysisReport:
    if isinstance(story, SocialStorySchema):
        story = extract_story_text(story)

    pronoun_patterns = [r"\byou\b", r"\byour\b", r"\byours\b"]
    constraint_patterns = [r"\bmust\b", r"\bshould\b", r"\balways\b", r"\bnever\b"]

    has_pronouns = any(
        bool(re.search(pattern, story, re.IGNORECASE)) for pattern in pronoun_patterns
    )

    has_constraints = any(
        bool(re.search(pattern, story, re.IGNORECASE))
        for pattern in constraint_patterns
    )

    obeys_sentence_ratio = False
    annotate_sentences_response = annotate_sentences(story)
    print("annotated_sentences: ", annotate_sentences_response.sentences)

    story_rating = -1
    if isinstance(annotate_sentences_response, SentenceListResponse):
        annotated_sentences = annotate_sentences_response.sentences
        descriptive_sentence_count = 0
        coaching_sentence_count = 0
        perspective_sentence_count = 0
        affirming_sentence_count = 0

        for sentence_item in annotated_sentences:
            match sentence_item.type:
                case "Affirming":
                    affirming_sentence_count += 1
                case "Coaching":
                    coaching_sentence_count += 1
                case "Descriptive":
                    descriptive_sentence_count += 1
                case "Perspective":
                    perspective_sentence_count += 1

        # FIX 1 & 3: Handle 0 coaching sentences safely, and cap total coaching count at 1
        if coaching_sentence_count == 0:
            obeys_sentence_ratio = True
            story_rating = float("inf")  # Mathematically infinite ratio
        else:
            # Calculate the actual ratio regardless of coaching count
            story_rating = (
                descriptive_sentence_count
                + affirming_sentence_count
                + perspective_sentence_count
            ) / coaching_sentence_count

            # Passes ONLY if ratio >= 4 AND coaching count is exactly 1
            obeys_sentence_ratio = (story_rating >= 4) and (
                coaching_sentence_count == 1
            )

    has_passed_tier1 = all(
        [not has_pronouns, not has_constraints, obeys_sentence_ratio]
    )

    return DeterministicAnalysisReport(
        second_person_pronouns=has_pronouns,
        absolute_constraints=has_constraints,
        sentence_ratio_criteria=obeys_sentence_ratio,
        story_rating=story_rating,
        tier1_passed=has_passed_tier1,
    )
