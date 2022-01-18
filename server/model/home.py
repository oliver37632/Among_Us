from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, TIMESTAMP, text

from server.model import Base
from server.model import user


class Home(Base):
    __talbname__ = 'home'

    idhoem = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(50), nullable=True)
    content = Column(VARCHAR(2000), nullable=True)
    image = Column(VARCHAR(255))
    category = Column(VARCHAR(45), nullable=True)
    town = Column(VARCHAR(45), nullable=True)
    price = Column(VARCHAR(100), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    user_iduser = Column(Integer, ForeignKey(user.iduser))


