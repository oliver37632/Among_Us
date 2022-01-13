from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, TIMESTAMP, text

from server.model import Base
from server.model import user


class Life(Base):
    __talbname__ = 'life'

    idlife = Column(Integer, primary_key=True)
    content = Column(VARCHAR(2000), nullable=True)
    photo = Column(VARCHAR(255))
    kategorie = Column(VARCHAR(45), nullable=True)
    town = Column(VARCHAR(45), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    user_iduser = Column(Integer, ForeignKey(user.iduser))


