from fastapi import APIRouter, HTTPException

from backend.services.arc_rpc import (
    get_balance,
    is_connected,
    latest_block
)

router = APIRouter()

@router.get("/status")
def rpc_status():

    return {
        "connected": is_connected(),
        "latest_block": latest_block()
    }

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
    
from backend.services.score import (
    calculate_score,
    get_badge
)

@router.get("/{address}/summary")
def wallet_summary(address: str):

    balance = get_balance(address)

    score = calculate_score(balance)

    badge = get_badge(score)

    return {
        "address": address,
        "balance": balance,
        "score": score,
        "badge": badge
    }