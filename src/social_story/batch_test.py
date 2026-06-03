import sys
from social_story.main import create_social_story_schema
from social_story.utils import save_as_md

if __name__ == "__main__":
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 1;
    test_cases = [
        {
            "situation": "Brushing teeth before bed",
            "trigger": "The strong minty flavor and foamy texture of the toothpaste",
            "reading_level": "Preschool, ultra-simple, 1-2 short sentences per page",
            "target_age": 4,
        },
        {
            "situation": "Getting a haircut at the salon",
            "trigger": "The buzzing sound of the clippers and the physical sensation of hair falling on the neck",
            "reading_level": "Early elementary, highly literal, 2-3 sentences per page",
            "target_age": 6,
        },
        {
            "situation": "An unexpected school fire drill",
            "trigger": "The sudden, extremely loud, flashing and ringing alarm sirens",
            "reading_level": "Early elementary, clear sequence, 2-3 sentences per page",
            "target_age": 7,
        },
        {
            "situation": "Going grocery shopping with mom",
            "trigger": "The buzzing hum of bright fluorescent overhead lights and crowded aisles",
            "reading_level": "Kindergarten, concrete, 1-2 sentences per page",
            "target_age": 5,
        },
        {
            "situation": "It is raining, so outdoor recess is canceled",
            "trigger": "The sudden change in the expected daily schedule and staying indoors",
            "reading_level": "Early elementary, logic-focused, 2-3 sentences per page",
            "target_age": 6,
        },
        {
            "situation": "Washing hands in the school bathroom before lunch",
            "trigger": "The slimy, wet feeling of liquid soap and the loud automated hand dryer",
            "reading_level": "Preschool, action-oriented, 1-2 sentences per page",
            "target_age": 4,
        },
        {
            "situation": "Attending a classmate's birthday party",
            "trigger": "The loud noise of everyone singing 'Happy Birthday' all at once and balloons popping",
            "reading_level": "Mid-elementary, descriptive-heavy, 3 sentences per page",
            "target_age": 8,
        },
        {
            "situation": "Riding the school bus in the morning",
            "trigger": "The deep rumble of the engine and the bumping vibration of the seats",
            "reading_level": "Early elementary, calming tone, 2 sentences per page",
            "target_age": 7,
        },
        {
            "situation": "Trying a new vegetable (broccoli) at dinner",
            "trigger": "The unfamiliar bumpy texture and bitter smell of a new food group",
            "reading_level": "Kindergarten, highly literal, 2 sentences per page",
            "target_age": 5,
        },
        {
            "situation": "Leaving the playground when the timer goes off",
            "trigger": "The transition away from a preferred high-interest activity to go home",
            "reading_level": "Early elementary, visual-heavy, 2-3 sentences per page",
            "target_age": 6,
        },
    ]

    for i, case in enumerate(test_cases[start - 1:], start=start):
        result = create_social_story_schema(
            situation=case["situation"],
            trigger=case["trigger"],
            reading_level=case["reading_level"],
            target_age=case["target_age"],
        )
        if result is None:
            print(f"Skipping story {i}: generation failed.")
            continue
        story_schema, story_report = result

        save_as_md(
            story_schema=story_schema,
            story_report=story_report,
            filename=f"test_story{i}.md",
        )
