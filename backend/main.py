from fastapi import FastAPI
from backend.api.wallets import router

app = FastAPI(
    title="Arc Activity Tracker"
)

app.include_router(
    router,
    prefix="/wallets",
    tags=["wallets"]
)

@app.get("/")
def root():
    return {
        "status": "running"
    }