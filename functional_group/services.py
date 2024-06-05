from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from functional_group.schemas import FunctionalGroupCreate, FunctionalGroup


def create_functional_group(item_form_data: FunctionalGroupCreate) -> FunctionalGroup:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO functional_group (
        tenant_id,
        title,
        active,
        created_at
    ) VALUES (%s, %s, %s, %s) RETURNING *;
    """

    values = (
        item_form_data.tenant_id,
        item_form_data.title,
        item_form_data.active,
        item_form_data.created_at
    )

    cursor.execute(query, values)
    new_item = cursor.fetchone()

   
    conn.commit()
    conn.close()

    if new_item:
        return FunctionalGroup(
            id=new_item[0],
            tenant_id=new_item[1],
            title=new_item[2],
            active=new_item[3],
            created_at=new_item[4]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Validity Detail creation failed")


def get_all_functional_group(tenant_id: int) -> List[FunctionalGroup]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM functional_group              
        WHERE tenant_id = %s 
        ORDER BY created_at DESC;
        """

    cursor.execute(query,(tenant_id, ))
    query_all_items = cursor.fetchall()

    conn.close()
    if query_all_items:
        return [
            FunctionalGroup(
                id=row[0],
                tenant_id=row[1],
                title=row[2],
                active=row[3],
                created_at=row[4]
            )
            for row in query_all_items
        ]
    else:
        None


def update_functional_group(functional_group_id: int,  item_form_data: FunctionalGroupCreate) -> Optional[FunctionalGroup]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE functional_group SET 
        title = %s,
        active = %s
    WHERE id = %s RETURNING *;
    """

    values = (
        item_form_data.title,
        item_form_data.active,
        functional_group_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return FunctionalGroup(
            id=updated_itemm[0],
            tenant_id=updated_itemm[1],
            title=updated_itemm[2],
            active=updated_itemm[3],
            created_at=updated_itemm[4]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Validity update failed")


def delete_functional_group(functional_group_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM functional_group WHERE id = %s RETURNING id;"
    cursor.execute(query, (functional_group_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False
    
def delete_all_functional_group(tenant_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM functional_group WHERE tenant_id = %s RETURNING id;"
    cursor.execute(query, (tenant_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False


def get_functional_group_by_id(functional_group_id: int) -> Optional[FunctionalGroup]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM functional_group WHERE id = %s;"

    cursor.execute(query, (functional_group_id,))
    get_all_items = cursor.fetchone()

    conn.close()

    if get_all_items:
        return FunctionalGroup (
                id=get_all_items[0],
                tenant_id=get_all_items[1],
                title=get_all_items[2],
                active=get_all_items[3],
                created_at=get_all_items[4]
            )
    else:
        return None


