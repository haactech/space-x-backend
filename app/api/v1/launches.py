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

            # Get launches from SpaceX API
            response = await client.get_launches(query=query, options=options)
            
            # Handle different response formats
            if isinstance(response, list):
                # If response is a list, convert it to LaunchResponse format
                return LaunchResponse.from_api_response(response)
            elif isinstance(response, dict):
                # If response is already paginated, process the docs
                if "docs" in response:
                    # Ensure each launch in docs is properly validated
                    validated_launches = []
                    for launch_data in response["docs"]:
                        try:
                            validated_launch = Launch(**launch_data)
                            validated_launches.append(validated_launch)
                        except Exception as e:
                            print(f"Error validating launch: {str(e)}")
                            continue
                    
                    # Update the docs with validated launches
                    response["docs"] = validated_launches
                    return LaunchResponse(**response)
                else:
                    # Single launch response
                    return LaunchResponse(
                        docs=[Launch(**response)],
                        totalDocs=1,
                        limit=1,
                        totalPages=1,
                        page=1,
                        pagingCounter=1
                    )
            
            raise HTTPException(
                status_code=500,
                detail="Invalid response format from SpaceX API"
            )
            
        except Exception as e:
            print(f"Error fetching launches: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching launches: {str(e)}"
            )

@router.get("/upcoming", response_model=List[Launch])
async def get_upcoming_launches():
    async with SpaceXClient() as client:
        try:
            launches_data = await client.get_upcoming_launches()
            return [Launch(**launch) for launch in launches_data]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
@router.get("/{launch_id}", response_model=Launch)
async def get_launch(launch_id: str):
    async with SpaceXClient() as client:
        try:
            launch_data = await client.get_launch(launch_id)
            if not launch_data:
                raise HTTPException(status_code=404, detail="Launch not found")
            return Launch(**launch_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))