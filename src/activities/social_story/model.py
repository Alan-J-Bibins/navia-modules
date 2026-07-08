from typing import Literal
from pydantic import BaseModel, Field


class SentenceItem(BaseModel):
    id: int = Field(description="1-Indexed id of the sentence. Do not start from 0")
    text: str = Field(description="Exactly one sentence of prose for the social story.")
    type: Literal["Descriptive", "Coaching"] | None = Field(
        default=None,
        description="The clinical classification according to Carol Gray's 10.4 framework. "
        "Use 'Descriptive' for objective facts, internal states, or thoughts/feelings of others. "
        "Use 'Coaching' for gentle self-determined strategies or caregiver support. "
        "Optional - may be None if not specified.",
    )


class StoryPage(BaseModel):
    page_number: int
    sentences: list[SentenceItem]
    visual_prompt: str = Field(description="Image prompt for the corresponding page formatted for nano banana. Avoid any style descriptions. Describe only the scene, the characters in it and the environment they are in.")


class SocialStorySchema(BaseModel):
    title: str = Field(
        description="A descriptive, positive, or neutral title representing the story's topic. Counts as a Descriptive sentence."
    )
    pages: list[StoryPage]
    target_age: int


class SocialStoryScoreResponse(BaseModel):
    score: float = Field(
        description="The score given to the social story in percentage (0.0 to 100.0)."
    )
    remarks: list[str] = Field(
        description="List individual, specific reasons why points were deducted, citing sentence examples and the exact 10.4 criterion number violated. "
        "If no points were lost, provide a positive summary of framework compliance here. "
        "Begin each point with 'POSITIVE' or 'NEGATIVE' depending on the type of remark."
    )


class PageVisualPrompt(BaseModel):
    page_number: int
    visual_description: str = Field(
        description="A highly detailed, descriptive scene composition prompt for an image generator. Focus on subjects, actions, setting, and emotions. Avoid abstract metaphors."
    )


class StoryVisualSchema(BaseModel):
    story_title: str
    style_preset: str = Field(
        description="A consistent artistic style descriptor to apply across all pages (e.g., 'Soft watercolor children's book illustration, clear outlines, bright and reassuring tones')."
    )
    pages: list[PageVisualPrompt]
