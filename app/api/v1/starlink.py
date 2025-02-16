from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models.startlink import StarlinkResponse
from app.clients.spacex import SpaceXClient

router = APIRouter(prefix="/starlink", tags=["starlink"])

@router.get("/", response_model=StarlinkResponse)
async def get_starlink(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=1000, description="Items per page")
):
    async with SpaceXClient() as client:
        try:
            options = {
                "page": page,
                "limit": limit,
                "sort": {"spaceTrack.CREATION_DATE": "desc"}
            }
            
            starlink = await client.get_starlink_satellites(options=options)
            return starlink
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
