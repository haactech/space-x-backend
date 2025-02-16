from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Measurement(BaseModel):
    meters: Optional[float] = Field(None, description="Measurement in meters")
    feet: Optional[float] = Field(None, description="Measurement in feet")

class Mass(BaseModel):
    kg: float = Field(..., description="Mass in kilograms")
    lb: float = Field(..., description="Mass in pounds")

class Thrust(BaseModel):
    kN: float = Field(..., description="Thrust in kilonewtons")
    lbf: float = Field(..., description="Thrust in pounds-force")

class ISP(BaseModel):
    sea_level: int = Field(..., description="Specific impulse at sea level")
    vacuum: int = Field(..., description="Specific impulse in vacuum")

class CompositeFairing(BaseModel):
    height: Optional[Measurement] = Field(None, description="Height of the fairing")
    diameter: Optional[Measurement] = Field(None, description="Diameter of the fairing")

class PayloadVolume(BaseModel):
    composite_fairing: Optional[CompositeFairing] = Field(None, description="Composite fairing details")
    option_1: Optional[str] = Field(None, description="Payload fairing option")

class FirstStage(BaseModel):
    thrust_sea_level: Thrust
    thrust_vacuum: Thrust
    reusable: bool
    engines: int
    fuel_amount_tons: float
    burn_time_sec: Optional[int]

class SecondStage(BaseModel):
    thrust: Thrust
    payloads: PayloadVolume
    reusable: bool
    engines: int
    fuel_amount_tons: float
    burn_time_sec: Optional[int]

class Engine(BaseModel):
    isp: ISP
    thrust_sea_level: Thrust
    thrust_vacuum: Thrust
    number: int
    type: str
    version: str
    layout: Optional[str] = None
    engine_loss_max: Optional[int] = None
    propellant_1: str
    propellant_2: str
    thrust_to_weight: float

class LandingLegs(BaseModel):
    number: int
    material: Optional[str]

class PayloadWeight(BaseModel):
    id: str
    name: str
    kg: int
    lb: int

class Rocket(BaseModel):
    height: Measurement
    diameter: Measurement
    mass: Mass
    first_stage: FirstStage
    second_stage: SecondStage
    engines: Engine
    landing_legs: LandingLegs
    payload_weights: List[PayloadWeight]
    flickr_images: List[str]
    name: str
    type: str
    active: bool
    stages: int
    boosters: int
    cost_per_launch: int
    success_rate_pct: int
    first_flight: str
    country: str
    company: str
    wikipedia: Optional[str]
    description: str
    id: str

    class Config:
        schema_extra = {
            "example": {
                "height": {
                    "meters": 22.25,
                    "feet": 73
                },
                "diameter": {
                    "meters": 1.68,
                    "feet": 5.5
                },
                "mass": {
                    "kg": 30146,
                    "lb": 66460
                },
                "first_stage": {
                    "thrust_sea_level": {
                        "kN": 420,
                        "lbf": 94000
                    },
                    "thrust_vacuum": {
                        "kN": 480,
                        "lbf": 110000
                    },
                    "reusable": False,
                    "engines": 1,
                    "fuel_amount_tons": 44.3,
                    "burn_time_sec": 169
                },
                "second_stage": {
                    "thrust": {
                        "kN": 31,
                        "lbf": 7000
                    },
                    "payloads": {
                        "composite_fairing": {
                            "height": {
                                "meters": 3.5,
                                "feet": 11.5
                            },
                            "diameter": {
                                "meters": 1.5,
                                "feet": 4.9
                            }
                        },
                        "option_1": "composite fairing"
                    },
                    "reusable": False,
                    "engines": 1,
                    "fuel_amount_tons": 3.38,
                    "burn_time_sec": 378
                },
                "engines": {
                    "isp": {
                        "sea_level": 267,
                        "vacuum": 304
                    },
                    "thrust_sea_level": {
                        "kN": 420,
                        "lbf": 94000
                    },
                    "thrust_vacuum": {
                        "kN": 480,
                        "lbf": 110000
                    },
                    "number": 1,
                    "type": "merlin",
                    "version": "1C",
                    "layout": "single",
                    "engine_loss_max": 0,
                    "propellant_1": "liquid oxygen",
                    "propellant_2": "RP-1 kerosene",
                    "thrust_to_weight": 96
                },
                "landing_legs": {
                    "number": 0,
                    "material": None
                },
                "payload_weights": [
                    {
                        "id": "leo",
                        "name": "Low Earth Orbit",
                        "kg": 450,
                        "lb": 992
                    }
                ],
                "flickr_images": [
                    "https://imgur.com/DaCfMsj.jpg",
                    "https://imgur.com/azYafd8.jpg"
                ],
                "name": "Falcon 1",
                "type": "rocket",
                "active": False,
                "stages": 2,
                "boosters": 0,
                "cost_per_launch": 6700000,
                "success_rate_pct": 40,
                "first_flight": "2006-03-24",
                "country": "Republic of the Marshall Islands",
                "company": "SpaceX",
                "wikipedia": "https://en.wikipedia.org/wiki/Falcon_1",
                "description": "The Falcon 1 was an expendable launch system privately developed and manufactured by SpaceX during 2006-2009. On 28 September 2008, Falcon 1 became the first privately-developed liquid-fuel launch vehicle to go into orbit around the Earth.",
                "id": "5e9d0d95eda69955f709d1eb"
            }
        }