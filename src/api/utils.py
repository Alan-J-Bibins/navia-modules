from entities.learner import (
    LearnerProfile,
    FamilyMember,
    Caregiver,
    GenderEnum,
    VerbalAbilityEnum,
    FunctionalWordRangeEnum,
)


def create_mock_profile() -> LearnerProfile:
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
