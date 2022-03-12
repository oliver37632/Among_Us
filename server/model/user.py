from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship

from server.model import Base
from server.model.home import Home
from server.model.life import Life


class User(Base):

    __tablename__ = 'user'

    nickname = Column(VARCHAR(16), primary_key=True)
    password = Column(VARCHAR(16), nullable=True)
    email = Column(VARCHAR(320), nullable=True)

    life = relationship("Life", cascade="all,delete", backref="user")
    home = relationship("Home", cascade="all,delete", backref="user")
    comment = relationship("Comment", cascade="all,delete", backref="user")




