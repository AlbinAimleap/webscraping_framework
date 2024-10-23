from typing import Any, Dict, List, Optional, Union
from pydantic import Field, field_validator
from aio_http.core.schema import BaseSchema


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
    flags: Flags
    safe: bool
    lang: str