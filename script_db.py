import requests
import json

# This script populates the database with data from another api


def post_all (max_pokedex_id, source_url, my_url):
    for i in range (1, max_pokedex_id+1):
        url_pokemon = source_url + str(i)

        response = requests.get(url_pokemon)

        if response.status_code == 200:
            response = response.json()

            types = []
            for type in (response["types"]):
                types.append(type["type"]["name"].title())

            pokemon = {"name": response["name"].title(), "pokedex_id": i, "types": types, "moveset": []}
            
            response = requests.post(my_url, json=pokemon)

            if response.status_code == 201:
                print(f"Pokemon {i} postado com sucesso!")
            else:
                print(f"Puxou os dados de {i}, mas a minha api n aceitou: {response.status_code}")
            
        else:
            print(f"Não achou os dados do pokemon {i}: {response.status_code}")


def put_moves(max_pokedex_id, source_url, my_url):
    for i in range (1, max_pokedex_id+1):
        url_pokemon = source_url + str(i)
        my_url_pokemon = my_url + str(i)

        response = requests.get(url_pokemon)

        if response.status_code == 200:
            response = response.json()

            moves = []
            for move in (response["moves"]):
                moves.append({"name":move["move"]["name"].title()})

            update_moves = json.dumps({"moveset": moves})

            response = requests.put(my_url_pokemon, data=update_moves)

            if response.status_code == 200:
                print(f"Os ataques do pokemon {i} foram atualizados com sucesso!")
            else:
                print(f"Puxou os dados de {i}, mas a minha api nao aceitou: {response.status_code}")
            
        else:
            print(f"Não achou os dados do pokemon {i}: {response.status_code}")


source_url = "https://pokeapi.co/api/v2/pokemon/"
my_url = "http://0.0.0.0:8008/pokemons/"

max_pokedex_id = 809

post_all(max_pokedex_id, source_url, my_url)
put_moves(max_pokedex_id, source_url, my_url)
