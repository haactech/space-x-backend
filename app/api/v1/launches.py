from fastapi import APIRouter, HTTPException
from typing import List 
from app.models.launch import Launch
from app.clients.spacex import SpaceXClient

router = APIRouter(prefix="/launches", tags=["launches"])

@router.get("/", response_model=List[Launch])
async def get_launches():
    async with SpaceXClient() as client:
        try:
            launches = await client.get_launches()
            return launches
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
@router.get("/{launch_id}", response_model=Launch)
async def get_launch(launch_id: str):
    async with SpaceXClient() as client:
        try:
            launch = await client.get_launch(launch_id)
            return launch
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))