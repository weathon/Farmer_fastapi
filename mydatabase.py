from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, func, select
import databases
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import sqlalchemy

DATABASE_URL = "sqlite:///./test.db"


database = databases.Database(DATABASE_URL)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
