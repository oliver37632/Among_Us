from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DATETIME, text
from server.model import Base


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(VARCHAR(8192), nullable=True)
    created_at = Column(DATETIME, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    life_id = Column(Integer, ForeignKey('life.id'))
    home_id = Column(Integer, ForeignKey('home.id'))