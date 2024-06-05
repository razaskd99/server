from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from persona.schemas import PersonaCreate, Persona


def create_persona(item_form_data: PersonaCreate) -> Persona:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO persona (
        tenant_id,
        persona_role,
        description,
        is_active,
        created_on
    ) VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        item_form_data.tenant_id,
        item_form_data.persona_role,
        item_form_data.description,
        item_form_data.is_active,
        item_form_data.created_on
    )

    cursor.execute(query, values)
    new_item = cursor.fetchone()

   
    conn.commit()
    conn.close()

    if new_item:
        return Persona(
            persona_id=new_item[0],
            tenant_id=new_item[1],
            persona_role=new_item[2],
            description=new_item[3],
            is_active=new_item[4],
            created_on=new_item[5]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Validity Detail creation failed")


def get_all_persona(tenant_id: int) -> List[Persona]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM persona              
        WHERE tenant_id = %s ;
        """

    cursor.execute(query,(tenant_id, ))
    query_all_items = cursor.fetchall()

    conn.close()
    if query_all_items:
        return [
            Persona(
                persona_id=row[0],
                tenant_id=row[1],
                persona_role=row[2],
                description=row[3],
                is_active=row[4],
                created_on=row[5]
            )
            for row in query_all_items
        ]
    else:
        None


def update_persona(persona_id: int,  item_form_data: PersonaCreate) -> Optional[Persona]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE persona SET 
        persona_role = %s,
        description = %s,
        is_active = %s
    WHERE persona_id = %s RETURNING *;
    """

    values = (
        item_form_data.persona_role,
        item_form_data.description,
        item_form_data.is_active,
        persona_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return Persona(
            persona_id=updated_itemm[0],
            tenant_id=updated_itemm[1],
            persona_role=updated_itemm[2],
            description=updated_itemm[3],
            is_active=updated_itemm[4],
            created_on=updated_itemm[5]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Validity update failed")


def delete_persona(persona_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM persona WHERE persona_id = %s RETURNING persona_id;"
    cursor.execute(query, (persona_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False
    
def delete_all_persona(tenant_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM persona WHERE tenant_id = %s RETURNING persona_id;"
    cursor.execute(query, (tenant_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False


def get_persona_by_id(persona_id: int) -> Optional[Persona]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM persona WHERE persona_id = %s ;"

    cursor.execute(query, (persona_id,))
    get_one_item = cursor.fetchone()

    conn.close()

    if get_one_item:
        return Persona (
                persona_id=get_one_item[0],
                tenant_id=get_one_item[1],
                persona_role=get_one_item[2],
                description=get_one_item[3],
                is_active=get_one_item[4],
                created_on=get_one_item[5]
            )
    else:
        return None


def get_persona_by_name(title : str, tenant_id: int) -> Optional[Persona]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM persona WHERE lower(title) = %s AND tenant_id = %s RETURNING *;"

    cursor.execute(query, (title.lower(), tenant_id))
    get_item = cursor.fetchone()

    conn.close()

    if get_item:
        return Persona(
                persona_id=get_item[0],
                tenant_id=get_item[1],
                rfx_id=get_item[2],
                title=get_item[3],
                is_active=get_item[4]
            )
    else:
        return None
    

