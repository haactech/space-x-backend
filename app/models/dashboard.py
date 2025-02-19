from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime

class SummaryMetrics(BaseModel):
    total_launches: int
    success_rate: float
    active_rockets: int
    total_starlink_satellites: int 

class RocketSpecification(BaseModel):
    name: str 
    height_m: float
    mass_kg: float
    success_rate: float 
    cost_per_launch: int 

class RocketSuccessRate(BaseModel):
    name: str 
    total_launches: int
    successful_launches: int 
    rate: float 

class RocketComparison(BaseModel):
    specifications: List[RocketSpecification]
    success_rates: List[RocketSuccessRate]

class YearlyLaunchMetric(BaseModel):
    year: int 
    total: int 
    successful: int 
    rate: float

class LaunchFrequency(BaseModel):
    date: str 
    launches: int 

class LaunchMetrics(BaseModel):
    by_year: List[YearlyLaunchMetric]
    frequency_data: List[LaunchFrequency]

class OrbitalParameters(BaseModel):
    version: str 
    count: int
    average_height_km: float
    average_velocity_kms: float

class SatellitePosition(BaseModel):
    id: str 
    latitude: Optional[float]
    longitude: Optional[float]
    height_km: Optional[float]

class StarlinkData(BaseModel):
    orbital_parameters: List[OrbitalParameters]
    satellite_positions: List[SatellitePosition]

class DashboardResponse(BaseModel):
    summary_metrics: SummaryMetrics
    rocket_comparison: RocketComparison
    launch_metrics: LaunchMetrics
    starlink_data: StarlinkData

    class Config:
            schema_extra = {
                "example": {
                    "summary_metrics": {
                        "total_launches": 100,
                        "success_rate": 98.5,
                        "active_rockets": 3,
                        "total_starlink_satellites": 1500
                    },
                    "rockets_comparison": {
                        "specifications": [
                            {
                                "name": "Falcon 9",
                                "height_m": 70,
                                "mass_kg": 549054,
                                "success_rate": 98,
                                "cost_per_launch": 67000000
                            }
                        ],
                        "success_rates": [
                            {
                                "name": "Falcon 9",
                                "total_launches": 100,
                                "successful_launches": 98,
                                "rate": 98
                            }
                        ]
                    },
                    "launch_metrics": {
                        "by_year": [
                            {
                                "year": 2022,
                                "total": 50,
                                "successful": 49,
                                "rate": 98
                            }
                        ],
                        "frequency_data": [
                            {
                                "date": "2022-01",
                                "launches": 5
                            }
                        ]
                    },
                    "starlink_data": {
                        "orbital_parameters": [
                            {
                                "version": "v1.5",
                                "count": 500,
                                "average_height_km": 550,
                                "average_velocity_kms": 7.8
                            }
                        ],
                        "satellite_positions": [
                            {
                                "id": "5eed770f096e59000698560d",
                                "latitude": 45.1,
                                "longitude": -82.3,
                                "height_km": 550
                            }
                        ]
                    }
                }
            }