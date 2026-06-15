import sys

from wrappers.image_gen.fanar import generate_fanar_image
from activities.social_story.utils import extract_story_text
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

    age = max(3, target_age)
    scaling_age = min(18, age)
    
    if scaling_age <= 5:
        max_len, max_passives, max_neg, pronoun_target = 6, "0 (Strict active voice only)", "1.0% (Max 1 negation)", "Exclusively use explicit names/nouns over pronouns"
    elif scaling_age <= 9:
        max_len, max_passives, max_neg, pronoun_target = 12, "0 (Strict active voice only)", "1.5%", "Keep pronouns low, lean heavily on concrete nouns"
    elif scaling_age <= 14:
        max_len, max_passives, max_neg, pronoun_target = 15, "Maximum 1 across the entire text", "2.0%", "Balanced, ensure clear anaphoric binding"
    else:
        max_len, max_passives, max_neg, pronoun_target = 18, "Maximum 2 across the entire text", "2.5%", "Standard clear prose"

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
           - *Affirming Sentences:* These are positive phrases that enhance the meaning of another sentence or reinforce a key point.
           Examples include: ‘this is okay’; ‘this is very important’.
           - *Partial Sentences:* These are sentences with missing words included to help establish the child’s level of understanding.
        8. **The 10.4 Social Story Formula (Criterion 8):** This is a strict mathematical requirement. Calculate the number of descriptive/informative sentences versus coaching sentences.
           - **Formula:** (Descriptive + Perspective + Affirming) / Coaching >= 4
           - There must be at least 4 sentences that describe (ie. Descriptive, Perspective or Affirming) for every ONE Coaching sentence. If there are 0 Coaching sentences, that is acceptable and passes the formula automatically.
           - **CRITICAL:** Only 1 coaching sentence is allowed in a social story.
           - **CRITICAL:** The title of the story is included in the count of Descriptive sentences.
        9. **Literal Accuracy (Criterion 9):** Words must mean exactly what they say. Absolutely no idioms, metaphors, figures of speech, or sarcasm (e.g., fail if you see "take a seat", "hold your horses", or "in a split second").
        10. **Implementation Design (Criterion 10):** The text must be structured in a way that naturally allows a parent or educator to introduce, review, and patiently fade the story out over time.

    ### STORY STRUCTURE:
    - Produce upto 12 pages.
    - Page 1: Introduction (sets the scene, states the situation factually).
    - Pages 2 to N-1: Body (walks through the sequence of events step by step, in chronological order).
    - Last page: Conclusion (affirms the experience, reinforces calm closure, no new information).

    ### PERSPECTIVE AND TONE:
    - WRITE ENTIRELY IN FIRST-PERSON ("I", "me", "my").
    - NEVER use "you", "your", "must", "should", "always", or "never".
    - NEVER use "I will try to" — use "I can" or "I will".

    ### CRITICAL LINGUISTIC AND READABILITY TARGETS (CALIBRATED FOR AGE {target_age})
    - **Max Sentence Length:** Under no circumstance should any sentence exceed {max_len} words.
    - **Passive Voice Constraint:** Allowed passive voice structures = {max_passives}. Rephrase passives to active voice.
    - **Negation Density:** Keep logical negations under {max_neg}. Frame instructions positively.
    - **Referential Clarity & Pronoun Density:** {pronoun_target}. Prevent tracking ambiguity.

    ### WHAT TO AVOID:
    - DO NOT assume or dictate the child's internal emotional state (e.g., do not write "I will think this is fun").
    - DO NOT use the word "try" to soften commands.
    - DO NOT list rules or demands disguised as sentences.
    - DO NOT reference autism, diagnoses, or clinical labels in the story text.
    - DO NOT use more than 1 Coaching sentence in the story text.

    Examples of social stories:
        1. When I go to the movies:
            When I go to the movies, I wait in line to get my ticket. Sometimes we buy snacks. Sometimes we buy drinks. 
            It can be a good idea to use the bathroom before we sit down. In the theater, we pick a seat and sit down.
            The theater might be dark. The theater might be loud. I can take breaks if I need to. I can ask to take a walk.
            When I am in the theater, I look at the big screen. I keep my voice quiet. 
            I am sitting safely with my family, and this is okay.
        2. Using glue (Validated 1st Person):
            At school, we make crafts. I use glue for my crafts. 
            Using the right amount of glue keeps my project clean.
            Too much glue makes the paper wet. Too little glue means the paper will not stick.
            I can squeeze a small dot of glue onto my paper. My craft looks great when the glue dries.
        3. Math at school (Validated 1st Person - Zero "You" triggers):
            Children learn math at school. Sometimes math worksheets have problems I already know how to do. 
            Reviewing old problems helps my brain stay strong. 
            My teacher gives the same math work to everyone in the class. That is the teacher's job. 
            My job is to finish my worksheet. When I complete my work, my teacher can give me new puzzles to figure out. 
            Solving new math puzzles feels satisfying.
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
    age = int(sys.argv[4]) if len(sys.argv) > 4 else 7
    result = create_social_story_schema(
        situation=situation,
        trigger=trigger,
        reading_level=reading_level,
        target_age=age,
    )
    if isinstance(result, SocialStorySchema):
        print(extract_story_text(result))


if __name__ == "__main__":
    main()
