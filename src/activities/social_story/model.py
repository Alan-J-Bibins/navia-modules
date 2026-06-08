from typing import Literal
from pydantic import BaseModel, Field


class SentenceItem(BaseModel):
    id: int = Field(description="1-Indexed id of the sentence. Do not start from 0")
    text: str = Field(description="Exactly one sentence of prose for the social story.")
    type: Literal["Descriptive", "Perspective", "Affirming", "Coaching", "Modified By User"] = Field(
        description="The clinical classification of the sentence according to Carol Gray's framework. Ignore 'Modified By User' that is not related to Carol Gray's framework and should not be used to classify the generated sentences."
    )


class StoryPage(BaseModel):
    page_number: int
    sentences: list[SentenceItem]


class SocialStorySchema(BaseModel):
    title: str
    pages: list[StoryPage]
    target_age: int


class SocialStoryScoreResponse(BaseModel):
    score: float = Field(
        description="The score given to the social story in percentage"
    )
    remarks: list[str] = Field(
        description="List individual, specific reasons why points were deducted, citing sentence examples and the exact criterion number violated. If no points were lost, provide a positive summary of framework compliance here. Begin each point with 'POSITIVE' or 'NEGATIVE' depending on the type of remark."
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
