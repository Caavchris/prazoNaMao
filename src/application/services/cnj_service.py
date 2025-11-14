import httpx
from typing import Dict, Any, Optional
from application.core.settings import Settings

class CNJService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = f"{self.settings.cnj_base_url}/api/v1/comunicacao"
        self.client = httpx.AsyncClient(timeout=self.settings.cnj_timeout)
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    async def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Internal method to handle API requests"""
        try:
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"API request failed: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            raise Exception(f"Network error: {str(e)}")
    
    async def query_case_number(self, case_number: str) -> Dict[str, Any]:
        """Query by case number (numeroProcesso)"""
        params = {"numeroProcesso": case_number}
        return await self._make_request(params)
    
    async def query_lawyer_name(self, lawyer_name: str) -> Dict[str, Any]:
        """Query by lawyer name (nomeAdvogado)"""
        params = {"nomeAdvogado": lawyer_name}
        return await self._make_request(params)