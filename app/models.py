from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


# Class to adapt '_id' to python
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# Models for validation
class Move(BaseModel):
    name: str = Field(..., max_length=30)
    power: Optional[int] = Field(None, ge=0)
    accuracy: Optional[float] = Field(None, ge=0, le=1)
    type: Optional[str] = Field(None)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Quick Attack",
                "power": 40,
                "accuracy": 1,
                "type": "Water"
            }
        }


class PokemonModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., min_length=3, max_length=30)
    pokedex_id: int = Field(..., gt=0, le=809)
    types: List[str] = Field([])
    moveset: Optional[List[Move]] = Field([])

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Squirtle",
                "pokedex_id": 7,
                "types": [
                    "Water"
                ],
                "moveset": [
                    {
                        "name": "Water Gun",
                        "power": 40,
                        "accuracy": 1,
                        "type": "Water"
                    },
                    {
                        "name": "Aqua Tail",
                        "power": 90,
                        "accuracy": 0.9,
                        "type": "Water"
                    }
                ]
            }
        }


class UpdatePokemonModel(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=30)
    types: Optional[List[str]] = Field([])
    moveset: Optional[List[Move]] = Field([])

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Squirtle",
                "types": [
                    "Water"
                ],
                "moveset": [
                    {
                        "name": "Water Gun",
                        "power": 40,
                        "accuracy": 1,
                        "type": "Water"
                    },
                    {
                        "name": "Aqua Tail",
                        "power": 90,
                        "accuracy": 0.9,
                        "type": "Water"
                    }
                ]
            }
        }