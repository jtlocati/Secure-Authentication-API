from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

#settings on how to spicicly connect to DB
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

#makes temporary sessions to connect to docker for moments in time. then closes
#time is specified in the .env file as ACCESS_TOKEN_EXPIRE_MIN, but can be changed here as well.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
