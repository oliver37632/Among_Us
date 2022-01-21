from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship

from server.model import Base
from server.model.home import Home
from server.model.life import Life


class User(Base):
    __tablename__ = 'user'

    iduser = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(VARCHAR(16), nullable=True)
    password = Column(VARCHAR(100), nullable=True)
    email = Column(VARCHAR(320), nullable=True)

    life = relationship("Life", cascade="all,delete", backref="user")
    home = relationship("Home", cascade="all,delete", backref="user")

