from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.config import settings
# Import the 'routers' we are about to create. A router is just a collection of API endpoints.
from api.routers import scan, enforce

# Create the main application instance. This is the core of our API.
app = FastAPI(title="GovernAble API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scan.router, prefix=f"{settings.API_V1_STR}/scan", tags=["scan"])
app.include_router(enforce.router, prefix=f"{settings.API_V1_STR}/enforce", tags=["enforce"])

@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.ENV}