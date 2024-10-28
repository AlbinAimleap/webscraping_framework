from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from aio_http.core.db import BaseModel

class Flags(BaseModel):
    __tablename__ = 'flags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nsfw = Column(Boolean, default=False)
    religious = Column(Boolean, default=False)
    political = Column(Boolean, default=False)
    racist = Column(Boolean, default=False)
    sexist = Column(Boolean, default=False)
    explicit = Column(Boolean, default=False)

    jokes = relationship("Joke", back_populates="flags", cascade="all, delete-orphan")


class Joke(BaseModel):
    __tablename__ = 'jokes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    error = Column(Boolean, default=False)
    category = Column(String(50), nullable=False)
    joke_type = Column(String(50), nullable=False)
    joke = Column(String(500), nullable=True)
    setup = Column(String(500), nullable=True)
    delivery = Column(String(500), nullable=True)
    safe = Column(Boolean, default=True)
    lang = Column(String(10), nullable=False)

    flags_id = Column(Integer, ForeignKey('flags.id'))
    flags = relationship("Flags", back_populates="jokes")

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="jokes")


class User(BaseModel):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)

    jokes = relationship("Joke", back_populates="user", cascade="all, delete-orphan")
