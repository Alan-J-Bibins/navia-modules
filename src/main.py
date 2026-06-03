from fastapi import Body, Depends, FastAPI, HTTPException
import json
import uuid

from starlette.responses import StreamingResponse
from image_gen.fanar import generate_fanar_image
from social_story.main import (
    create_social_story,
    create_social_story_schema,
    generate_story_visual_plan,
)
from models.learner import (
    LearnerProfile,
    FamilyMember,
    Caregiver,
    GenderEnum,
    VerbalAbilityEnum,
    FunctionalWordRangeEnum,
)
from social_story.model import SocialStorySchema


def _create_mock_profile() -> LearnerProfile:
    return LearnerProfile(
        # Identity
        therapistId="clx8h1a2b0000xyzwvutsrqpo",
        name="Sample Learner",
        age=7,
        gender=GenderEnum.MALE,
        nationality="AE",
        # Languages
        primaryLanguage=["en", "ar"],
        secondaryLanguage=["other"],
        secondaryLanguageOther="Urdu",
        # People Network
        familyMembers=[
            FamilyMember(
                id="fm_01",
                name="Parent A",
                preferredName="Mama",
                relation="mother",
                hasASD=False,
                preferredLanguage="en",
            ),
            FamilyMember(
                id="fm_02",
                name="Parent B",
                relation="father",
                hasASD=False,
                preferredLanguage="ar",
            ),
            FamilyMember(
                id="fm_03",
                name="Sibling",
                preferredName="Sis",
                relation="sister",
                hasASD=True,
                preferredLanguage="en",
            ),
        ],
        caregivers=[
            Caregiver(
                id="cg_01",
                name="Nanny Name",
                role="nanny",
                preferredLanguage="other",
                preferredLanguageOther="Tagalog",
                hoursPerWeek=40,
            ),
            Caregiver(
                id="cg_02",
                name="Shadow Teacher Name",
                role="shadow-teacher",
                preferredLanguage="en",
                hoursPerWeek=25,
            ),
        ],
        # Communication
        verbalAbility=VerbalAbilityEnum.MINIMAL_VERBAL,
        functionalWordRange=FunctionalWordRangeEnum.TWENTY_ONE_TO_HUNDRED,
        communicationModality=["speech", "aac", "gestures"],
        # Sensory
        sensoryProfile={
            "auditory": "over-sensitive",
            "visual": "typical",
            "tactile": "under-sensitive",
            "vestibular": "typical",
            "proprioceptive": "under-sensitive",
            "olfactory": "not-assessed",
            "gustatory": "over-sensitive",
        },
        sensoryPreferences={
            "auditory": "Calm instrumental music, white noise",
            "tactile": "Deep pressure, weighted blanket",
            "proprioceptive": "Jumping on trampoline, climbing",
        },
        sensoryTriggers={
            "auditory": "Sudden loud noises, hand dryers, vacuum cleaner",
            "gustatory": "Strong flavors, mixed textures in food",
        },
        sensoryNotes="Responds well to noise-cancelling headphones in busy environments.",
        # Interests & Preferences
        interests=["trains", "dinosaurs", "numbers", "Pixar movies"],
        reinforcers=["tablet time", "bubbles", "praise + high-five", "favorite snack"],
        preferredFoods=["plain pasta", "apple slices", "cheddar cheese", "rice"],
        preferredActivities=["puzzle play", "watching trains", "drawing", "trampoline"],
        # Environments
        primaryEnvironment=["mainstream-school"],
        secondaryEnvironment=["clinic", "home"],
    )


_mock_sessions: dict[str, LearnerProfile] = {}
app = FastAPI()


@app.post("/login")
def mock_login():
    """Create a mock session and return a session token."""
    token = str(uuid.uuid4())
    _mock_sessions[token] = _create_mock_profile()
    return {
        "session_token": token,
        "message": "Use this token in X-Session-Token header",
    }


def get_learner_profile(x_session_token: str | None = None) -> LearnerProfile:
    """Dependency to inject the mock profile into any route."""
    if not x_session_token or x_session_token not in _mock_sessions:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing session token. Call /login first.",
        )
    return _mock_sessions[x_session_token]


@app.get("/")
def read_root():
    return {"HOla": "NAVIA"}


@app.get("/health")
def checkhealth():
    return {"msg": "Server is running"}


@app.post("/activity/social_story/stream")
async def generate_social_story_stream(
    profile: LearnerProfile = Depends(get_learner_profile),
    situation: str = Body(..., embed=True),
):
    async def event_stream():
        triggers = json.dumps(profile.sensoryTriggers)
        reading_level = profile.verbalAbility

        yield f"data: {json.dumps({'type': 'status', 'message': 'Generating story...'})}\n\n"

        story_schema = create_social_story_schema(
            situation=situation,
            trigger=triggers,
            target_age=profile.age,
            reading_level=reading_level,
        )

        if story_schema is None:
            yield f"data: {json.dumps({'type': 'error', 'message': 'Failed to generate story schema'})}\n\n"
            return

        yield f"data: {json.dumps({'type': 'story', 'data': story_schema.model_dump_json()})}\n\n"

        yield f"data: {json.dumps({'type': 'status', 'message': 'Planning illustrations...'})}\n\n"

        visual_plan = generate_story_visual_plan(story_schema)

        if visual_plan is None:
            yield f"data: {json.dumps({'type': 'error', 'message': 'Failed to generate visual plan for story'})}\n\n"
            return

        for i, page in enumerate(visual_plan.pages):
            yield f"data: {json.dumps({'type': 'status', 'message': f'Generating image {i+1}/{len(visual_plan.pages)}...'})}\n\n"

            image_path = f"generated_page{i}.png"
            generate_fanar_image(
                prompt=f"{page.visual_description}\n\n{visual_plan.style_preset}",
                output_path=image_path,
            )

            yield f"data: {json.dumps({'type': 'image', 'page': i+1, 'path': image_path})}\n\n"

        yield f"data: {json.dumps({'type': 'complete'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
