from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from datetime import datetime

from backend.models.database import Base

class ScoreHistory(Base):

    __tablename__ = "score_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    wallet = Column(
        String,
        index=True
    )

    score = Column(Float)

    balance = Column(Float)

    grade = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )