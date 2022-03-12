from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DATETIME, text

from server.model import Base


class Home(Base):
    __tablename__ = 'home'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(50), nullable=True)
    content = Column(VARCHAR(8192), nullable=True)
    category = Column(VARCHAR(45), nullable=True)
    town = Column(VARCHAR(45), nullable=True)
    price = Column(VARCHAR(10), nullable=True)
    created_at = Column(DATETIME, nullable=True, server_default=text("CURRENT_TIMESTAMP"))

    nickname = Column(VARCHAR(16), ForeignKey('user.nickname'))


