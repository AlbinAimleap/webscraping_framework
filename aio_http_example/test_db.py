from typing import Optional, get_origin, get_args, Union
from pydantic import BaseModel, Field

class Test(BaseModel):
    name: str = Field(unique=True)  
    prof: Optional[str] = "coder"  

# Create an instance of the model
new = Test(name="coder")

# Iterate over the fields and check if they are optional
for field_name, field_type in Test.__annotations__.items():
    # Check if the field is Optional by inspecting the type
    field_info = Test.model_fields[field_name]
    
    nullable =  get_origin(field_type) is Union and type(None) in get_args(field_type)
    
    unique = False
    if extra:= field_info.json_schema_extra:
        unique = extra.get("unique")
        
    


for field_name, field_type in Test.__annotations__.items():
    print()
    print(field_name, str(field_type))