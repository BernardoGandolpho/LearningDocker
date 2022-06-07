from os import environ

from pymongo import MongoClient
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from ..models import PokemonModel, UpdatePokemonModel

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

        return HTTPException(status_code=404, detail=f"Pokemon {id} not found")