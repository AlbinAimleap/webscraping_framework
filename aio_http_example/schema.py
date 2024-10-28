from typing import Any, Dict, List, Optional, Union
from pydantic import Field, model_validator, BaseModel, SkipValidation
from pydb.core import BaseSchema

from icecream import ic


class Flags(BaseSchema):
    nsfw: bool
    religious: bool
    political: bool
    racist: bool
    sexist: bool
    explicit: bool

class Joke(BaseSchema):
    error: bool
    category: str
    joke_type: str = Field(alias="type")
    joke: Optional[str] = None
    setup: Optional[str] = None
    delivery: Optional[str] = None
    flags: int
    safe: bool
    lang: str

class Test(BaseSchema):
    name: str = Field(unique=False)
    prof: Optional[str] = None


# new = T


print(Test.s3_client)