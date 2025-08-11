from fastapi import FastAPI
from app.api.v1 import pii

app = FastAPI(title="AI Security API")

app.include_router(pii.router, prefix="/api/v1/pii.py", tags=["PII Detection"])