import sys

from wrappers.image_gen.fanar import generate_fanar_image
from wrappers.text_gen.llm import call_llm
from activities.social_story.model import (
    SentenceItem,
    SocialStorySchema,
    StoryVisualSchema,
)


def regenerate_sentence_item(
    story_schema: SocialStorySchema, sentence_id: int, modification_prompt: str | None
) -> SentenceItem | None:
    # Locate the target sentence
    target_sentence = None
    for page in story_schema.pages:
        for sentence in page.sentences:
            if sentence.id == sentence_id:
                target_sentence = sentence
                break
        if target_sentence:
            break
    if target_sentence is None:
        print(f"Sentence ID {sentence_id} not found in story.")
        return None
    prompt = f"""
You are an expert clinical psychologist specializing in Social Stories for autistic individuals, strictly adhering to Carol Gray's 10.4 criteria.
Regenerate a specific sentence from the following social story.
Original Story Title: {story_schema.title}
Target Sentence ID: {sentence_id}
Original Sentence Text: "{target_sentence.text}"
Original Sentence Type: {target_sentence.type}
Full Story Context:
{story_schema.model_dump_json()}
Your task is to regenerate ONLY the target sentence while maintaining:
- The same sentence type ({target_sentence.type})
- First-person perspective ("I", "me", "my")
- Simple, concrete, literal language (no idioms, metaphors, or figures of speech)
- Short sentence structure (max ~15 words)
- Consistency with the rest of the story
- Carol Gray's framework rules
{f'Modification Request: {modification_prompt}' if modification_prompt else 'Keep the same meaning and intent, but rephrase it to be clearer and more effective.'}
Return ONLY the regenerated SentenceItem with the same id ({sentence_id}).
"""
    result = call_llm(prompt=prompt, model="gemini", response_schema=SentenceItem)
    if isinstance(result, SentenceItem):
        return result
    return None


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
    ### THE CAROL GRAY 10.4 FRAMEWORK CRITERIA
        1. **The Social Story Goal (Criterion 1):** The primary objective must be to share accurate, meaningful information in a patient, respectful, and reassuring tone. It must NOT be written to demand, command, or force compliance or behavior change. It is about understanding, not compliance.
        2. **Two-Part Discovery (Criterion 2):** The narrative must reflect a deep understanding of the child's perspective and the specific contextual challenges of the situation. 
        3. **Three Parts (Criterion 3):** The story must have an absolute structural arc:
           - A descriptive, positive, or neutral Title.
           - An Introduction that introduces the topic and setting.
           - A Body that provides details and adds context.
           - A Conclusion that summarizes and provides safe reassurance.
        4. **Tailored Formatting (Criterion 4):** The syntax, text length, and vocabulary density must be optimized for the developmental age and language level of an autistic child.
        5. **The Social Story Chime / Voicing (Criterion 5):** 
           - Must be written exclusively in the **First Person (I, we)** or **Third Person (he, she, they, the children)**.
           - **CRITICAL FAIL TRIGGER:** Any use of the **Second Person (You, your)** is an automatic failure of this criterion. "You" feels accusatory and demanding to an autistic child.
           - The tone must be entirely positive and matter-of-fact. Completely avoid authoritarian or absolute constraint words: "must", "should", "have to", "always", "never", "bad", or "naughty".
        6. **Guided by 6 Questions (Criterion 6):** The narrative must clearly answer: Who, What, When, Where, Why, and How. The "Why" (the social rationale behind an expectation) is the most critical component.
        7. **Sentence Types (Criterion 7):** The story should predominantly use:
           - *Descriptive Sentences:* These sentences describe the facts relating to the situation in a clear and
            objective way. They are free of opinions or assumptions and can share information that “everybody
            knows” (but that may not be obvious to an autistic child). Examples include: ‘Adults and children
            wash to keep clean and smell fresh’, or ‘Everyone needs to see a doctor from time to time’
           - *Perspective Sentences:* These are sentences describe people’s thoughts, feelings or beliefs.
            They can be particularly helpful for autistic children who can have difficulties understanding that
            other people may not have the same thoughts and feelings as them. Examples of perspective
            sentences include: ‘Many people enjoy going to the cinema’, or ‘When I try my best my mum feels
            very proud of me’.
           - *Coaching Sentences (3 types):*
                i. Sentences that describe or suggest responses for the child (e.g. ‘I will try to put my hand up when I want to speak to my teacher in class’)
                ii. Sentences that suggest or describe responses for the caregiver (e.g. ‘Mrs XX can help me to use the soap when I am washing my hands’)
                iii. Sentences that are developed by the child themselves (e.g. ‘I can draw in my special drawing book when I am feeling sad.’)
           - *Affirmative Sentences:* These are positive phrases that enhance the meaning of another sentence or reinforce a key point.
           Examples include: ‘this is okay’; ‘this is very important’.
           - *Partial Sentences:* These are sentences with missing words included to help establish the child’s level of understanding.
        8. **The 10.4 Social Story Formula (Criterion 8):** This is a strict mathematical requirement. Calculate the number of descriptive/informative sentences versus coaching sentences.
           - **Formula:** (Descriptive + Perspective + Affirmative) / Coaching >= 4
           - There must be at least 4 sentences that describe (ie. Descriptive, Perspective or Affirmative) for every ONE Coaching sentence. If there are 0 Coaching sentences, that is acceptable and passes the formula automatically.
           - **CRITICAL:** Only 1 coaching sentence is allowed in a social story.
           - **CRITICAL:** The title of the story is included in the count of Descriptive sentences.
        9. **Literal Accuracy (Criterion 9):** Words must mean exactly what they say. Absolutely no idioms, metaphors, figures of speech, or sarcasm (e.g., fail if you see "take a seat", "hold your horses", or "in a split second").
        10. **Implementation Design (Criterion 10):** The text must be structured in a way that naturally allows a parent or educator to introduce, review, and patiently fade the story out over time.
    STORY STRUCTURE:
    - Produce upto 12 pages.
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
    WHAT TO AVOID:
    - DO NOT write "You will have fun" or "You will enjoy it" — this is predictive and invalidating.
    - DO NOT use the word "try" to soften commands (e.g., "I will try to be quiet").
    - DO NOT list rules or demands disguised as sentences (e.g., "I must not scream").
    - DO NOT frame the child's natural reactions as problems to fix.
    - DO NOT reference autism, diagnoses, or any clinical labels in the story text.

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


def main():
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


if __name__ == "__main__":
    main()
