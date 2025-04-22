import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv


load_dotenv()


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from shared.db.database import Base
from shared.models import chat_models  # noqa: F401 - нужно для регистрации моделей
from services.user_service.models import user_service_model  # noqa: F401


target_metadata = Base.metadata


DB_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)


config = context.config
fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        {"sqlalchemy.url": DB_URL},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        print("Registered tables in metadata:", target_metadata.tables.keys())
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    print("Running migrations in OFFLINE mode")
    run_migrations_offline()
else:
    print("Running migrations in ONLINE mode")
    run_migrations_online()
