from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from application.services.cnj_service import CNJService
from application.core.settings import get_settings, Settings

router = APIRouter()

def get_cnj_service(settings: Settings = Depends(get_settings)) -> CNJService:
    """Dependency injection for CNJService"""
    return CNJService(settings=settings)

@router.get("/case-number", response_model=Dict[str, Any])
async def get_case_by_number(
    case_number: str,
    service: CNJService = Depends(get_cnj_service)
) -> Dict[str, Any]:
    """
    Query case information by case number (numeroProcesso).
    
    - **case_number**: The case number to search for
    """
    try:
        result = await service.query_case_number(case_number)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await service.close()

@router.get("/lawyer-name", response_model=Dict[str, Any])
async def get_case_by_lawyer(
    lawyer_name: str,
    service: CNJService = Depends(get_cnj_service)
) -> Dict[str, Any]:
    """
    Query case information by lawyer name (nomeAdvogado).
    
    - **lawyer_name**: The lawyer's name to search for
    """
    try:
        result = await service.query_lawyer_name(lawyer_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await service.close()