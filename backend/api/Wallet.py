from fastapi import APIRouter

router = APIRouter(
    prefix="/wallets",
    tags=["wallets"]
)

@router.get("/")
def get_wallets():
    return {
        "wallets": []
    }