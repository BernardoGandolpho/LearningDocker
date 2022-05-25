from os import environ
from typing import List, Optional

from bson import ObjectId
from fastapi import FastAPI, HTTPException, status, Body, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from pydantic import BaseModel, Field


# App and Database
app = FastAPI()

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
                "description": "Quick Attack inflicts damage. It has a priority of +1, so it is used before all moves that do not have increased priority.",
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


class PokemonRepository():
    def __init__(self):
        self.mongo_url = (f'mongodb://{environ["DB_USER"]}:{environ["DB_PASSWORD"]}@mongodb')
        self.client = MongoClient(self.mongo_url)
        self.db = self.client['pokedex']

    def list_all(self, skip, limit, projection):
        pokemons = self.db['pokemons'].find(skip=skip, limit=limit,
            projection=projection).sort('pokedex_id')

        return list(pokemons)

    def list_one_pokemon(self, id, projection):
        if str(id).isdigit():
            return self.db['pokemons'].find_one({"pokedex_id": int(id)}, projection=projection)
        else:
            return self.db['pokemons'].find_one({"name": id.title()}, projection=projection)

    def add(self, pokemon: PokemonModel):
        if (self.list_one_pokemon(id=pokemon['pokedex_id'], projection={"pokedex_id": True})) is not None:
            return HTTPException(status_code=400, detail="Duplicate pokemon")
        
        try:
            self.db["pokemons"].insert_one(pokemon)
            pokemon.pop("_id", None)

            return JSONResponse(status_code=status.HTTP_201_CREATED, content=pokemon)
        
        except:
            return HTTPException(status_code=500, detail="Internar Server Error")

    def update(self, pokemon: UpdatePokemonModel, id):
        if (self.list_one_pokemon(id=id, projection={"pokedex_id": True})) is None:
            return HTTPException(status_code=404, detail=f"Pokemon {id} not found")

        pokemon = {k: v for k, v in pokemon.dict().items() if v is not None and v != []}     

        try:
            self.db["pokemons"].update_one({"pokedex_id": id}, {"$set": pokemon})
            
            return self.list_one_pokemon(id, {'_id': False})

        except:
            return HTTPException(status_code=500, detail="Internal Server Error")

    def remove(self, id):
        delete_result = self.db["pokemons"].delete_one({"pokedex_id": id})

        if delete_result.deleted_count == 1:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

        raise HTTPException(status_code=404, detail=f"Pokemon {id} not found")


# Routes
@app.get("/")
async def root():
    return {"message": "Salve"}


@app.get("/pokemons")
def list_pokemon(
        skip: Optional[int] = Query(0, ge=0),
        limit: Optional[int] = Query(10, gt=0),
        repository: PokemonRepository = Depends(PokemonRepository)
    ):

    pokemons = repository.list_all(skip, limit, {"_id": False, "moveset": False})

    if pokemons is not None:
        return {"pokemons": pokemons}
    
    raise HTTPException(status_code=404, detail=f"Pokemon not found")


@app.get("/pokemons/{id}")
def find_pokemon(
        id: str = Path(..., max_length=30),
        repository: PokemonRepository = Depends(PokemonRepository)
    ):

    pokemon = repository.list_one_pokemon(id=id, projection={"_id": False, "moveset": False})

    if pokemon is None:
        raise HTTPException(status_code=404, detail=f"Pokemon {id} not found")  
    
    return {"pokemon":pokemon} 


@app.get("/pokemons/{id}/moveset")
def list_moveset(
        id: str = Path(...,max_length=30),
        skip: Optional[int] = Query(0, ge=0),
        limit: Optional[int] = Query(10, gt=0),
        repository: PokemonRepository = Depends(PokemonRepository)
    ):

    pokemon = repository.list_one_pokemon(id=id, projection={"_id": False, "moveset": True})
    
    if pokemon is None:
        raise HTTPException(status_code=404, detail=f"Pokemon {id} not found")

    moveset = pokemon["moveset"][skip : skip + limit]

    if len(moveset) > 0:
        return {"moveset":moveset}
        
    raise HTTPException(status_code=404, detail=f"No moves found from pokemon {id}")


@app.get("/pokemons/{id}/moveset/{move_id}")
async def find_move(
        id: str = Path(..., max_length=30),
        move_id: int = Path(..., ge=0, lt=30),
        repository: PokemonRepository = Depends(PokemonRepository)
    ):

    pokemon = repository.list_one_pokemon(id=id, projection={"_id": False, "moveset": True})

    if pokemon is None:
        raise HTTPException(status_code=404, detail=f"Pokemon {id} not found")

    if len(pokemon["moveset"]) > move_id:
        result = pokemon["moveset"][move_id]
        return {"move": result}
        
    raise HTTPException(status_code=404, detail=f"Move {move_id} from pokemon {id} was not found")


@app.post("/pokemons", response_model=PokemonModel)
def create_pokemon(
        pokemon: PokemonModel = Body(...),
        repository: PokemonRepository = Depends(PokemonRepository)
):
    new_pokemon = jsonable_encoder(pokemon)
    new_pokemon["name"] = new_pokemon["name"].title()
    
    response = repository.add(new_pokemon)

    if type(response) is type(HTTPException(status_code=400)):
        raise response

    return response


@app.put("/pokemons/{id}", response_model=PokemonModel)
def update_pokemon(
        id: int = Path(..., gt=0, le=809),
        pokemon: UpdatePokemonModel = Body(...),
        repository: PokemonRepository = Depends(PokemonRepository)
):
    if pokemon.name is not None:
        pokemon.name = pokemon.name.title()

    response = repository.update(pokemon, id)

    if type(response) is type(HTTPException(status_code=400)):
        raise response

    return response


@app.delete("/pokemons/{id}")
def delete_pokemon(
        id: int = Path(..., gt=0, le=809),
        repository: PokemonRepository = Depends(PokemonRepository)
):

    response = repository.remove(id)

    if type(response) is type(HTTPException(status_code=400)):
        raise response

    return response