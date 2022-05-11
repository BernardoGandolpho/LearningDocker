import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Body, Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from bson import ObjectId
import motor.motor_asyncio


# App and Database
app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.pokedex


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
    name: Optional[str] = Field(None, max_length=30)
    power: int = Field(..., ge=0)
    accuracy: Optional[float] = Field(1, gt=0, le=1)
    description: Optional[str] = Field(None, max_length=300)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Quick Attack",
                "power": 40,
                "accuracy": 1,
                "description": "Quick Attack inflicts damage. It has a priority of +1, so it is used before all moves that do not have increased priority.",
            }
        }


class PokemonModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., min_length=3, max_length=30)
    pokedex_id: int = Field(..., gt=0, le=905)
    types: List[str] = []
    moveset: Optional[List[Move]] = None

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
                        "accuracy": 1
                    },
                    {
                        "name": "Aqua Tail",
                        "power": 90,
                        "accuracy": 0.9
                    }
                ]
            }
        }


class UpdatePokemonModel(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=30)
    types: Optional[List[str]] = None
    moveset: Optional[List[Move]] = None

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
                        "accuracy": 1
                    },
                    {
                        "name": "Aqua Tail",
                        "power": 90,
                        "accuracy": 0.9
                    }
                ]
            }
        }


# Routes
@app.get("/")
async def root():
    return {"message": "Salve"}


@app.get("/pokemons")
async def list_pokemon(
        skip: Optional[int] = Query(0, ge=0),
        limit: Optional[int] = Query(10, gt=0)
    ):
    pokemons = await db["pokemons"].find(skip=skip, limit=limit, projection={"_id": False, "moveset": False}).sort('pokedex_id').to_list(limit)
    
    if pokemons is not None:
        return {"pokemons":pokemons}
    
    raise HTTPException(status_code=404, detail=f"Pokemon not found")


@app.get("/pokemons/{id}")
async def find_pokemon(id: int = Path(..., gt=0, le=905)):
    pokemon = await db["pokemons"].find_one({"pokedex_id": id}, projection={"_id": False})

    if pokemon is not None:
        return {"pokemon":pokemon}

    raise HTTPException(status_code=404, detail=f"Pokemon {id} not found")


@app.get("/pokemons/{id}/moveset")
async def list_moveset(
        id: int = Path(..., gt=0, le=905),
        skip: Optional[int] = Query(0, ge=0),
        limit: Optional[int] = Query(10, gt=0)
    ):

    pokemon = await db["pokemons"].find_one({"pokedex_id": id})

    if pokemon is not None:
        name = pokemon["name"]
        moveset = pokemon["moveset"][skip : skip + limit]
        if len(moveset) > 0:
            return {"moveset":moveset}
        raise HTTPException(status_code=404, detail=f"No moves found from {name}")

    raise HTTPException(status_code=404, detail=f"Pokemon {id} not found")


@app.get("/pokemons/{id}/moveset/{move_id}")
async def find_move(
        id: int = Path(..., gt=0, le=905),
        move_id: int = Path(..., ge=0, lt=30)):

    pokemon = await db["pokemons"].find_one({"pokedex_id": id})

    if pokemon is not None:
        name = pokemon["name"]

        if len(pokemon["moveset"]) > move_id:
            result = pokemon["moveset"][move_id]
            return result
            
        raise HTTPException(status_code=404, detail=f"Move {move_id} from {name} was not found")

    raise HTTPException(status_code=404, detail=f"Pokemon {id} not found")


@app.post("/pokemons", response_model=PokemonModel)
async def create_pokemon(pokemon: PokemonModel = Body(...)):
    new_pokemon = jsonable_encoder(pokemon)

    if (await db["pokemons"].find_one({"pokedex_id": pokemon.pokedex_id})) is not None:
        raise HTTPException(status_code=400, detail="Duplicate pokemon")

    try:
        await db["pokemons"].insert_one(new_pokemon)
        new_pokemon.pop("_id", None)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_pokemon)
    except:
        raise HTTPException(status_code=500, detail="Internar Server Error")


@app.put("/pokemons/{id}", response_model=PokemonModel)
async def update_pokemon(id: int = Path(..., gt=0, le=905), pokemon: UpdatePokemonModel = Body(...)):
    pokemon = {k: v for k, v in pokemon.dict().items() if v is not None}

    if len(pokemon) >= 1:
        update_result = await db["pokemons"].update_one({"pokedex_id": id}, {"$set": pokemon})

        if update_result.modified_count == 1:
            if (
                updated_pokemon := await db["pokemons"].find_one({"pokedex_id": id})
            ) is not None:
                return updated_pokemon

    if (existing_pokemon := await db["pokemons"].find_one({"pokedex_id": id})) is not None:
        return existing_pokemon

    raise HTTPException(status_code=404, detail=f"Pokemon {id} not found")


@app.delete("/pokemons/{id}")
async def delete_pokemon(id: int = Path(..., gt=0, le=905)):

    delete_result = await db["pokemons"].delete_one({"pokedex_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Pokemon {id} not found")
