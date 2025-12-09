from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class EmissionsQuery(BaseModel):
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    sector: Optional[str] = None
    region: Optional[str] = None

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    web_fetch: bool = False
    filters: Optional[Dict[str, Any]] = None
