from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///app/message_history_db/message_history_db.db")
Base = declarative_base()

class Conversations(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer)
    messages = Column(String)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

