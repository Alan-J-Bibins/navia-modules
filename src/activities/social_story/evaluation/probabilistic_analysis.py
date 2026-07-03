from pydantic import BaseModel, Field, field_validator
from activities.social_story.model import SocialStorySchema
from activities.social_story.utils import extract_story_text
from wrappers.text_gen.llm import call_llm


class QualitativeMatrix(BaseModel):
    # Criterion 1
    goal_alignment: int = Field(
        ...,
        description="Score 0-5. Measures if text shares meaningful info patiently via Social Humility (5) or acts as a compliance checklist (0).",
    )
    # Criterion 3
    structural_cohesion: int = Field(
        ...,
        description="Score 0-5. Verifies structural arc: clear descriptive title, environmental setup, chronological steps, reassuring summary (5).",
    )
    # Criterion 7
    celebratory_framing: int = Field(
        ...,
        description="Score 0-5. Assesses if the text honors abilities, praises established skills, and highlights positive attributes instead of focusing strictly on deficits (5).",
    )
    # Criterion 6
    contextual_rationale: int = Field(
        ...,
        description="Score 0-5. Evaluates how explicitly the story answers relevant WH-questions and uncovers the underlying social 'Why' (5).",
    )

    @field_validator(
        "goal_alignment",
        "structural_cohesion",
        "celebratory_framing",
        "contextual_rationale",
    )
    @classmethod
    def validate_scores(cls, v: int) -> int:
        if not (0 <= v <= 5):
            raise ValueError(
                "All qualitative matrix scores must be integers between 0 and 5."
            )
        return v


class ProbabilisticAnalysisReport(BaseModel):
    qualitative_reviews: QualitativeMatrix = Field(
        ..., description="The 0-5 clinical evaluation matrix."
    )
    constructive_feedback: list[str] = Field(
        ..., description="Surgical, specific adjustments to eliminate stylistic flaws."
    )
    tier3_passed: bool = Field(
        ..., description="True if ALL individual metrics score a minimum of 4 out of 5."
    )


def probabilistic_analysis(
    story: str | SocialStorySchema,
) -> ProbabilisticAnalysisReport | None:
    story_text = (
        extract_story_text(story) if isinstance(story, SocialStorySchema) else story
    )

    prompt = f"""
    You are an expert clinical psychologist and linguist specializing in Carol Gray's authentic 10.4 Social Story framework. 
    Your objective is to execute a qualitative macro-audit on the provided social story text string.

    CRITICAL LINGUISTIC SAFETY FILTER:
    As an unwritten prerequisite of 10.4 safety, ensure the text contains absolutely NO idioms, metaphors, or figures of speech (e.g., "take a seat", "in a split second"). If any exist, penalize GOAL ALIGNMENT heavily because the message is no longer safe for an autistic reader.

    EVALUATE THE STORY ALONG THESE 4 CLINICAL DIMENSIONS (Score each 0 to 5):
    1. GOAL ALIGNMENT (Criterion 1): Does the text map out environments patiently using Social Humility to build predictable understanding (5)? Or does it function as a rigid rule-list demanding behavioral compliance (0)?
    2. STRUCTURAL COHESION (Criterion 3): Does the text build a reliable chronological sequence starting from a factual setting and ending with safe, comforting reassurance?
    3. CELEBRATORY FRAMING (Criterion 7): Does the story actively emphasize strengths, talents, and successful baselines? It must feel supportive and encouraging rather than sounding like a breakdown of a child's problem behavior.
    4. CONTEXTUAL RATIONALE (Criterion 6): Does the text adequately cover the essential WH-questions, explicitly revealing the clear, logical "Why" behind social scenarios?

    DETERMINING TIER3_PASSED:
    Set `tier3_passed` to true ONLY if every single one of the four qualitative metrics scores a 4 or a 5. If any single metric scores 3 or lower, `tier3_passed` must be false.

    STORY TEXT TO REVIEW:
    \"\"\"
    {story_text}
    \"\"\"

    Populate and return the evaluation metrics matching the requested response schema exactly.
    """

    response = call_llm(
        prompt=prompt, model="gemini", response_schema=ProbabilisticAnalysisReport
    )
    return response if isinstance(response, ProbabilisticAnalysisReport) else None
