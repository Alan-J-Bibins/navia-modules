import sys
from typing import Literal
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from social_story.config import settings
from image_gen.main import create_image

class SentenceItem(BaseModel):
    text: str = Field(description="Exactly one sentence of prose for the social story.")
    type: Literal["Descriptive", "Perspective", "Affirming", "Coaching"] = Field(
        description="The clinical classification of the sentence according to Carol Gray's framework."
    )


class StoryPage(BaseModel):
    page_number: int
    sentences: list[SentenceItem]
    image_prompt: str = Field(description="The prompt to generate an image for this page of the social story, the artstyle should be cute and engaging")


class SocialStorySchema(BaseModel):
    title: str
    pages: list[StoryPage]


def main():
    print("Running social story generation")

    situation = sys.argv[1] if len(sys.argv) > 1 else "Going to the dentist for a cleaning"
    trigger = sys.argv[2] if len(sys.argv) > 2 else "The loud buzzing noise of the cleaning tool"
    reading_level = sys.argv[3] if len(sys.argv) > 3 else "Early elementary, highly literal, 2-3 sentences per page"

    print(f"-> Situation: {situation}")
    print(f"-> Trigger: {trigger}")
    print(f"-> Reading Level: {reading_level}")

    prompt = f"""
    You are an expert clinical psychologist specializing in writing Social Stories for autistic individuals, 
    strictly adhering to Carol Gray's 10.4 criteria. 

    Your goal is to share accurate, meaningful social information rather than demanding or forcing behavioral compliance.

    Write a Social Story based on the following input:
    - Situation: {situation}
    - Core Anxiety/Trigger: {trigger}
    - Target Reading Level: {reading_level}

    CRITICAL CLINICAL CRITERIA:
    1. PERSPECTIVE: Write entirely in the first-person ("I") or third-person plural ("We"/"They"). Never use directing or commanding language targeted at the reader (DO NOT use "You must", "You should", or "Always remember to").
    2. TONE: Maintain a patient, reassuring, factual, and completely literal tone. Avoid idioms, metaphors, or vague emotional descriptions.
    3. SENTENCE RATIO (Carol Gray's Criterion 8): For every 1 "Coaching" sentence (which suggests a calm coping strategy), you MUST provide at least 2 to 5 "Descriptive", "Perspective", or "Affirming" sentences across the story.
    """

    client = genai.Client(api_key=settings.google_gemini_api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SocialStorySchema,
            temperature=0.2,
        ),
    )

    print("\n--- Raw JSON Response from Gemini ---")
    print(response.text)

    if(response.text):
        story_schema = SocialStorySchema.model_validate_json(response.text)

        print("\n--- Generating Images ---")
        for _, page in enumerate(story_schema.pages):
            print(f"Processing Page {page.page_number}")
            create_image(page.image_prompt, f"page{page.page_number}.png")
        print("All images printed successfully")




if __name__ == "__main__":
    main()
