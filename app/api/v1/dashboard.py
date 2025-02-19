# api/dashboard.py
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from app.services.dashboard import DashboardService
from app.models.dashboard import DashboardResponse
from app.clients.spacex import SpaceXClient

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get(
    "/",
    response_model=DashboardResponse,
    summary="Get dashboard data",
    description="Retrieve aggregated statistics and metrics for the SpaceX dashboard with optional filters."
)
async def get_dashboard_data(
    rocket_id: Optional[str] = Query(None, description="Filter launches by rocket ID"),
    start_year: Optional[int] = Query(None, description="Filter launches from this year onward", alias="startYear"),
    end_year: Optional[int] = Query(None, description="Filter launches up to this year", alias="endYear"),
    limit: int = Query(100, description="Number of launches to retrieve per page"),
    page: int = Query(1, description="Pagination page number (1-based)"),
    spacex_client: SpaceXClient = Depends()
) -> DashboardResponse:
    """
    Endpoint para obtener la información del dashboard con filtros opcionales.
    """
    try:
        service = DashboardService(spacex_client)
        return await service.get_dashboard_data(
            rocket_id=rocket_id,
            start_year=start_year,
            end_year=end_year,
            limit=limit,
            page=page
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard data: {e}")
