from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your model's Base and set target_metadata for 'autogenerate' support
# Assuming the 'Base' class is in 'models.py'
from models import Base
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Get the database URL from the config file
    url = config.get_main_option("sqlalchemy.url")
    
    # Configure the context with the URL and target_metadata
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # Start the migration process in offline mode
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Set up an engine using the configuration settings
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),  # Get settings from the alembic.ini file
        prefix="sqlalchemy.",  # Prefix for the SQLAlchemy settings in alembic.ini
        poolclass=pool.NullPool,  # Set the pool class for database connections
    )

    # Connect to the database and configure the context
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata  # Pass the metadata for autogenerate support
        )

        # Run the migrations within a transaction
        with context.begin_transaction():
            context.run_migrations()

# Check if we're in offline or online mode and run the appropriate migration function
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
