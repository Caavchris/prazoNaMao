from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, Any, List, Optional
from application.services.cnj_service import CNJService
from application.core.settings import get_settings, Settings
from application.services.deadline import annotate_deadlines

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
        # Normalize response to a consistent structure for frontend
        if isinstance(result, list):
            items = result
        elif isinstance(result, dict) and 'items' in result:
            items = result['items']
        elif isinstance(result, dict):
            # try to find a list value inside dict
            items = next((v for v in result.values() if isinstance(v, list)), [])
        else:
            items = []
        return {"items": items, "total": len(items), "page": 1, "page_size": len(items)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await service.close()

@router.get("/lawyer-name/deadlines", response_model=Dict[str, Any])
async def get_case_by_lawyer_with_deadlines(
    lawyer_name: str,
    status: Optional[str] = Query(None, description="Filter by deadline status: approaching, expired, ok"),
    page: int = 1,
    page_size: int = 25,
    threshold_days: Optional[int] = None,
    service: CNJService = Depends(get_cnj_service),
    settings: Settings = Depends(get_settings)
) -> Dict[str, Any]:
    """
    Query cases by lawyer and annotate deadlines.

    - **status**: optional filter (`approaching`, `expired`, `ok`)
    - **threshold_days**: override the configured threshold for `approaching`
    """
    try:
        result = await service.query_lawyer_name(lawyer_name)
        if isinstance(result, list):
            items = result
        elif isinstance(result, dict) and 'items' in result:
            items = result['items']
        elif isinstance(result, dict):
            items = next((v for v in result.values() if isinstance(v, list)), [])
        else:
            items = []

        # Optionally override threshold in settings copy
        if threshold_days is not None:
            # shallow copy of settings-like object for annotate_deadlines
            class S:
                pass
            s = S()
            s.deadlines = settings.deadlines
            s.deadlines_default = settings.deadlines_default
            s.deadlines_threshold = threshold_days
        else:
            s = settings

        annotated = annotate_deadlines(items, s)

        if status:
            # support comma-separated statuses, e.g., status=expired,approaching
            statuses = [st.strip().lower() for st in status.split(',') if st.strip()]
            annotated = [it for it in annotated if (it.get('deadline_status') or '').lower() in statuses]

        # simple pagination
        total = len(annotated)
        start = (page - 1) * page_size
        end = start + page_size
        paged = annotated[start:end]

        return {"items": paged, "total": total, "page": page, "page_size": page_size} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await service.close()