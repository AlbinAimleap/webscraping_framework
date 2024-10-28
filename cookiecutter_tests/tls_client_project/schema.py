from typing import Any, Dict, List, Optional, Union
from pydantic import Field, field_validator
from tlsclient.core.schema import BaseSchema

"""Your Schema Goes Here"""
class Schema(BaseSchema):
    ...


if __name__ == "__main__":
    import json
    from pathlib import Path
    with open(Path(__file__) / "schema.json", "w") as f:
        json.dump(Joke.model_json_schema(), f, indent=4)
 