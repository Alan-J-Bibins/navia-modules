from typing import Literal
from pydantic import BaseModel, Field


class SentenceItem(BaseModel):
    text: str = Field(description="Exactly one sentence of prose for the social story.")
    type: Literal["Descriptive", "Perspective", "Affirming", "Coaching"] = Field(
        description="The clinical classification of the sentence according to Carol Gray's framework."
    )


class StoryPage(BaseModel):
    page_number: int
    sentences: list[SentenceItem]
    image_prompt: str = Field(
        description="The prompt to generate an image for this page of the social story"
    )


class SocialStorySchema(BaseModel):
    title: str
    pages: list[StoryPage]
