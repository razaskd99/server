from pydantic import BaseModel
from typing import Optional

class TemplateBase(BaseModel):
    name: str
    content: str

class TemplateCreate(TemplateBase):
    tenant_id: int
    template_category: str

class Template(TemplateBase):
    id: int
    tenant_id: int
    template_category: str

    class Config:
        orm_mode = True
