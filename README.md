# SQLAlchemy practice

# Installation
1. Set up PostgreSQL as you like
2. Install requirements
```shell
pip install poetry
poetry install --no-root
```

3. Edit ```alembic\env.py```, change ```POSTGRESQL_DSN``` value to your database dsn
4. Run migrations
```shell
alembic upgrade head
```

5. Run admin from ```admin/main.py``` with environment ```POSTGRESQL_DSN```, like ```POSTGRESQL_DSN=postgresql+psycopg2://otus:otus@localhost:5432/sqlalchemy```
6. Run main app from ```app/main.py``` with environment ```POSTGRESQL_DSN```, like ```POSTGRESQL_DSN=postgresql+asyncpg://otus:otus@localhost:5432/sqlalchemy```
