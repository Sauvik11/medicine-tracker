# backend/models/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config
from .models import Base  # Now works because of __init__.py
import logging

logger = logging.getLogger(__name__)

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    echo=False,
    pool_pre_ping=True,
    future=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DBSession = scoped_session(SessionLocal)

def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        Base.metadata.create_all(bind=engine, checkfirst=True)
        logger.info("Tables ensured via SQLAlchemy ORM")
    except Exception as e:
        logger.error(f"DB init failed: {e}")
        raise