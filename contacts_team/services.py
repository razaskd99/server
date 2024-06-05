from typing import Optional, List
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import ContactsTeamCreate, ContactsTeam, GetContactsTeam


def create_contacts_team(team_data: ContactsTeamCreate) -> ContactsTeam:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO contacts_team (tenant_id, primary_contacts_id, team_title, team_role, status, created_at)
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        team_data.tenant_id,
        team_data.primary_contacts_id,
        team_data.team_title,
        team_data.team_role,
        team_data.status,
        team_data.created_at

    )

    cursor.execute(query, values)
    new_team = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_team:
        return ContactsTeam(
            contacts_team_id=new_team[0],
            tenant_id=new_team[1],
            primary_contacts_id=new_team[2],
            team_title=new_team[3],
            team_role=new_team[4],
            status=new_team[5],
            created_at=new_team[6]
        
        )
    else:
        raise HTTPException(status_code=404, detail="Contacts Team creation failed")


def get_all_contacts_team(tenant_id: int, searchTerm: str) -> List[GetContactsTeam]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if searchTerm:
        searchTerm = '%' + searchTerm.lower() + '%'
        query = """
            SELECT c.*,
                p.first_name, p.last_name, p.email, p.contact_number, p.profile_image, p.job_title
                FROM contacts_team c
                LEFT JOIN users p ON p.user_id=c.primary_contacts_id
        WHERE c.tenant_id = %s AND lower(c.team_title) LIKE %s
        ORDER BY created_at DESC;
        """
        cursor.execute(query,(tenant_id, searchTerm.lower()))
        teams = cursor.fetchall()
    else:
        query = """
            SELECT c.*,
                p.first_name, p.last_name, p.email, p.contact_number, p.profile_image, p.job_title
                FROM contacts_team c
                LEFT JOIN users p ON p.user_id=c.primary_contacts_id
        WHERE c.tenant_id = %s
        ORDER BY created_at DESC;
        """
        cursor.execute(query,(tenant_id,))
        teams = cursor.fetchall()
        
    conn.close()
    
    return [
        GetContactsTeam(
            contacts_team_id=row[0],
            tenant_id=row[1],
            primary_contacts_id=row[2],
            team_title=row[3],
            team_role=row[4],
            status=row[5],
            created_at=row[6],
            first_name=row[7],
            last_name=row[8],
            email=row[9],
            contact_number=row[10],
            profile_image=row[11],
            job_title=row[12]
        )
        for row in teams
    ]


def update_contact_team(contacts_team_id: int, team_data: ContactsTeamCreate) -> ContactsTeam:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE contacts_team SET 
        team_title = %s,
        team_role = %s,
        status = %s
    WHERE contacts_team_id = %s RETURNING *;
    """

    values = (
        team_data.team_title,
        team_data.team_role,
        team_data.status,
        contacts_team_id
    )

    cursor.execute(query, values)
    updated_team = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_team:
        return ContactsTeam(
            contacts_team_id=updated_team[0],
            tenant_id=updated_team[1],
            primary_contacts_id=updated_team[2],
            team_title=updated_team[3],
            team_role=updated_team[4],
            status=updated_team[5],
            created_at=updated_team[6]
        
        )
    else:
        raise HTTPException(status_code=404, detail="Contacts Team update failed")


def delete_contact_team(contacts_team_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM contacts_team WHERE contacts_team_id = %s RETURNING contacts_team_id;"
    cursor.execute(query, (contacts_team_id,))
    deleted_team = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_team:
        return True
    else:
        return False


def get_contact_team_by_id(contacts_team_id: int) -> Optional[GetContactsTeam]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT c.*,
            p.first_name, p.last_name, p.email, p.contact_number, p.profile_image, p.job_title
            FROM contacts_team c
            LEFT JOIN users p ON p.user_id=c.primary_contacts_id
        WHERE c.contacts_team_id = %s;
        """
    cursor.execute(query, (contacts_team_id,))
    updated_team = cursor.fetchone()

    conn.close()

    if updated_team:
        return GetContactsTeam(
            contacts_team_id=updated_team[0],
            tenant_id=updated_team[1],
            primary_contacts_id=updated_team[2],
            team_title=updated_team[3],
            team_role=updated_team[4],
            status=updated_team[5],
            created_at=updated_team[6],
            first_name=updated_team[7],
            last_name=updated_team[8],
            email=updated_team[9],
            contact_number=updated_team[10],
            profile_image=updated_team[11],
            job_title=updated_team[12]
        
        )
    else:
        return None

def get_contact_team_by_title(tenant_id: int, team_title: str) -> List[GetContactsTeam]:
    conn = get_db_connection()
    cursor = conn.cursor()
    team_title = team_title.replace("-", " ")

    query = """
        SELECT c.*,
            p.first_name, p.last_name, p.email, p.contact_number, p.profile_image, p.job_title
            FROM contacts_team c
            LEFT JOIN users p ON p.user_id=c.primary_contacts_id
        WHERE c.tenant_id = %s AND lower(c.team_title) = %s;
        """
    cursor.execute(query, (tenant_id, team_title.lower(),))
    get_team = cursor.fetchall()

    conn.close()

    if get_team:
        return [GetContactsTeam(
                contacts_team_id=row[0],
                tenant_id=row[1],
                primary_contacts_id=row[2],
                team_title=row[3],
                team_role=row[4],
                status=row[5],
                created_at=row[6],
                first_name=row[7],
                last_name=row[8],
                email=row[9],
                contact_number=row[10],
                profile_image=row[11],
                job_title=row[12]            
            )
            for row in get_team
        ]
    else:
        return None


