"""SQLAlchemy engine + session setup.

TODO:
  - create_engine() pointed at config.database_url
  - a SessionLocal sessionmaker
  - a get_db() FastAPI dependency that yields a session and closes it
  - a Base = declarative_base() for models.py to import
"""
