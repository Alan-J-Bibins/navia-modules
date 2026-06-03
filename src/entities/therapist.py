from typing import Callable
from cuid2 import cuid_wrapper
from pydantic import BaseModel, Field

cuid_generator: Callable[[], str] = cuid_wrapper()


class Therapist(BaseModel):
    id: str = Field(
        default_factory=lambda: cuid_generator()
    )
    name: str
