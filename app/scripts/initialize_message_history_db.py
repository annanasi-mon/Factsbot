from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from .. import settings
# from dotenv import load_dotenv

# load_dotenv()
print(settings.MESSAGE_HISTORY_DB_DIR)
engine = create_engine(settings.MESSAGE_HISTORY_DB_DIR)
Base = declarative_base()

class Conversations(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer)
    messages = Column(String)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

