import sys
import os
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
    image_prompt: str = Field(
        description="The prompt to generate an image for this page of the social story, the artstyle should be cute and engaging. Provide names for each character so as to keep consecutive image prompts consistent, along with names provide accurate detailed descriptions for each character. The environment should be accurate described with emphasis on time of day, lighting, mood, material of objects, etc"
    )


class SocialStorySchema(BaseModel):
    title: str
    pages: list[StoryPage]


def generate_html_view(story: SocialStorySchema, output_filename: str = "story.html"):
    """Generates a clean, accessible HTML layout combining imagery and prose blocks."""
    print(f"📄 Compiling clinical social narrative into {output_filename}...")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{story.title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
            margin: 0;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            color: #0f172a;
            font-size: 2.5rem;
            margin-bottom: 40px;
            border-bottom: 3px solid #cbd5e1;
            padding-bottom: 15px;
        }}
        .page-card {{
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 40px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }}
        .page-header {{
            background: #f1f5f9;
            padding: 12px 24px;
            font-weight: bold;
            font-size: 1.1rem;
            color: #475569;
            border-bottom: 1px solid #e2e8f0;
        }}
        .image-container {{
            text-align: center;
            background: #fafafa;
            padding: 20px;
            border-bottom: 1px solid #e2e8f0;
        }}
        .story-image {{
            max-width: 100%;
            height: auto;
            max-height: 500px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        .prose-content {{
            padding: 30px;
        }}
        .sentence-line {{
            font-size: 1.3rem;
            line-height: 1.8;
            margin-bottom: 16px;
            display: block;
        }}
        .badge {{
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 4px;
            margin-left: 10px;
            vertical-align: middle;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .badge-descriptive {{ background-color: #e0f2fe; color: #0369a1; }}
        .badge-perspective {{ background-color: #dcfce7; color: #15803d; }}
        .badge-affirming {{ background-color: #fef9c3; color: #a16207; }}
        .badge-coaching {{ background-color: #f3e8ff; color: #6b21a8; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{story.title}</h1>
    """

    for page in story.pages:
        image_file = f"page{page.page_number}.png"
        html_content += f"""
        <div class="page-card">
            <div class="page-header">Page {page.page_number}</div>
            <div class="image-container">
                <img src="{image_file}" alt="Illustration for page {page.page_number}" class="story-image">
            </div>
            <div class="prose-content">
        """
        
        for sentence in page.sentences:
            badge_class = f"badge-{sentence.type.lower()}"
            html_content += f"""
                <span class="sentence-line">
                    {sentence.text}
                    <span class="badge {badge_class}">{sentence.type}</span>
                </span>
            """
            
        html_content += """
            </div>
        </div>
        """

    html_content += """
    </div>
</body>
</html>
    """

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✨ Successfully exported local web view asset to {output_filename}")


def main():
    print("Running social story generation")

    situation = (
        sys.argv[1] if len(sys.argv) > 1 else "Going to the dentist for a cleaning"
    )
    trigger = (
        sys.argv[2]
        if len(sys.argv) > 2
        else "The loud buzzing noise of the cleaning tool"
    )
    reading_level = (
        sys.argv[3]
        if len(sys.argv) > 3
        else "Early elementary, highly literal, 2-3 sentences per page"
    )

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

    IMAGE PROMPT RULES:
    1. Distinct and detailed character descriptions
    2. Image prompts must be within 500 characters
    3. Environments should be accurately described
    4. Try to use the same characters consistently
    5. Describe the scene first, then elaborate the characters.
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

    if response.text:
        story_schema = SocialStorySchema.model_validate_json(response.text)

        print("\n--- Generating Images ---")
        outputs = []
        for i, page in enumerate(story_schema.pages):
            output_name = f"page{page.page_number}.png"
            print(f"Processing Page {page.page_number}")
            
            create_image(
                prompt=page.image_prompt,
                output_name=output_name,
                continuity=True,
                ref_image_path=outputs[-1] if outputs else "",
                initial_image=(i == 0),
            )
            outputs.append(output_name)
            
        print("All images printed successfully")
        
        # --- NEW STEP: Generate HTML Presentation ---
        generate_html_view(story_schema, "story.html")


if __name__ == "__main__":
    main()
