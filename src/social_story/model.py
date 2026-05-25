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
    target_age: int


class SocialStoryScoreResponse(BaseModel):
    score: float = Field(description="The score given to the social story in percentage")
    remarks: list[str] = Field(
        description="List individual, specific reasons why points were deducted, citing sentence examples and the exact criterion number violated. If no points were lost, provide a positive summary of framework compliance here. Begin each point with 'POSITIVE' or 'NEGATIVE' depending on the type of remark."
    )
