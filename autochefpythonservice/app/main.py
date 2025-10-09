from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(title="AutoChef Python LLM Service")
app.include_router(endpoints.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
