from typing import Optional, List
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import DesignationCreate, Designation

def create_designation(designation_data: DesignationCreate) -> Designation:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO designation (tenant_id, title, type, description)
    VALUES (%s, %s, %s, %s)
    RETURNING *;
    """

    values = (designation_data.tenant_id, designation_data.title, designation_data.type, designation_data.description)

    cursor.execute(query, values)
    new_designation = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_designation:
        return Designation(
            designation_id=new_designation[0],
            tenant_id=new_designation[1],
            title=new_designation[2],
            type=new_designation[3],
            description=new_designation[4]
        )
    else:
        raise HTTPException(status_code=404, detail="Designation creation failed")

def get_all_designations(tenant_id: int) -> List[Designation]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM designation WHERE tenant_id = %s;"
    cursor.execute(query,(tenant_id, ))
    designations = cursor.fetchall()

    conn.close()

    return [
        Designation(
            designation_id=row[0],
            tenant_id=row[1],
            title=row[2],
            type=row[3],
            description=row[4]
        )
        for row in designations
    ]

def update_designation(designation_id: int, designation_data: DesignationCreate) -> Designation:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE designation
    SET title = %s, type = %s, description = %s
    WHERE designation_id = %s
    RETURNING *;
    """

    values = (designation_data.title, designation_data.type, designation_data.description, designation_id)

    cursor.execute(query, values)
    updated_designation = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_designation:
        return Designation(
            designation_id=updated_designation[0],
            tenant_id=updated_designation[1],
            title=updated_designation[2],
            type=updated_designation[3],
            description=updated_designation[4]
        )
    else:
        raise HTTPException(status_code=404, detail="Designation update failed")

def delete_designation(designation_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM designation WHERE designation_id = %s RETURNING designation_id;"
    cursor.execute(query, (designation_id,))
    deleted_designation = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_designation:
        return True
    else:
        return False

def delete_all_designations(designation_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT delete_designation_disable_FK(%s);"
    cursor.execute(query, (designation_id,))
    deleted_designation = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_designation:
        return True
    else:
        return False



def get_designation_by_name(title: str) -> Optional[Designation]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM designation WHERE lower(title) = %s;"
    cursor.execute(query, (title.lower(),))
    designation = cursor.fetchone()

    conn.close()

    if designation:
        return Designation(
            designation_id=designation[0],
            tenant_id=designation[1],
            title=designation[2],
            type=designation[3],
            description=designation[4]
        )
    else:
        return None

def get_designation_by_id(designation_id: int) -> Optional[Designation]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM designation WHERE designation_id = %s;"
    cursor.execute(query, (designation_id,))
    designation = cursor.fetchone()

    conn.close()

    if designation:
        return Designation(
            designation_id=designation[0],
            tenant_id=designation[1],
            title=designation[2],
            type=designation[3],
            description=designation[4]
        )
    else:
        return None
