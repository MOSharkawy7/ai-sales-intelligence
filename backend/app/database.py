import os

from pathlib import Path

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# --------------------------------------------------
# Project root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ENV_PATH = PROJECT_ROOT / ".env"


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv(
    dotenv_path=ENV_PATH
)


DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


if not DATABASE_URL:

    raise ValueError(
        f"DATABASE_URL is not configured. "
        f"Expected .env file at: {ENV_PATH}"
    )


# --------------------------------------------------
# Database engine
# --------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# --------------------------------------------------
# Session
# --------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# --------------------------------------------------
# Base model
# --------------------------------------------------

Base = declarative_base()


# --------------------------------------------------
# Database dependency
# --------------------------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()