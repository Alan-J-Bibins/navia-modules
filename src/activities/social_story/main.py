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
    situation: str,
    trigger: str,
    reading_level: str,
    target_age: int,
    functional_word_range: str,
    target_gender: str,
) -> SocialStorySchema | None:
    print("Running social story generation")
    print(f"-> Situation: {situation}")
    print(f"-> Trigger: {trigger}")
    print(f"-> Reading Level: {reading_level}")
    print(f"-> Functional Word Range: {functional_word_range}")
    print(f"-> Target age: {target_age}")
    print(f"-> Target gender: {target_gender}")

    age = max(3, target_age)
    scaling_age = min(18, age)

    if scaling_age <= 5:
        max_len, max_passives, max_neg, pronoun_target = (
            6,
            "0 (Strict active voice only)",
            "1.0% (Max 1 negation)",
            "Exclusively use explicit names/nouns over pronouns",
        )
    elif scaling_age <= 9:
        max_len, max_passives, max_neg, pronoun_target = (
            12,
            "0 (Strict active voice only)",
            "1.5%",
            "Keep pronouns low, lean heavily on concrete nouns",
        )
    elif scaling_age <= 14:
        max_len, max_passives, max_neg, pronoun_target = (
            15,
            "Maximum 1 across the entire text",
            "2.0%",
            "Balanced, ensure clear anaphoric binding",
        )
    else:
        max_len, max_passives, max_neg, pronoun_target = (
            18,
            "Maximum 2 across the entire text",
            "2.5%",
            "Standard clear prose",
        )

    prompt = f"""
    You are an expert clinical psychologist specializing in writing Social Stories for autistic individuals, strictly adhering to Carol Gray's 10.4 criteria.
    Your goal is to share accurate, meaningful social information in a patient, safe, and supportive quality rather than demanding, commanding, or forcing behavioral compliance.
    
    Write a Social Story based on the following input:
    - Situation: {situation}
    - Core Anxiety/Triggers: {trigger}
    - Target Reading Level: {reading_level}
    - Functional Word Range of the child: {functional_word_range}
    - Child's age: {target_age}
    - Child's gender: {target_gender}

    ### THE CAROL GRAY 10.4 FRAMEWORK CRITERIA
        1. **One Philosophy, Definition, and Goal (Criterion 1):** Grounded entirely in *Social Humility*. Acknowledge that your mind is fallible and cast assumptions aside. The goal is ensuring the intended message remains intact, patient, and supportive from Author to Audience. It must never force compliance or support a faulty rationale.
        2. **Discovery (Criterion 2):** Gather information to deeply understand the Audience in relation to the context, identifying the precise focus of the story or discovering if an alternate solution is required.
        3. **Structure (Criterion 3):** The story must have exactly one title (meaningfully representing the topic), three parts (an Introduction that sets the scene, a Body that adds chronological detail, and a Conclusion that reinforces/summarizes), and a MAXIMUM of two sentence types: Descriptive and Coaching.
        4. **Format (Criterion 4):** Tailor and personalize the text layout, length, and delivery to the specific abilities, attention span, learning styles, and whenever possible, the talents and interests of the Audience.
        5. **Tone (Criterion 5):** Keep a safe, patient, positive, and accurate "voice." It must be written exclusively in the First Person ("I", "we") or Third Person ("he", "she", "they"). *CRITICAL FAIL:* Never use Second Person ("you", "your") as it feels demanding. Avoid authoritarian terms like "must", "should", "have to", "always", or "never".
        6. **Questions (Criterion 6):** Clearly answer relevant 'WH' questions describing the context: Where (place), When (time), Who (people), What (cues), How (activities/statements), and Why (the underlying social rationale).
        7. **Celebrate (Criterion 7):** Social Stories make celebration a habit. A minimum of 50% of stories developed for an audience must applaud achievements or celebrate established talents, abilities, and positive qualities. Ensure this narrative heavily affirms what the Audience does well or frames the context with positive reinforcement.
        8. **Formula (Criterion 8):** Maintain the strict 10.4 mathematical sentence ratio:
           (Total Descriptive sentences / Total coaching sentences) >= 4
           Descriptive sentences must appear at least four times as often as Coaching sentences. You are limited to a MAXIMUM of one single sentence that Coaches the Audience per story. The story title counts as a Descriptive sentence.
        9. **Revise (Criterion 9):** Check and correct the text comprehensively until it flawlessly satisfies all ten Social Story criteria.
        10. **Share (Criterion 10):** Structure how the story is introduced and monitored with the same care it was researched. Plan for comprehension, keep introductions highly positive, and track its efficacy over time.

    ### CRITICAL SENTENCE TYPE DEFINITIONS (FOR CRITERION 3 & 8)
    You are strictly limited to using ONLY these two sentence categories:
    - **Descriptive Sentences:** Objectively describe factual aspects of the context (both external factors like settings and internal factors like feelings/perceptions). Free of bias, judgment, or devaluation. (e.g., "Children learn math at school. Reviewing old problems helps my brain stay strong.")
    - **Coaching Sentences:** Gently guide via descriptions of effective Team responses, structured Audience responses, or self-coaching. (e.g., "I can ask to take a walk if I need a break.") *Reminder: Max 1 audience-coaching sentence allowed in the entire text.*

    ### STORY PRODUCING STRUCTURE:
    - Produce upto 12 pages/sections.
    - Page 1: Introduction (sets the scene, states the situation factually).
    - Pages 2 to N-1: Body (walks through the sequence of events step by step, in chronological order).
    - Last page: Conclusion (affirms the experience, reinforces calm closure, no new information).

    ### PERSPECTIVE AND TONE:
    - WRITE ENTIRELY IN FIRST-PERSON ("I", "me", "my") [or third-person if explicitly preferred by the situation setup].
    - NEVER use "you", "your", "must", "should", "always", or "never".
    - NEVER use "I will try to" to soften instructions — use definitive but gentle statements like "I can" or "I will".

    ### CRITICAL LINGUISTIC AND READABILITY TARGETS (CALIBRATED FOR AGE {target_age})
    - **Max Sentence Length:** Under no circumstance should any sentence exceed {max_len} words.
    - **Passive Voice Constraint:** Allowed passive voice structures = {max_passives}. Rephrase passives to active voice.
    - **Negation Density:** Keep logical negations under {max_neg}. Frame instructions positively.
    - **Referential Clarity & Pronoun Density:** {pronoun_target}. Prevent tracking ambiguity.

    ### PERSONALIZATION RULES
    - **Conditional Trigger Relevance:** Evaluate the specific sensory/anxiety `{trigger}` against the given `{situation}`. Only mention the trigger if it is highly probable or directly present in that environment. 
      For example: If the trigger is olfactory (e.g., cooking odors) but the situation is "Reading a book at the school library," DO NOT mention smells. 
      Never manufacture artificial distress or introduce irrelevant triggers where they do not naturally occur.
    - **Main character descriptions:** When describing the visual_prompt for each page, make sure to describe each character in length, if the child's gender is given make use of that. Ensure that any particular object of importance is adequately described (Eg: The 9-year old boy wearing a green t-shirt and blue jeans is holding a paper with the words "Science Test" on it).

    ### WHAT TO AVOID:
    - **NO LITERAL INACCURACY:** Words must mean exactly what they say. Absolutely NO idioms, metaphors, figures of speech, or sarcasm (e.g., do NOT use phrases like "take a seat", "hold your horses", "it's raining cats and dogs", or "in a split second").
    - DO NOT assume or dictate the child's internal emotional state (e.g., do not write "I will think this is fun").
    - DO NOT list rules, commands, or demands disguised as sentences.
    - DO NOT reference autism, diagnoses, or clinical labels in the story text.

    Examples of valid 10.4 social stories:
        1. When I go to the movies:
            When I go to the movies, I wait in line to get my ticket. Sometimes we buy snacks. Sometimes we buy drinks. 
            It can be a good idea to use the bathroom before we sit down. In the theater, we pick a seat and sit down.
            The theater might be dark. The theater might be loud. I can take breaks if I need to. I can ask to take a walk.
            When I am in the theater, I look at the big screen. I keep my voice quiet. 
            I am sitting safely with my family, and this is okay.
        2. Math at school:
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
    situation: str,
    trigger: str,
    reading_level: str,
    target_age: int,
    functional_word_range: str,
    target_gender: str,
):
    story_schema = create_social_story_schema(
        situation=situation,
        trigger=trigger,
        reading_level=reading_level,
        target_age=target_age,
        functional_word_range=functional_word_range,
        target_gender=target_gender
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
    functional_word_range = sys.argv[4] if len(sys.argv) > 4 else "1-20 words"
    age = int(sys.argv[5]) if len(sys.argv) > 5 else 7
    gender = (
        sys.argv[6]
        if len(sys.argv) > 6
        else "male"
    )
    result = create_social_story_schema(
        situation=situation,
        trigger=trigger,
        reading_level=reading_level,
        target_age=age,
        functional_word_range=functional_word_range,
        target_gender=gender,
    )
    if isinstance(result, SocialStorySchema):
        print(extract_story_text(result))


if __name__ == "__main__":
    main()
