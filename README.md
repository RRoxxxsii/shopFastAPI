<h1>Маркетплейс API</h1>
<br>

<h3>Технологии:</h3>

`FastAPI`, `SQLAlchemy`, `Alembic`, `Pydantic`, `PostgreSQL`, `asyncpg`, `asyncio`, `aiohttp`, `pytest`, `Docker`

<h3>
Запуск:
</h3>

1. `git clone https://github.com/RRoxxxsii/shopFastAPI.git`
2. `Вставить файл .env в корне на уровне с Dockerfile`
3. `docker compose up --build`

<h3>Пример .env: </h3>

```
POSTGRES_USER=marketplace_user
POSTGRES_PASSWORD=marketplace_password
POSTGRES_DB=marketplace_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

PGADMIN_DEFAULT_EMAIL=example@gmail.com
PGADMIN_DEFAULT_PASSWORD=password
```
