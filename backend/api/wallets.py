from datetime import datetime
from backend.services.arc_rpc import (
    get_balance,
    is_connected,
    latest_block
)

from backend.services.arcscan import (
    get_address,
    get_counters,
    get_transactions
)

from backend.services.ecosystem import (
    detect_protocols
)

from backend.services.score import (
    calculate_score,
    get_badge
)
from backend.services.leaderboard import (
    get_leaderboard
)
from backend.services.timeline import (
    build_timeline
)
from backend.services.risk import (
    calculate_risk
)
from backend.services.wallet_intelligence import (
    build_wallet_insights
)
from backend.services.grade import (
    get_grade
)
from backend.services.scoring_engine import (
    score_breakdown
)
from backend.services.watchlist import (
    load_watchlist,
    add_wallet,
    remove_wallet
)
from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)
from sqlalchemy.orm import Session
from backend.models.database import get_db
from backend.models.score_history import ScoreHistory
from backend.services.protocol_analytics import (
    get_protocol_ranking
)
from backend.services.ai_wallet_coach import wallet_coach
from backend.services.wallet_summary_service import (
    build_wallet_summary
)

router = APIRouter()

# ====================================
# RPC STATUS
# ====================================

@router.get("/status")
def rpc_status():

    return {
        "connected": is_connected(),
        "latest_block": latest_block()
    }

# ===================================
# ECOSYSTEM TREND
# ===================================

@router.get("/ecosystem-trend")
def ecosystem_trend(
    db: Session = Depends(get_db)
):

    rows = db.query(
        ScoreHistory
    ).all()

    if not rows:

        return {
            "wallet_growth": 0,
            "snapshot_growth": 0,
            "avg_score_growth": 0
        }

    wallets = len(
        set(
            row.wallet
            for row in rows
        )
    )

    snapshots = len(rows)

    avg_score = round(
        sum(
            row.score
            for row in rows
        ) / snapshots,
        2
    )

    return {
        "wallet_growth": wallets,
        "snapshot_growth": snapshots,
        "avg_score_growth": avg_score
    }

# ===================================
# TOP PROTOCOLS
# ===================================

@router.get("/top-protocols")
def top_protocols():

    return [
        "UnitFlow",
        "PredictMarket",
        "XyloVault",
        "XyloStablePool"
    ]

# ====================================
# WALLET SUMMARY
# ====================================

@router.get("/{address}/summary")
def wallet_summary(
    address: str,
    db: Session = Depends(get_db)
):

    try:

        summary = build_wallet_summary(address)

        history = ScoreHistory(
            wallet=summary["address"],

            score=summary["score"],

            balance=summary["balance"],

            grade=summary["grade"],

            protocols=",".join(summary["protocols"]),

            created_at=datetime.utcnow()
        )

        db.add(history)

        db.commit()

        db.refresh(history)

        return summary

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# ====================================
# SCORE BREAKDOWN
# ====================================

@router.get(
    "/{address}/score-breakdown"
)
def score_breakdown_api(
    address: str
):

    try:

        balance = get_balance(
            address
        )

        activity = get_counters(
            address
        )

        txs = get_transactions(
            address
        )

        protocols = detect_protocols(
            txs
        )

        return score_breakdown(
            balance,
            activity,
            protocols
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# ===================================
# COACH_AI
# ===================================
@router.get("/{address}/coach")
def wallet_ai_coach(address: str):

    try:

        summary = build_wallet_summary(address)

        return wallet_coach(summary)

    except Exception as e:

        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ===================================
# ANALYTICS
# ===================================

@router.get("/analytics")
def analytics(
    db: Session = Depends(get_db)
):

    rows = db.query(
        ScoreHistory
    ).all()

    if not rows:

        return {
            "wallets": 0,
            "snapshots": 0,
            "avg_score": 0,
            "avg_balance": 0
        }

    wallets = len(
        set(
            row.wallet
            for row in rows
        )
    )

    snapshots = len(rows)

    avg_score = round(
        sum(
            row.score
            for row in rows
        ) / snapshots,
        2
    )

    avg_balance = round(
        sum(
            row.balance
            for row in rows
        ) / snapshots,
        2
    )

    return {
        "wallets": wallets,
        "snapshots": snapshots,
        "avg_score": avg_score,
        "avg_balance": avg_balance
    }


# ====================================
# WALLET RANKING
# ====================================

@router.get("/ranking")
def wallet_ranking(
    db: Session = Depends(get_db)
):

    rows = db.query(
        ScoreHistory
    ).all()

    latest_wallets = {}

    for row in rows:

        if (
            row.wallet not in latest_wallets
            or
            row.created_at >
            latest_wallets[row.wallet].created_at
        ):

            latest_wallets[row.wallet] = row

    ranking = list(
        latest_wallets.values()
    )

    ranking.sort(
        key=lambda x: x.score,
        reverse=True
    )

    return ranking[:20]


# ====================================
# GRADE DISTRIBUTION
# ====================================

@router.get("/grade-distribution")
def grade_distribution(
    db: Session = Depends(get_db)
):

    rows = db.query(
        ScoreHistory
    ).all()

    grades = {
        "S": 0,
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0
    }

    latest_wallets = {}

    for row in rows:

        if (
            row.wallet not in latest_wallets
            or
            row.created_at >
            latest_wallets[row.wallet].created_at
        ):

            latest_wallets[row.wallet] = row

    for wallet in latest_wallets.values():

        grade = wallet.grade

        if grade in grades:

            grades[grade] += 1

    return grades


# ====================================
# ECOSYSTEM HEALTH
# ====================================

@router.get("/health-score")
def health_score(
    db: Session = Depends(get_db)
):

    rows = db.query(
        ScoreHistory
    ).all()

    if not rows:

        return {
            "health_score": 0
        }

    avg_score = (

        sum(
            row.score
            for row in rows
        )

        /

        len(rows)

    )

    health = round(
        (
            avg_score
            /
            5000
        )
        * 100,
        2
    )

    return {
        "health_score": health
    }

# ===================================
# PROTOCOL RANKING
# ===================================

@router.get("/protocol-ranking")
def protocol_ranking(
    db: Session = Depends(get_db)
):

    rows = db.query(
        ScoreHistory
    ).all()

    ranking = get_protocol_ranking(
        rows
    )

    return ranking

# ===================================
# RISK DISTRIBUTION
# ===================================

@router.get("/risk-distribution")
def risk_distribution(
    db: Session = Depends(get_db)
):

    rows = db.query(
        ScoreHistory
    ).all()

    result = {
        "Low": 0,
        "Medium": 0,
        "High": 0
    }

    for row in rows:

        if row.score >= 1000:

            result["Low"] += 1

        elif row.score >= 300:

            result["Medium"] += 1

        else:

            result["High"] += 1

    return result

# ===================================
# Leaderboard
# ===================================
   
@router.get("/leaderboard")
def leaderboard():

    return get_leaderboard()


# ====================================
# GET WATCHLIST
# ====================================

@router.get("/watchlist")
def get_watchlist():

    return load_watchlist()


# ====================================
# WATCHLIST STATUS
# ====================================

@router.get("/watchlist-status")
def watchlist_status(
    db: Session = Depends(get_db)
):

    wallets = load_watchlist()

    result = []

    for wallet in wallets:

        rows = (

            db.query(
                ScoreHistory
            )

            .filter(
                ScoreHistory.wallet == wallet
            )

            .order_by(
                ScoreHistory.created_at.desc()
            )

            .limit(2)

            .all()

        )

        current_score = None
        previous_score = None
        delta = 0

        if rows:

            current_score = rows[0].score

        if len(rows) > 1:

            previous_score = rows[1].score
            delta = current_score - previous_score

        if delta > 0:

            direction = "increase"
            indicator = "up"

        elif delta < 0:

            direction = "decrease"
            indicator = "down"

        else:

            direction = "unchanged"
            indicator = "flat"

        result.append(
            {
                "wallet": wallet,
                "current_score": current_score,
                "previous_score": previous_score,
                "delta": delta,
                "direction": direction,
                "indicator": indicator
            }
        )

    return result

# ====================================
# POST WATCHLIST
# ====================================

@router.post("/watchlist/{address}")
def add_to_watchlist(
    address: str
):

    return add_wallet(address)

# ====================================
# DELETE WATCHLIST
# ====================================

@router.delete("/watchlist/{address}")
def delete_wallet(
    address: str
):

    return remove_wallet(address)

# ====================================
# TOP-WALLETS
# ====================================

@router.get("/top-wallets")
def top_wallets(
    db: Session = Depends(get_db)
):

    rows = (

        db.query(
            ScoreHistory
        )

        .order_by(
            ScoreHistory.score.desc()
        )

        .limit(20)

        .all()

    )

    return rows
    
# ====================================
# HISTORY
# ====================================

@router.get("/{wallet}/history")
def get_history(
    wallet: str,
    db: Session = Depends(get_db)
):

    rows = (

        db.query(
            ScoreHistory
        )

        .filter(
            ScoreHistory.wallet == wallet
        )

        .order_by(
            ScoreHistory.created_at
        )

        .all()

    )

    return rows

# ====================================
# WALLET BALANCE
# ====================================

@router.get("/{address}")
def wallet(address: str):

    try:

        balance = get_balance(address)

        return {
            "address": address,
            "balance": balance
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
# ====================================
# ADDRESS DETAILS
# ====================================

@router.get("/{address}/details")
def wallet_details(address: str):

    try:

        return get_address(address)

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ====================================
# ACTIVITY COUNTERS
# ====================================

@router.get("/{address}/activity")
def activity(address: str):

    try:

        return get_counters(address)

    except Exception:

        raise HTTPException(
            status_code=404,
            detail="Wallet has no on-chain activity"
        )


# ====================================
# TRANSACTIONS
# ====================================

@router.get("/{address}/transactions")
def transactions(address: str):

    try:

        return get_transactions(address)

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ====================================
# PROTOCOL DETECTOR
# ====================================

@router.get("/{address}/protocols")
def wallet_protocols(address: str):

    try:

        txs = get_transactions(address)

        protocols = detect_protocols(txs)

        return {
            "address": address,
            "protocols": protocols,
            "protocol_count": len(protocols)
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# ====================================
# TIMELINE
# ====================================

@router.get("/{address}/timeline")
def wallet_timeline(address: str):

    return build_timeline(address)