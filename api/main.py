from fastapi import FastAPI
from api.routes import scan

app = FastAPI(title="AI Security API")
app.include_router(scan.router, prefix="/scan", tags=["Scan"])
