from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.launch import Launch, LaunchResponse
from app.clients.spacex import SpaceXClient

router = APIRouter(prefix="/launches", tags=["launches"])

@router.get("/", response_model=LaunchResponse)
async def get_launches(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    sort: str = Query("date_utc", description="Sort field"),
    order: str = Query("desc", description="Sort order (asc/desc)"),
    upcoming: Optional[bool] = Query(None, description="Filter upcoming launches"),
    success: Optional[bool] = Query(None, description="Filter by launch success")
):
    async with SpaceXClient() as client:
        try:
            # Construct query and options
            query = {}
            if upcoming is not None:
                query["upcoming"] = upcoming
            if success is not None:
                query["success"] = success

            options = {
                "page": page,
                "limit": limit,
                "sort": {
                    sort: 1 if order == "asc" else -1
                },
                "pagination": True
            }

            launches = await client.get_launches(query=query, options=options)
            return launches
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/upcoming", response_model=List[Launch])
async def get_upcoming_launches():
    async with SpaceXClient() as client:
        try:
            launches = await client.get_upcoming_launches()
            return launches
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
@router.get("/{launch_id}", response_model=Launch)
async def get_launch(launch_id: str):
    async with SpaceXClient() as client:
        try:
            launch = await client.get_launch(launch_id)
            if not launch:
                raise HTTPException(status_code=404, detail="Launch not found")
            return launch
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))