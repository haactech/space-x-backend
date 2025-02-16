from httpx import AsyncClient
from typing import Optional, List, Dict, Any 
from app.core.config import settings
from app.core.exceptions import SpaceXAPIException 

class SpaceXClient:
    def __init__(self):
        self.base_url = settings.SPACEX_API_URL
        self.client = AsyncClient(base_url=self.base_url)

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Any:
        try:
            response = await self.client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise SpaceXAPIException(f"Error making request to SpaceX API: {e}")
    #Rockets
    async def get_rockets(self) -> List[Dict]:
        """Get all rockets""" 
        return await self._make_request("GET", "/rockets")

    async def get_rocket(self, rocket_id: str) -> Dict:
        """Get a specific rocket by ID"""
        return await self._make_request("GET", f"/rockets/{rocket_id}")
    #Launches 
    async def get_launches(self, query: Optional[Dict] = None, options: Optional[Dict] = None) -> List[Dict]:
        """
        Get launches with optional query parameters and options
        Returns the 'docs' array from the paginated response
        """
        payload = {
            "query": query or {},
            "options": options or {}
        }
        response = await self._make_request("POST", "/launches/query", json=payload)
        return response.get("docs", [])

    async def get_launch(self, launch_id: str) -> Dict:
        """Get a specific launch by ID"""
        return await self._make_request("GET", f"/launches/{launch_id}") 

    async def get_upcoming_launches(self) -> List[Dict]:
        """Get upcoming launches"""
        return await self._make_request("GET", "/launches/upcoming")

    #Starlink endpoints
    async def get_starlink_satellites(self, query: Optional[Dict] = None, options: Optional[Dict] = None) -> Dict:
        """
        Get Starlink satellites with optional query parameters and options
        Returns the complete paginated response
        """
        payload = {
            "query": query or {},
            "options": options or {
                "limit": 100,
                "page": 1
            }
        }
        return await self._make_request("POST", "/starlink/query", json=payload)


    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
