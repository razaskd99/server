from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class SalesPursuitProgressCreate(BaseModel):
    tenant_id: int
    title: Optional[str]
    active: Optional[bool] = True
    created_at : datetime

class SalesPursuitProgress(SalesPursuitProgressCreate):
    sales_pursuit_progress_id : int
