from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class OppComittedForSalesBudgetCreate(BaseModel):
    tenant_id: int
    title: Optional[str]
    active: Optional[bool] = True
    created_at : datetime

class OppComittedForSalesBudget(OppComittedForSalesBudgetCreate):
    opp_committed_for_sales_budget_id : int
