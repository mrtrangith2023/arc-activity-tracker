from sqlalchemy.orm import Session

from backend.models.score_history import ScoreHistory


def get_wallet_history(
    db: Session,
    wallet: str,
    limit: int = 30
):

    history = (
        db.query(ScoreHistory)
        .filter(
            ScoreHistory.wallet == wallet
        )
        .order_by(
            ScoreHistory.created_at
        )
        .limit(limit)
        .all()
    )

    return history