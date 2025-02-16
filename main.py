from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import  rockets, launches, starlink

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(rockets.router, prefix=settings.API_V1_STR)
app.include_router(launches.router, prefix=settings.API_V1_STR)
app.include_router(starlink.router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}