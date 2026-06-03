from datetime import datetime, timezone
from enum import Enum
from typing import Callable, Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from cuid2 import cuid_wrapper

cuid_generator: Callable[[], str] = cuid_wrapper()

class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer-not-to-say"


class VerbalAbilityEnum(str, Enum):
    NON_VERBAL = "non-verbal"
    MINIMAL_VERBAL = "minimal-verbal"
    VERBAL = "verbal"
    FLUENT = "fluent"


class FunctionalWordRangeEnum(str, Enum):
    ZERO = "0"
    ONE_TO_TWENTY = "1-20"
    TWENTY_ONE_TO_HUNDRED = "21-100"
    HUNDRED_PLUS = "100+"


CommunicationModalityType = Literal["speech", "aac", "sign", "gestures", "mixed"]
EnvironmentType = Literal[
    "mainstream-school", "special-needs-school", "clinic", "home", "other"
]


class FamilyMember(BaseModel):
    id: str
    name: str
    relation: str
    hasASD: bool
    preferredLanguage: str
    preferredName: Optional[str] = None


class Caregiver(BaseModel):
    id: str
    name: str
    role: str
    preferredLanguage: str
    hoursPerWeek: int
    preferredLanguageOther: Optional[str] = None


class LearnerProfile(BaseModel):
    # System and Identity Fields
    id: str = Field(
        default_factory=lambda: cuid_generator()
    )  # Or use a dedicated cuid library
    therapistId: str
    learnerId: Optional[str] = None
    name: str
    age: int
    gender: GenderEnum
    nationality: Optional[str] = None
    avatar: Optional[str] = None

    # Language Fields
    primaryLanguage: List[str] = Field(default_factory=list)
    primaryLanguageOther: Optional[str] = None
    secondaryLanguage: List[str] = Field(default_factory=list)
    secondaryLanguageOther: Optional[str] = None

    # People Network
    familyMembers: List[FamilyMember] = Field(default_factory=list)
    caregivers: List[Caregiver] = Field(default_factory=list)

    # Communication Profile
    verbalAbility: VerbalAbilityEnum
    functionalWordRange: Optional[FunctionalWordRangeEnum] = None
    communicationModality: List[CommunicationModalityType] = Field(default_factory=list)

    # Sensory Profile (Typed dynamically via Dict or strictly if required)
    sensoryProfile: Dict[str, str] = Field(default_factory=dict)
    sensoryPreferences: Dict[str, str] = Field(default_factory=dict)
    sensoryTriggers: Dict[str, str] = Field(default_factory=dict)
    sensoryNotes: Optional[str] = None

    # Interests and Preferences
    interests: List[str] = Field(default_factory=list)
    reinforcers: List[str] = Field(default_factory=list)
    preferredFoods: List[str] = Field(default_factory=list)
    preferredActivities: List[str] = Field(default_factory=list)

    # Environments
    primaryEnvironment: List[EnvironmentType] = Field(default_factory=list)
    primaryEnvironmentOther: Optional[str] = None
    secondaryEnvironment: List[EnvironmentType] = Field(default_factory=list)
    secondaryEnvironmentOther: Optional[str] = None

    # Timestamps
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
