from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DATETIME, text

from server.model import Base


class Life(Base):
    __tablename__  = 'life'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(VARCHAR(8192), nullable=True)
    category = Column(VARCHAR(45), nullable=True)
    town = Column(VARCHAR(45), nullable=True)
    created_at = Column(DATETIME, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    heart = Column(Integer, nullable=True, default=0)

    nickname = Column(VARCHAR(16), ForeignKey('user.nickname'))


