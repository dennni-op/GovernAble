from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.config import settings
# Import the 'routers' we are about to create. A router is just a collection of API endpoints.
from api.routers import scan, enforce

# Create the main application instance. This is the core of our API.
app = FastAPI(title="GovernAble API", version="0.1.0")
# This is important! It's called CORS middleware.
# Analogy: By default, a web browser (like Chrome) won't let a website from one address
# (e.g., my-dashboard.com) talk to an API at another address (e.g., api.governable.com).
# This middleware tells the browser, "It's okay, I trust these websites."
# The setting "CORS_ORIGINS: '*'" means we trust *everyone* for now.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Here, we're telling our main app to include the endpoints from our router files.
# We're adding the 'scan' router and giving it a prefix, so all its URLs will
# start with /api/v1/scan.
app.include_router(scan.router, prefix=f"{settings.API_V1_STR}/scan", tags=["scan"])
app.include_router(enforce.router, prefix=f"{settings.API_V1_STR}/enforce", tags=["enforce"])
# This is a simple "health check" endpoint. It's a common practice to have a URL
# that just returns "ok" so you can easily check if your API is running.
@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.ENV}