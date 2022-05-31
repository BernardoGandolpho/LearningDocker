from dotenv import load_dotenv

from fastapi.testclient import TestClient

from app.poke_app import app


# TODO -> Create tests for Pydantic's validation
# TODO -> Create tests for skip and limit parameters
# TODO -> Create tests for not found items


load_dotenv("/usr/src/poke_api/.env")

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Salve"}


def test_list_pokemon():
    response = client.get("/pokemons")
    assert response.status_code == 200


def test_find_pokemon():
    response = client.get("/pokemons/1")
    assert response.status_code == 200


def test_list_moveset():
    response = client.get("/pokemons/1/moveset")
    assert response.status_code == 200


def test_find_move():
    response = client.get("/pokemons/1/moveset/1")
    assert response.status_code == 200


def test_create_existing_pokemon():
    data = {
        "name": "Binho",
        "pokedex_id": 1,
        "types": ["Explosive", "Baiano"]
    }
    response = client.post("/pokemons", json=data)
    assert response.status_code == 400


def test_update_pokemon():
    data = {
        "name": "Binho"
    }
    response = client.put("/pokemons/1", json=data)
    assert response.status_code == 200


def test_delete_pokemon():
    response = client.delete("/pokemons/1")
    assert response.status_code == 204


def test_create_pokemon():
    data = {
        "name": "Bulbasaur",
        "pokedex_id": 1,
        "types": [
            "Grass",
            "Poison"
        ],
        "moveset": [
            {
                "name": "Razor-Wind",
                "power": 80,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Swords-Dance",
                "type": "Normal"
            },
            {
                "name": "Cut",
                "power": 50,
                "accuracy": 0.95,
                "type": "Normal"
            },
            {
                "name": "Bind",
                "power": 15,
                "accuracy": 0.85,
                "type": "Normal"
            },
            {
                "name": "Vine-Whip",
                "power": 45,
                "accuracy": 1.0,
                "type": "Grass"
            },
            {
                "name": "Headbutt",
                "power": 70,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Tackle",
                "power": 40,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Body-Slam",
                "power": 85,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Take-Down",
                "power": 90,
                "accuracy": 0.85,
                "type": "Normal"
            },
            {
                "name": "Double-Edge",
                "power": 120,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Growl",
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Strength",
                "power": 80,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Mega-Drain",
                "power": 40,
                "accuracy": 1.0,
                "type": "Grass"
            },
            {
                "name": "Leech-Seed",
                "accuracy": 0.9,
                "type": "Grass"
            },
            {
                "name": "Growth",
                "type": "Normal"
            },
            {
                "name": "Razor-Leaf",
                "power": 55,
                "accuracy": 0.95,
                "type": "Grass"
            },
            {
                "name": "Solar-Beam",
                "power": 120,
                "accuracy": 1.0,
                "type": "Grass"
            },
            {
                "name": "Poison-Powder",
                "accuracy": 0.75,
                "type": "Poison"
            },
            {
                "name": "Sleep-Powder",
                "accuracy": 0.75,
                "type": "Grass"
            },
            {
                "name": "Petal-Dance",
                "power": 120,
                "accuracy": 1.0,
                "type": "Grass"
            },
            {
                "name": "String-Shot",
                "accuracy": 0.95,
                "type": "Bug"
            },
            {
                "name": "Toxic",
                "accuracy": 0.9,
                "type": "Poison"
            },
            {
                "name": "Rage",
                "power": 20,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Mimic",
                "type": "Normal"
            },
            {
                "name": "Double-Team",
                "type": "Normal"
            },
            {
                "name": "Defense-Curl",
                "type": "Normal"
            },
            {
                "name": "Light-Screen",
                "type": "Psychic"
            },
            {
                "name": "Reflect",
                "type": "Psychic"
            },
            {
                "name": "Bide",
                "type": "Normal"
            },
            {
                "name": "Sludge",
                "power": 65,
                "accuracy": 1.0,
                "type": "Poison"
            },
            {
                "name": "Skull-Bash",
                "power": 130,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Amnesia",
                "type": "Psychic"
            },
            {
                "name": "Flash",
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Rest",
                "type": "Psychic"
            },
            {
                "name": "Substitute",
                "type": "Normal"
            },
            {
                "name": "Snore",
                "power": 50,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Curse",
                "type": "Ghost"
            },
            {
                "name": "Protect",
                "type": "Normal"
            },
            {
                "name": "Sludge-Bomb",
                "power": 90,
                "accuracy": 1.0,
                "type": "Poison"
            },
            {
                "name": "Mud-Slap",
                "power": 20,
                "accuracy": 1.0,
                "type": "Ground"
            },
            {
                "name": "Outrage",
                "power": 120,
                "accuracy": 1.0,
                "type": "Dragon"
            },
            {
                "name": "Giga-Drain",
                "power": 75,
                "accuracy": 1.0,
                "type": "Grass"
            },
            {
                "name": "Endure",
                "type": "Normal"
            },
            {
                "name": "Charm",
                "accuracy": 1.0,
                "type": "Fairy"
            },
            {
                "name": "False-Swipe",
                "power": 40,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Swagger",
                "accuracy": 0.85,
                "type": "Normal"
            },
            {
                "name": "Fury-Cutter",
                "power": 40,
                "accuracy": 0.95,
                "type": "Bug"
            },
            {
                "name": "Attract",
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Sleep-Talk",
                "type": "Normal"
            },
            {
                "name": "Return",
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Frustration",
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Safeguard",
                "type": "Normal"
            },
            {
                "name": "Sweet-Scent",
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Synthesis",
                "type": "Grass"
            },
            {
                "name": "Hidden-Power",
                "power": 60,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Sunny-Day",
                "type": "Fire"
            },
            {
                "name": "Rock-Smash",
                "power": 40,
                "accuracy": 1.0,
                "type": "Fighting"
            },
            {
                "name": "Facade",
                "power": 70,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Nature-Power",
                "type": "Normal"
            },
            {
                "name": "Helping-Hand",
                "type": "Normal"
            },
            {
                "name": "Ingrain",
                "type": "Grass"
            },
            {
                "name": "Knock-Off",
                "power": 65,
                "accuracy": 1.0,
                "type": "Dark"
            },
            {
                "name": "Secret-Power",
                "power": 70,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Weather-Ball",
                "power": 50,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Grass-Whistle",
                "accuracy": 0.55,
                "type": "Grass"
            },
            {
                "name": "Bullet-Seed",
                "power": 25,
                "accuracy": 1.0,
                "type": "Grass"
            },
            {
                "name": "Magical-Leaf",
                "power": 60,
                "type": "Grass"
            },
            {
                "name": "Natural-Gift",
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Worry-Seed",
                "accuracy": 1.0,
                "type": "Grass"
            },
            {
                "name": "Seed-Bomb",
                "power": 80,
                "accuracy": 1.0,
                "type": "Grass"
            },
            {
                "name": "Energy-Ball",
                "power": 90,
                "accuracy": 1.0,
                "type": "Grass"
            },
            {
                "name": "Leaf-Storm",
                "power": 130,
                "accuracy": 0.9,
                "type": "Grass"
            },
            {
                "name": "Power-Whip",
                "power": 120,
                "accuracy": 0.85,
                "type": "Grass"
            },
            {
                "name": "Captivate",
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Grass-Knot",
                "accuracy": 1.0,
                "type": "Grass"
            },
            {
                "name": "Venoshock",
                "power": 65,
                "accuracy": 1.0,
                "type": "Poison"
            },
            {
                "name": "Round",
                "power": 60,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Echoed-Voice",
                "power": 40,
                "accuracy": 1.0,
                "type": "Normal"
            },
            {
                "name": "Grass-Pledge",
                "power": 80,
                "accuracy": 1.0,
                "type": "Grass"
            },
            {
                "name": "Work-Up",
                "type": "Normal"
            },
            {
                "name": "Grassy-Terrain",
                "type": "Grass"
            },
            {
                "name": "Confide",
                "type": "Normal"
            },
            {
                "name": "Grassy-Glide",
                "power": 70,
                "accuracy": 1.0,
                "type": "Grass"
            }
        ]
    }
    response = client.post("/pokemons", json=data)
    assert response.status_code == 201
