from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, TIMESTAMP, text

from server.model import Base


class Life(Base):
    __tablename__  = 'life'

    idlife = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(VARCHAR(2000), nullable=True)
    image = Column(VARCHAR(255))
    category = Column(VARCHAR(45), nullable=True)
    town = Column(VARCHAR(45), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    user_iduser = Column(Integer, ForeignKey('user.iduser'))


