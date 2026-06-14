from fastapi import APIRouter

router = APIRouter()

@router.get("/{address}")
def get_wallet(address: str):

    return {
        "address": address,
        "score": 0,
        "transactions": 0
    }