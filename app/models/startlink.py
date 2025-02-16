from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class SpaceTrack(BaseModel):
    CCSDS_OMM_VERS: str
    COMMENT: str
    CREATION_DATE: str
    ORIGINATOR: str
    OBJECT_NAME: str
    OBJECT_ID: str
    CENTER_NAME: str
    REF_FRAME: str
    TIME_SYSTEM: str
    MEAN_ELEMENT_THEORY: str
    EPOCH: str
    MEAN_MOTION: float
    ECCENTRICITY: float
    INCLINATION: float
    RA_OF_ASC_NODE: float
    ARG_OF_PERICENTER: float
    MEAN_ANOMALY: float
    EPHEMERIS_TYPE: int
    CLASSIFICATION_TYPE: str
    NORAD_CAT_ID: int
    ELEMENT_SET_NO: int
    REV_AT_EPOCH: int
    BSTAR: float
    MEAN_MOTION_DOT: float
    MEAN_MOTION_DDOT: float
    SEMIMAJOR_AXIS: float
    PERIOD: float
    APOAPSIS: float
    PERIAPSIS: float
    OBJECT_TYPE: str
    RCS_SIZE: Optional[str] = None
    COUNTRY_CODE: Optional[str] = None
    LAUNCH_DATE: Optional[str] = None
    SITE: Optional[str] = None
    DECAY_DATE: Optional[str] = None
    DECAYED: int
    FILE: int
    GP_ID: int
    TLE_LINE0: str
    TLE_LINE1: str
    TLE_LINE2: str

class StarlinkSatellite(BaseModel):
    spaceTrack: SpaceTrack
    launch: Optional[str] = None
    version: Optional[str] = None
    height_km: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    velocity_kms: Optional[float] = None
    id: str

class StarlinkResponse(BaseModel):
    docs: List[StarlinkSatellite]
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
    offset: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "spaceTrack": {
                    "CCSDS_OMM_VERS": "2.0",
                    "COMMENT": "GENERATED VIA SPACE-TRACK.ORG API",
                    "CREATION_DATE": "2020-10-13T04:16:08",
                    "ORIGINATOR": "18 SPCS",
                    "OBJECT_NAME": "STARLINK-30",
                    "OBJECT_ID": "2019-029K",
                    "CENTER_NAME": "EARTH",
                    "REF_FRAME": "TEME",
                    "TIME_SYSTEM": "UTC",
                    "MEAN_ELEMENT_THEORY": "SGP4",
                    "EPOCH": "2020-10-13T02:56:59.566560",
                    "MEAN_MOTION": 16.43170483,
                    "ECCENTRICITY": 0.0003711,
                    "INCLINATION": 52.9708,
                    "RA_OF_ASC_NODE": 332.0356,
                    "ARG_OF_PERICENTER": 120.7278,
                    "MEAN_ANOMALY": 242.0157,
                    "EPHEMERIS_TYPE": 0,
                    "CLASSIFICATION_TYPE": "U",
                    "NORAD_CAT_ID": 44244,
                    "ELEMENT_SET_NO": 999,
                    "REV_AT_EPOCH": 7775,
                    "BSTAR": 0.0022139,
                    "MEAN_MOTION_DOT": 0.47180237,
                    "MEAN_MOTION_DDOT": 0.000012426,
                    "SEMIMAJOR_AXIS": 6535.519,
                    "PERIOD": 87.635,
                    "APOAPSIS": 159.809,
                    "PERIAPSIS": 154.958,
                    "OBJECT_TYPE": "PAYLOAD",
                    "RCS_SIZE": "LARGE",
                    "COUNTRY_CODE": "US",
                    "LAUNCH_DATE": "2019-05-24",
                    "SITE": "AFETR",
                    "DECAY_DATE": "2020-10-13",
                    "DECAYED": 1,
                    "FILE": 2850561,
                    "GP_ID": 163365918,
                    "TLE_LINE0": "0 STARLINK-30",
                    "TLE_LINE1": "1 44244U 19029K   20287.12291165  .47180237  12426-4  22139-2 0  9995",
                    "TLE_LINE2": "2 44244  52.9708 332.0356 0003711 120.7278 242.0157 16.43170483 77756"
                },
                "launch": "5eb87d30ffd86e000604b378",
                "version": "v0.9",
                "height_km": None,
                "latitude": None,
                "longitude": None,
                "velocity_kms": None,
                "id": "5eed770f096e59000698560d"
            }
        }