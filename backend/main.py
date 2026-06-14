from fastapi import FastAPI

app = FastAPI(
    title="Arc Activity Tracker"
)

@app.get("/")
def root():
    return {
        "status": "running"
    }