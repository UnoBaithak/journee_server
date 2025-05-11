from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class Accommodation(BaseModel):
    hotel_name: str
    check_in: datetime
    check_out: datetime
    metadata: Optional[Dict[str, Any]] = None