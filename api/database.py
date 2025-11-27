from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "sqlite:///./NailBooking.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()



