from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
from typing import Dict, Any, List
from contextlib import contextmanager

from app.logging.utils import get_app_logger
logger = get_app_logger("database")

from app.config.settings import OMSConfigs
configs = OMSConfigs()

DATABASE_URL = configs.DATABASE_URL
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

DATABASE_READ_URL = configs.DATABASE_READ_URL
if DATABASE_READ_URL and DATABASE_READ_URL.startswith("postgresql://"):
    DATABASE_READ_URL = DATABASE_READ_URL.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

read_engine = create_engine(
    DATABASE_READ_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
) if DATABASE_READ_URL != DATABASE_URL else engine

ReadSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=read_engine)

def execute_raw_sql_readonly(query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    db = ReadSessionLocal()
    try:
        result = db.execute(text(query), params or {})
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]
    finally:
        db.close()


