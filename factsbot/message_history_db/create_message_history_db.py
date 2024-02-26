from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///message_history_db.db")
Base = declarative_base()


class Conversations(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer)
    messages = Column(String)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


