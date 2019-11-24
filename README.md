# CoCode API

CoCode API Project

## How To Start
```bash
# Start API and MySQL server
$ docker-compose up --build

# Migration
$ docker-compose exec cocode-api python3 main.py db init
$ docker-compose exec cocode-api python3 main.py db migrate
$ docker-compose exec cocode-api python3 main.py db upgrade
```