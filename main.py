from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Add this import
from app.core.config import settings
from app.api.v1 import  rockets, launches, starlink, dashboard

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(rockets.router, prefix=settings.API_V1_STR)
app.include_router(launches.router, prefix=settings.API_V1_STR)
app.include_router(starlink.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}