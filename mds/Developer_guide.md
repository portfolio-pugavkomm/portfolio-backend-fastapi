# Developer guide

## Local start project

You need to install the [uv](https://docs.astral.sh/uv/) package manager.
After that, you need to install all dependencies:

```bash
uv install --extra=dev
```

Then, you can use follow command:

```bash
fastapi dev src/main.py
```

## Docker start project

You need to install docker (or docker desktop)

Use the follow command:

```bash
docker compose up
```

> You also need to copy file .env.example to .env and configure parameters

## environment

Environment variables will be described here

> Please read .env.example firstly, because this section may not be updated in timely manner

- `BACKEND_PORT` - external backend port.
- `DB_USER` - database username
- `DB_PASS` - database password
- `DB` - database name
- `DB_PORT` - database port
- `COMPOSE_PROFILES` - specify which service profiles to enable (database or (and backend))
