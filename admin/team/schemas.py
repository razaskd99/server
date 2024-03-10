from pydantic import BaseModel
from typing import Optional

class TeamCreate(BaseModel):
    tenant_id: int
    team_title: str
    team_role: str
    role_level: int

class Team(TeamCreate):
    team_id: int
