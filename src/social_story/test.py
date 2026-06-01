from social_story.model import SocialStorySchema, SocialStoryScoreResponse
from text_gen.llm import call_llm
from social_story.utils import story_text

def test_social_story(
    story_schema: SocialStorySchema, judge: int = 0
) -> SocialStoryScoreResponse | None:
    story = story_text(story_schema)
    print("Story passed to test module: ", story)
    prompt = f"""
        You are an expert Board Certified Behavior Analyst (BCBA) and an authority on Carol Gray's 10.4 Framework (the 2023 version) for writing Social Stories. Your job is to strictly audit and score the provided social story. 

        Analyze the story text against the entire 10.4 Framework criteria detailed below.

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
           - *Descriptive Sentences:* Objective, observable facts (e.g., "The lunch bell rings at 12:00 PM.").
           - *Perspective Sentences:* Internal states, feelings, or thoughts of others (e.g., "Teachers feel happy when the room is quiet.").
           - *Coaching Sentences:* Gentle, optional suggestions from the child's perspective (e.g., "I can try to take a deep breath.").
           - *Cooperative Sentences:* What others will do to support the child (e.g., "My teacher can help me find my headphones.").
        8. **The 10.4 Social Story Formula (Criterion 8):** This is a strict mathematical requirement. Calculate the number of descriptive/informative sentences versus coaching sentences.
           - **Formula:** (Descriptive + Perspective + Cooperative) / Coaching >= 2
           - There must be at least TWO descriptive/informative sentences for every ONE coaching sentence. If there are 0 coaching sentences, that is acceptable and passes the formula automatically.
        9. **Literal Accuracy (Criterion 9):** Words must mean exactly what they say. Absolutely no idioms, metaphors, figures of speech, or sarcasm (e.g., fail if you see "take a seat", "hold your horses", or "in a split second").
        10. **Implementation Design (Criterion 10):** The text must be structured in a way that naturally allows a parent or educator to introduce, review, and patiently fade the story out over time.

        ---

        ADDITIONAL CRITERIA:
        1. The target age for this story is {story_schema.target_age}, check whether the vocabulary and grammar used in the social story match that which a child of this age can comprehend and understand. Deduct one point if it doesn not. This is not part of Carol Grey's criteria but it is part of the scoring criteria. If violated deduct one point and mention in remarks.

        ### SCORING INSTRUCTIONS
        - Start with a base score of 11. 
        - Deduct 1 full point for each criterion violated. 
        - **Automatic Score Cap:** If the story uses the word "you/your" (Criterion 5) or fails the 10.4 Formula Ratio (Criterion 8), its maximum possible total score cannot exceed 5/10, regardless of how well written the rest of the story is.
        - After scoring, convert this into a percentage.

        ### INPUT DATA TO EVALUATE:
        {story}

    """

    match judge:
        case 0:
            response = call_llm(
                prompt=prompt,
                model="deepseek",
                response_schema=SocialStoryScoreResponse,
            )

            if isinstance(response, SocialStoryScoreResponse):
                print(f"Deepseek Judge: Story attained {response.score}\n Remarks:")
                for remark in response.remarks:
                    print(f"- {remark}")
                return response
        case 1:
            response = call_llm(
                prompt=prompt,
                model="gemini",
                response_schema=SocialStoryScoreResponse,
            )

            if isinstance(response, SocialStoryScoreResponse):
                print(f"Gemini Judge: Story attained {response.score}\n Remarks:")
                for remark in response.remarks:
                    print(f"- {remark}")
                return response

    return None
