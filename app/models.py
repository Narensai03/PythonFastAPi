from sqlalchemy import Column, Integer
from sqlalchemy.sql.expression import text, true
from sqlalchemy.sql.sqltypes import TIMESTAMP, String
from .database import Base

class user(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key= True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    type = Column(String, nullable=False)
    create_at = Column(TIMESTAMP(timezone=true), nullable=False, server_default=text('now()'))

