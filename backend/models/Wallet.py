from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Wallet(Base):

    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)

    address = Column(
        String,
        unique=True
    )

    score = Column(
        Integer,
        default=0
    )