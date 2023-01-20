from sqlalchemy import Column, Integer, String, DateTime,ARRAY, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    image = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    audios = relationship(
        "AudioModel", back_populates="user", cascade="all, delete-orphan")


class AudioModel(Base):
    __tablename__ = "audio"
    session_id = Column(Integer, primary_key=True, index=True, unique=True)
    step_count = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    selected_tick = Column(Integer)
    ticks = Column(ARRAY(Numeric))
    user = relationship("UserModel", back_populates="audios")
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
