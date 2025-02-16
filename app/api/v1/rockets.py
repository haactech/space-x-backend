from fastapi import  APIRouter, HTTPException 
from typing import List 
from app.models.rocket import Rocket
from app.clients.spacex import SpaceXClient

router = APIRouter(prefix="/rockets", tags=["rockets"])

@router.get("/", response_model=List[Rocket])
async def get_rockets():
    async with SpaceXClient() as client:
        try:
            rockets = await client.get_rockets()
            return rockets

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/{rocket_id}", response_model=Rocket)
async def get_rocket(rocket_id: str):
    async with SpaceXClient() as client: 
        try:
            rocket = await client.get_rocket(rocket_id)
            return rocket

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))