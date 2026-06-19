from fastapi import FastAPI
from backend.api.wallets import router
from backend.models.database import (
    Base,
    engine
)

from backend.models.wallet import *
from backend.models.score_history import *

app = FastAPI(
    title="Arc Activity Tracker"
)
Base.metadata.create_all(
    bind=engine
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