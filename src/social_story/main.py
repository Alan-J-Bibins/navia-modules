import sys

from image_gen.fanar import generate_fanar_image
from text_gen.llm import call_llm
from social_story.model import (
    SocialStorySchema,
    StoryVisualSchema,
)


def create_social_story_schema(
    situation: str, trigger: str, reading_level: str, target_age: int
) -> SocialStorySchema | None:
    print("Running social story generation")
    print(f"-> Situation: {situation}")
    print(f"-> Trigger: {trigger}")
    print(f"-> Reading Level: {reading_level}")
    print(f"-> Target age: {target_age}")

    prompt = f"""
    You are an expert clinical psychologist specializing in writing Social Stories for autistic individuals, strictly adhering to Carol Gray's 10.4 criteria.
    Your goal is to share accurate, meaningful social information rather than demanding or forcing behavioral compliance.
    Write a Social Story based on the following input:
    - Situation: {situation}
    - Core Anxiety/Trigger: {trigger}
    - Target Reading Level: {reading_level}
    - Child's age: {target_age}
    SENTENCE TYPE DEFINITIONS (Carol Gray's framework):
    - "Descriptive": States objective facts about the situation, setting, people, or steps. Answers who, what, where, when, why. Example: "A restaurant has tables and chairs."
    - "Perspective": Describes the internal states, thoughts, feelings, or sensory experiences of self or others. Example: "Sometimes the restaurant feels noisy to me." or "Waiters work hard to bring food quickly."
    - "Affirming": Reinforces a shared value, strength, or reassuring truth. Example: "Grown-ups help me when I feel unsure."
    - "Coaching": Suggests a gentle, optional strategy the reader CAN try (never MUST). Example: "When it feels too loud, I can put on my headphones."
    STORY STRUCTURE:
    - Produce exactly 8-12 pages.
    - Page 1: Introduction (sets the scene, states the situation factually).
    - Pages 2 to N-1: Body (walks through the sequence of events step by step, in chronological order).
    - Last page: Conclusion (affirms the experience, reinforces calm closure, no new information).
    - Each page MUST have 1-3 sentences. Never more than 3 sentences per page.
    - Sentences on a page must form a coherent, logically connected set.
    PERSPECTIVE AND TONE:
    - WRITE ENTIRELY IN FIRST-PERSON ("I", "me", "my"). This is the child's own story told from their voice.
    - NEVER use "you", "you must", "you should", "you will", "always", or "never".
    - NEVER use "I will try to" — this implies anticipated failure. Use "I can" or "I will".
    - Use simple, concrete, completely literal language. Avoid ALL idioms, metaphors, sarcasm, and figures of speech.
    - Use short sentences (max ~15 words each).
    SENTENCE RATIO (MANDATORY):
    - Every Coaching sentence on a page MUST be preceded by at least 1-2 Descriptive, Perspective, or Affirming sentences on the SAME page.
    - No page may consist only of Coaching sentences.
    - Aim for approximately: 50% Descriptive, 20% Perspective, 20% Affirming, 10% Coaching across the entire story.
    WHAT TO AVOID:
    - DO NOT write "You will have fun" or "You will enjoy it" — this is predictive and invalidating.
    - DO NOT use the word "try" to soften commands (e.g., "I will try to be quiet").
    - DO NOT list rules or demands disguised as sentences (e.g., "I must not scream").
    - DO NOT frame the child's natural reactions as problems to fix.
    - DO NOT reference autism, diagnoses, or any clinical labels in the story text.
    IMAGE PROMPT RULES (each prompt max 500 characters):
    - FIRST sentence: describe a specific protagonist (age, gender, hair color, clothing) that will appear consistently. Use the EXACT same character description in every image prompt. Example: "A 7-year-old boy with short brown hair, wearing a blue striped t-shirt and jeans."
    - THEN describe the setting and action matching this particular page.
    - Specify: "well-lit, calm, uncluttered environment. No crowds, no harsh shadows."
    - Artstyle: "simple and clean flat vector illustration, cute and playful cartoon art style, soft pastel color palette, gentle diffused lighting, matte textures, low contrast, minimal shading, clean rounded outlines, comforting and friendly aesthetic, high readability, isolated on a solid light cream background."
    - NEVER depict the child in distress, crying, or fearful.
    - Avoid abstract or surreal elements. Scenes must be literal and grounded in reality.

    Examples of social stories:
        1. When I go to the movies:
            When I go to the movies, I wait in line to get my ticket. Sometimes we buy snacks. Sometimes we buy drinks. It can be a good idea to use the bathroom before we sit down.
            In the theater, we pick a seat and sit down. The theater might be dark. The theater might be loud. I can take breaks if I need to. I can ask to take a walk.
            When I am in the theater, I am sitting in my seat with a quiet voice. Going to the movies is fun!
        2. Using glue:
            At school we do crafts and make things that use glue. I like to make things at school. I like to use glue.When we make things at school it is important to use the right amount of glue.
            If I use too little glue things won’t stick. If I use too much glue everything gets covered in glue. It could make my paper too wet, it won’t be sticky and the glue will drip or it may rip the paper. 
            It could even ruin my work.I will try to use just the right amount to make the glue stick and it will look great.
        3. Math at school:
            All kids learn math at school. Math is really fun. But, sometimes kids have to practice math problems they already know how to do. It may not be fun to have to do math problems and worksheets that you already know how to do.
            The teachers have all the kids to do the math work. That is their job. They have to give all of the kids the math work even when they know that the kids know how to do the work. All teachers, everywhere have to do it.
            It is the kids’ job to do the work the teachers give them. All kids everywhere have to do it. Sometimes you have to do things that are not so much fun to do. Sometimes you have to do math work that you already know how to do.
            But if you do the work then the teacher will give special math problems just for you to figure out. It is fun to figure out new math problems. First you finish the math work and then the teacher gives you special things to do! That sounds like lots of FUN!!!!!!
    """

    story_schema = call_llm(
        prompt=prompt, model="gemini", response_schema=SocialStorySchema
    )

    if not isinstance(story_schema, SocialStorySchema):
        print("Failed to generate a valid story schema.")
        return None
    return story_schema

    # if story_schema:
    #
    #     print("Commencing test with deepseek judge")
    #     if isinstance(story_schema, SocialStorySchema):
    #         social_story_score_response = test_social_story(story_schema)
    #
    #         if isinstance(social_story_score_response, SocialStoryScoreResponse):
    #             return (story_schema,social_story_score_response)
    #

    # print("\n--- Generating Images ---")
    # outputs = []
    # for i, page in enumerate(story_schema.pages):
    #     output_name = f"page{page.page_number}.png"
    #     print(f"Processing Page {page.page_number}")
    #
    #     sdxl_create_image(
    #         prompt=page.image_prompt,
    #         output_name=output_name,
    #         continuity=True,
    #         ref_image_path=outputs[-1] if outputs else "",
    #         initial_image=(i == 0),
    #     )
    #     outputs.append(output_name)
    # print("All images printed successfully")
    # generate_html_view(story_schema, "story.html")


def generate_story_visual_plan(
    story_schema: SocialStorySchema,
) -> StoryVisualSchema | None:

    prompt = (
        f"You are an expert children's book illustrator and art director.\n"
        f"Analyze the following social story titled '{story_schema.title}'. "
        f"Break the story down page-by-page. For each page, design a concrete, visually rich scene "
        f"description that an AI image generator can use to create an illustration.\n\n"
        f"Guidelines for descriptions:\n"
        f"- Be literal and explicit. Describe the character's actions, expressions, the setting, and key objects.\n"
        f"- Maintain visual consistency: reference the same character traits throughout.\n"
        f"- Keep the mood safe, reassuring, and positive.\n"
        f"- Avoid using abstract text concepts (e.g., do not say 'the image represents love', instead say 'a mother hugging her child warmly in a sunlit living room').\n\n"
        f"Full Story Data:\n{story_schema.model_dump_json()}"
    )

    result = call_llm(
        prompt=prompt, model="deepseek", response_schema=StoryVisualSchema
    )

    if isinstance(result, StoryVisualSchema):
        return result
    return None


def create_social_story(
    situation: str, trigger: str, reading_level: str, target_age: int
):
    story_schema = create_social_story_schema(
        situation=situation,
        trigger=trigger,
        reading_level=reading_level,
        target_age=target_age,
    )

    if not isinstance(story_schema, SocialStorySchema):
        return

    visual_plan = generate_story_visual_plan(story_schema)

    if not isinstance(visual_plan, StoryVisualSchema):
        return

    print(visual_plan.model_dump_json(indent=2))

    for i, page in enumerate(visual_plan.pages):
        generate_fanar_image(
            prompt=f"{page.visual_description}\n\n{visual_plan.style_preset}",
            output_path=f"generated_page{i}.png",
        )


if __name__ == "__main__":
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
    age = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    create_social_story(
        situation=situation,
        trigger=trigger,
        reading_level=reading_level,
        target_age=age,
    )
