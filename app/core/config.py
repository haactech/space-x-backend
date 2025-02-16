from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Config
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SpaceX Dashboard API"
    
    SPACEX_API_URL: str = "https://api.spacexdata.com/v4"
    
    # AWS Config
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: Optional[str] = None
    
    # Redis Config
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: int = 6379
    
    class Config:
        env_file = ".env"

settings = Settings()