from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True
        use_enum_values = True
        validate_assignment = True
        arbitrary_types_allowed = True
        json_encoders = {
            set: list,
            frozenset: list,
            bytes: lambda v: v.decode(),
        }
        