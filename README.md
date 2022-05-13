# Learning Docker

Este projeto consiste em uma API com dados de pokemons, e foi criada para colocar em prática uso de FastAPI, MongoDB e Docker/Docker-Compose dentre outros conceitos menores.

Para inicializar a API e o banco de dados, exeute com 'docker-compose' os comandos:
```
$ docker-compose build
$ docker-compose up
```

Para popular o banco de dados, em outro terminal, utilize o comando:
```
$ python script_db.py
```

Depois de inicializada, a interface pode ser acessada pelo navegador com a URL:
- http://0.0.0.0:8008

Para ver uma lista com os pokemons presentes no banco de dados, é possível acessar pela URL:
- http://0.0.0.0:8008/pokemons

Para fazer buscas por pokemons específicos, é possível utilizar seu nome ou id da pokedex na URL, por exemplo:
- http://0.0.0.0:8008/pokemons/025
- http://0.0.0.0:8008/pokemons/pikachu

Com a busca realizada, é possível buscar uma lista com os ataques de um pokemon utilizando o caminho "moveset", como por exemplo:
- http://0.0.0.0:8008/pokemons/pikachu/moveset

Também é possível buscar um único ataque indicando o índice dele na lista:
- http://0.0.0.0:8008/pokemons/pikachu/moveset/17

Em todo os casos que retorna uma lista de objetos, o limite definido é de 10 itens, entretanto, esse limite pode ser alterado incluindo o parâmetro 'limit' no fim da URL:
- http://0.0.0.0:8008/pokemons?limit=1000


Por fim, outras operações CRUD como create, update e delete podem ser realizados com requisições http, seguindo o formato indicado na documentação da api:
- http://0.0.0.0:8008/docs