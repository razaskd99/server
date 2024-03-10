from typing import Optional, List
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import TeamCreate, Team


def create_team(team_data: TeamCreate) -> Team:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO team (tenant_id, team_title, team_role, role_level)
    VALUES (%s, %s, %s, %s) RETURNING *;
    """

    values = (team_data.tenant_id, team_data.team_title, team_data.team_role, team_data.role_level)

    cursor.execute(query, values)
    new_team = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_team:
        return Team(team_id=new_team[0], **team_data.dict())
    else:
        raise HTTPException(status_code=404, detail="Team creation failed")


def get_all_teams(tenant_id: int) -> List[Team]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM team WHERE tenant_id = %s;"
    cursor.execute(query,(tenant_id,))
    teams = cursor.fetchall()
  
    conn.close()
    
    return [Team(
        team_id=row[0],
        tenant_id=row[1],
        team_title=row[2],
        team_role=row[3],
        role_level=0 if row[4] is None else row[4]
    )
    for row in teams
    ]


def update_team(team_id: int, team_data: TeamCreate) -> Team:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE team SET 
        team_title = %s,
        team_role = %s,
        role_level = %s
    WHERE team_id = %s RETURNING *;
    """

    values = (
        team_data.team_title,
        team_data.team_role,
        team_data.role_level,
        team_id
    )

    cursor.execute(query, values)
    updated_team = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_team:
        return Team(
            team_id=updated_team[0],
            tenant_id=updated_team[1],
            team_title=updated_team[2],
            team_role=updated_team[3],
            role_level=updated_team[4],  
        )
    else:
        raise HTTPException(status_code=404, detail="Team update failed")


def delete_team(team_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM team WHERE team_id = %s RETURNING team_id;"
    cursor.execute(query, (team_id,))
    deleted_team = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_team:
        return True
    else:
        return False


def get_team_by_id(team_id: int) -> Optional[Team]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM team WHERE team_id = %s;"
    cursor.execute(query, (team_id,))
    team = cursor.fetchone()

    conn.close()

    if team:
        return Team(team_id=team[0], tenant_id=team[1], team_title=team[2], team_role=team[3], role_level=team[4])
    else:
        return None


def get_team_by_title(team_title: str) -> Optional[Team]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM team WHERE lower(team_title) = %s;"
    cursor.execute(query, (team_title.lower(),))
    team = cursor.fetchone()

    conn.close()

    if team:
        return Team(team_id=team[0], tenant_id=team[1], team_title=team[2], team_role=team[3], role_level=team[4])
    else:
        return None


def delete_all_team_record(team_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT delete_team_disable_FK(%s);"
    cursor.execute(query, (team_id,))
           
    
    delete_team = cursor.fetchone()
    

    conn.commit()
    conn.close()
                
        
    if delete_team:
        return True
    else:
        return False
