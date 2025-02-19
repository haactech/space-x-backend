from datetime import datetime
from typing import Dict, List
from collections import defaultdict

from app.models.dashboard import (
    DashboardResponse, SummaryMetrics, RocketComparison,
    LaunchMetrics, StarlinkData, RocketSpecification,
    RocketSuccessRate, YearlyLaunchMetric, LaunchFrequency,
    OrbitalParameters, SatellitePosition
)
from app.models.launch import Launch, LaunchResponse
from app.models.rocket import Rocket
from app.models.startlink import StarlinkResponse, StarlinkSatellite
from app.clients.spacex import SpaceXClient

class DashboardService:
    def __init__(self, spacex_client: SpaceXClient):
        self.client = spacex_client

    async def get_dashboard_data(self) -> DashboardResponse:
        """
        Fetch and aggregate dashboard data from SpaceX API
        """
        rockets_data = await self.client.get_rockets()
        launches_data = await self.client.get_launches()
        starlink_data = await self.client.get_starlink_satellites()

        rockets = [Rocket(**rocket) for rocket in rockets_data]
        launches = [Launch(**launch) for launch in launches_data]
        
        starlink = []
        for sat in starlink_data:
            if isinstance(sat, dict):
                starlink.append(StarlinkSatellite(**sat))
            else:
                continue

        return DashboardResponse(
            summary_metrics=await self._get_summary_metrics(rockets, launches, starlink),
            rocket_comparison=await self._get_rocket_comparisons(rockets, launches),  # Removed 's'
            launch_metrics=await self._get_launch_metrics(launches),
            starlink_data=await self._get_starlink_data(starlink)
        )

    async def _get_summary_metrics(
        self, 
        rockets: List[Rocket], 
        launches: List[Launch], 
        starlink: List[StarlinkSatellite]
    ) -> SummaryMetrics:
        completed_launches = [l for l in launches if not l.upcoming]
        successful_launches = [l for l in completed_launches if l.success]
        
        return SummaryMetrics(
            total_launches=len(launches),
            success_rate=len(successful_launches) / len(completed_launches) * 100 if completed_launches else 0,
            active_rockets=len([r for r in rockets if r.active]),
            total_starlink_satellites=len(starlink)
        )

    async def _get_rocket_comparisons(
        self, 
        rockets: List[Rocket], 
        launches: List[Launch]
    ) -> RocketComparison:
        specifications = [
            RocketSpecification(
                name=rocket.name,
                height_m=rocket.height.meters,
                mass_kg=rocket.mass.kg,
                success_rate=rocket.success_rate_pct,
                cost_per_launch=rocket.cost_per_launch
            )
            for rocket in rockets
        ]

        success_rates = []
        for rocket in rockets:
            rocket_launches = [l for l in launches if l.rocket == rocket.id]
            successful = len([l for l in rocket_launches if l.success])
            
            success_rates.append(
                RocketSuccessRate(
                    name=rocket.name,
                    total_launches=len(rocket_launches),
                    successful_launches=successful,
                    rate=successful / len(rocket_launches) * 100 if rocket_launches else 0
                )
            )

        return RocketComparison(
            specifications=specifications,
            success_rates=success_rates
        )

    async def _get_launch_metrics(self, launches: List[Launch]) -> LaunchMetrics:
        launches_by_year = defaultdict(lambda: {"total": 0, "successful": 0})
        frequency_data = defaultdict(int)

        for launch in launches:
            if launch.upcoming:
                continue

            date = datetime.fromisoformat(launch.date_utc.replace("Z", "+00:00"))
            year = date.year
            
            launches_by_year[year]["total"] += 1
            if launch.success:
                launches_by_year[year]["successful"] += 1
            
            month_key = date.strftime("%Y-%m")
            frequency_data[month_key] += 1

        yearly_data = [
            YearlyLaunchMetric(
                year=year,
                total=data["total"],
                successful=data["successful"],
                rate=data["successful"] / data["total"] * 100 if data["total"] > 0 else 0
            )
            for year, data in launches_by_year.items()
        ]

        frequency = [
            LaunchFrequency(date=date, launches=count)
            for date, count in frequency_data.items()
        ]

        return LaunchMetrics(
            by_year=sorted(yearly_data, key=lambda x: x.year),
            frequency_data=sorted(frequency, key=lambda x: x.date)
        )

    async def _get_starlink_data(self, starlink: List[StarlinkSatellite]) -> StarlinkData:
        versions = defaultdict(lambda: {
            "count": 0,
            "height_sum": 0,
            "velocity_sum": 0
        })

        positions = []

        for satellite in starlink:
            if satellite.version:
                version_data = versions[satellite.version]
                version_data["count"] += 1
                
                if satellite.height_km:
                    version_data["height_sum"] += satellite.height_km
                if satellite.velocity_kms:
                    version_data["velocity_sum"] += satellite.velocity_kms

            if all(v is not None for v in [
                satellite.latitude,
                satellite.longitude,
                satellite.height_km
            ]):
                positions.append(
                    SatellitePosition(
                        id=satellite.id,
                        latitude=satellite.latitude,
                        longitude=satellite.longitude,
                        height_km=satellite.height_km
                    )
                )

        orbital_parameters = [
            OrbitalParameters(
                version=version,
                count=data["count"],
                average_height_km=data["height_sum"] / data["count"] if data["count"] > 0 else 0,
                average_velocity_kms=data["velocity_sum"] / data["count"] if data["count"] > 0 else 0
            )
            for version, data in versions.items()
        ]

        return StarlinkData(
            orbital_parameters=orbital_parameters,
            satellite_positions=positions
        )