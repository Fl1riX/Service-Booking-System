from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String(50))
    phone = Column(String(30), unique=True)