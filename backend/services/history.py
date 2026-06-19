from datetime import datetime

from backend.models.score_history import ScoreHistory

def save_snapshot(
    db,
    wallet,
    summary
):

    item = ScoreHistory(

        wallet=wallet,

        score=summary["score"],

        balance=summary["balance"],

        grade=summary["grade"],

        created_at=datetime.utcnow()

    )

    db.add(item)

    db.commit()

    db.refresh(item)

    return item