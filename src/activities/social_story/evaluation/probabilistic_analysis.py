from pydantic import BaseModel, Field, field_validator
from activities.social_story.model import SocialStorySchema
from activities.social_story.utils import extract_story_text
from wrappers.text_gen.llm import call_llm

class QualitativeMatrix(BaseModel):
    # Criterion 1
    goal_alignment: int = Field(
        ...,
        description="Score 0-5. Measures if the text shares meaningful info patiently (5) or acts as an authoritarian compliance checklist (0).",
    )
    # Criterion 3
    structural_cohesion: int = Field(
        ...,
        description="Score 0-5. Measures if the story progresses chronologically from a factual setting to a safe, reassuring closure (5).",
    )
    # Criterion 5
    literal_precision: int = Field(
        ...,
        description="Score 0-5. Tracks avoidance of abstract tracking issues, double-meanings, or figures of speech missed by regex (5).",
    )
    # Criterion 6
    social_rationale: int = Field(
        ...,
        description="Score 0-5. Evaluates how clearly the story explains the underlying social 'Why' behind an expectation (5).",
    )

    @field_validator(
        "goal_alignment", "structural_cohesion", "literal_precision", "social_rationale"
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
        ...,
        description="Surgical, highly specific behavioral feedback to fix any detected qualitative deficiencies.",
    )
    tier3_passed: bool = Field(
        ...,
        description="True if ALL individual qualitative metrics score a minimum of 4 out of 5.",
    )


def probabilistic_analysis(
    story: str | SocialStorySchema,
) -> ProbabilisticAnalysisReport | None:
    story_text = (
        extract_story_text(story) if isinstance(story, SocialStorySchema) else story
    )

    prompt = f"""
You are an expert clinical psychologist and linguist specializing in Carol Gray's 10.4 Social Story criteria. 
Your objective is to execute a qualitative macro-audit on the provided social story text.

Focus your entire analysis on the holistic narrative flow, tone, and psychological safety.

EVALUATE THE STORY ALONG THESE 4 CLINICAL DIMENSIONS (Score each 0 to 5):
1. GOAL ALIGNMENT: Does the text focus purely on mapping an environment to build predictability (5)? Or does it function as a disguised commanding rule-list designed to force behavior compliance (0)?
2. STRUCTURAL COHESION: Does the text establish a factual setting at the start, develop chronological progression in the body, and arrive at a calm, validating wrap-up on the final page without presenting new surprises?
3. LITERAL PRECISION: Check for semantic or hidden contextual vulnerabilities like similes, metaphors, etc. Are there any conversational phrases that could be misinterpreted literally by an autistic mind? 
4. SOCIAL RATIONALE: Does the narrative explicitly outline the contextual 'Why' behind social situations, or does it simply tell the reader what happens without offering a rationale?

DETERMINING TIER3_PASSED:
Set `tier3_passed` to true ONLY if every single one of the four qualitative matrix criteria scores a 4 or a 5. If any single metric scores 3 or lower, `tier3_passed` must be false.

STORY TEXT TO REVIEW:
\"\"\"
{story_text}
\"\"\"

Populate and return the complete evaluation metrics strictly matching the requested JSON schema.
"""

    response = call_llm(
        prompt=prompt, model="gemini", response_schema=ProbabilisticAnalysisReport
    )

    if isinstance(response, ProbabilisticAnalysisReport):
        return response
    return None
