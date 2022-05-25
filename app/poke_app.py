from typing import Optional

from fastapi import FastAPI, HTTPException, Body, Path, Query, Depends
from fastapi.encoders import jsonable_encoder

from .repositories.pokemon_repository import PokemonRepository
from .models import PokemonModel, UpdatePokemonModel


# App and Database
app = FastAPI()


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
def find_move(
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