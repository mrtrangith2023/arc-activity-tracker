from datetime import datetime
from backend.models.score_history import ScoreHistory
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
from backend.services.grade import (
    get_grade
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
from backend.models.database import Base

router = APIRouter()

# ===================================
# Leaderboard
# ===================================   
@router.get("/leaderboard")
def leaderboard():

    return get_leaderboard()

# ====================================
# RPC STATUS
# ====================================

@router.get("/status")
def rpc_status():

    return {
        "connected": is_connected(),
        "latest_block": latest_block()
    }

# ====================================
# GET WATCHLIST
# ====================================

@router.get("/watchlist")
def get_watchlist():

    return load_watchlist()

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

# ====================================
# WALLET SUMMARY
# ====================================

@router.get("/{address}/summary")
def wallet_summary(
    address: str,
    db: Session = Depends(get_db)
):

    try:

        # balance
        balance = get_balance(address)

        # activity
        activity = get_counters(address)

        # transactions
        txs = get_transactions(address)

        # protocols
        protocols = detect_protocols(txs)

        # score
        score = calculate_score(
            activity,
            protocols
        )

        # risk
        risk = calculate_risk(
            activity,
            protocols
        )

        # badge
        badge = get_badge(score)

        # grade
        grade = get_grade(score)

        history = ScoreHistory(
            wallet=address,
            score=score,
            balance=balance,
            grade=grade,
            created_at=datetime.utcnow()
        )

        db = next(get_db())

        db.add(history)
        db.commit()

        return {
        "address": address,
        "balance": balance,
        "score": score,
        "badge": badge,
        "grade": grade,
        "risk": risk,
        "protocol_count": len(protocols),
        "protocols": protocols,
        "activity": activity,
        "timeline": build_timeline(address)
    }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
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