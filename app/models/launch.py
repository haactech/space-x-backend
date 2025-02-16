from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class LaunchLinks(BaseModel):
    patch: Optional[Dict[str, str]] = Field(None, description="Mission patch links")
    reddit: Optional[Dict[str, Optional[str]]] = Field(None, description="Reddit links")
    flickr: Optional[Dict[str, List[str]]] = Field(None, description="Flickr image links")
    presskit: Optional[str] = None
    webcast: Optional[str] = None
    youtube_id: Optional[str] = None
    article: Optional[str] = None
    wikipedia: Optional[str] = None

class LaunchFailure(BaseModel):
    time: Optional[int] = None
    altitude: Optional[int] = None
    reason: Optional[str] = None

class Core(BaseModel):
    core: Optional[str] = None
    flight: Optional[int] = None
    gridfins: Optional[bool] = None
    legs: Optional[bool] = None
    reused: Optional[bool] = None
    landing_attempt: Optional[bool] = None
    landing_success: Optional[bool] = None
    landing_type: Optional[str] = None
    landpad: Optional[str] = None

class Fairings(BaseModel):
    reused: Optional[bool] = None
    recovery_attempt: Optional[bool] = None
    recovered: Optional[bool] = None
    ships: List[str] = Field(default_factory=list)

class Launch(BaseModel):
    fairings: Optional[Fairings] = None
    links: LaunchLinks
    static_fire_date_utc: Optional[str] = None
    static_fire_date_unix: Optional[int] = None
    net: Optional[bool] = None
    window: Optional[int] = None
    rocket: str = Field(..., description="Rocket ID reference")
    success: Optional[bool] = None
    failures: List[LaunchFailure] = Field(default_factory=list)
    details: Optional[str] = None
    crew: List[str] = Field(default_factory=list)
    ships: List[str] = Field(default_factory=list)
    capsules: List[str] = Field(default_factory=list)
    payloads: List[str] = Field(default_factory=list)
    launchpad: str
    flight_number: int
    name: str
    date_utc: str
    date_unix: int
    date_local: str
    date_precision: str
    upcoming: bool
    cores: List[Core]
    auto_update: Optional[bool] = None
    tbd: Optional[bool] = None
    launch_library_id: Optional[str] = None
    id: str

class LaunchResponse(BaseModel):
    docs: List[Launch]
    totalDocs: int
    offset: int
    limit: int
    totalPages: int
    page: int
    pagingCounter: int
    hasPrevPage: bool
    hasNextPage: bool
    prevPage: Optional[int] = None
    nextPage: Optional[int] = None

class Config:
        schema_extra = {
            "example": {
                "fairings": {
                    "reused": False,
                    "recovery_attempt": False,
                    "recovered": False,
                    "ships": []
                },
                "links": {
                    "patch": {
                        "small": "https://images2.imgbox.com/94/f2/NN6Ph45r_o.png",
                        "large": "https://images2.imgbox.com/5b/02/QcxHUb5V_o.png"
                    },
                    "reddit": {
                        "campaign": None,
                        "launch": None,
                        "media": None,
                        "recovery": None
                    },
                    "flickr": {
                        "small": [],
                        "original": []
                    },
                    "presskit": None,
                    "webcast": "https://www.youtube.com/watch?v=0a_00nJ_Y88",
                    "youtube_id": "0a_00nJ_Y88",
                    "article": "https://www.space.com/2196-spacex-inaugural-falcon-1-rocket-lost-launch.html",
                    "wikipedia": "https://en.wikipedia.org/wiki/DemoSat"
                },
                "static_fire_date_utc": "2006-03-17T00:00:00.000Z",
                "static_fire_date_unix": 1142553600,
                "net": False,
                "window": 0,
                "rocket": "5e9d0d95eda69955f709d1eb",
                "success": False,
                "failures": [
                    {
                        "time": 33,
                        "altitude": None,
                        "reason": "merlin engine failure"
                    }
                ],
                "details": "Engine failure at 33 seconds and loss of vehicle",
                "crew": [],
                "ships": [],
                "capsules": [],
                "payloads": ["5eb0e4b5b6c3bb0006eeb1e1"],
                "launchpad": "5e9e4502f5090995de566f86",
                "flight_number": 1,
                "name": "FalconSat",
                "date_utc": "2006-03-24T22:30:00.000Z",
                "date_unix": 1143239400,
                "date_local": "2006-03-25T10:30:00+12:00",
                "date_precision": "hour",
                "upcoming": False,
                "cores": [
                    {
                        "core": "5e9e289df35918033d3b2623",
                        "flight": 1,
                        "gridfins": False,
                        "legs": False,
                        "reused": False,
                        "landing_attempt": False,
                        "landing_success": None,
                        "landing_type": None,
                        "landpad": None
                    }
                ],
                "auto_update": True,
                "tbd": False,
                "launch_library_id": None,
                "id": "5eb87cd9ffd86e000604b32a"
            }
        }