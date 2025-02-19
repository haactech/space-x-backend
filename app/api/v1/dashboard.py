from fastapi import APIRouter, HTTPException, Depends 
from app.services.dashboard import DashboardService
from app.models.dashboard import DashboardResponse
from app.clients.spacex import SpaceXClient

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get(
    "/",
    response_model=DashboardResponse,
    summary="Get dashboard data",
    description="Retrieve aggregated statistics and metrics for the SpaceX dashboard."
)
async def get_dashboard_data(
    spacex_client: SpaceXClient = Depends()
) -> DashboardResponse:
    try: 
        service  = DashboardService(spacex_client)
        return await service.get_dashboard_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard data: {e}")