import os
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from alembic import context

# загрузка .env
load_dotenv()

# URL из env
DATABASE_URL = os.getenv("DATABASE_URL")

# это конфиг alembic.ini
config = context.config

# логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# импорт моделей
from app.database import Base  # <-- здесь твоя база
from app import models         # <-- чтобы alembic видел все модели

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
