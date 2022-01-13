from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship

from server.model import Base


class User(Base):
    __tablename__ = 'user'

    iduser = Column(Integer, primary_key=True)
    nickname = Column(VARCHAR(16), nullable=True)
    password = Column(VARCHAR(100), nullable=True)
    email = Column(VARCHAR(320), nullable=True)

    home = relationship("home", cascade="all, delete", backref="user")
    life = relationship("life", canonical="all, delete", backref="user")
