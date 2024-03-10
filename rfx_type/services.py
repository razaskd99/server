from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from rfx_type.schemas import RfxTypeCreate, RfxType


def create_rfx_type(item_form_data: RfxTypeCreate) -> RfxType:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO rfx_type (
        tenant_id,
        title,
        is_active,
        alias
    ) VALUES (%s, %s, %s, %s) RETURNING *;
    """

    values = (
        item_form_data.tenant_id,
        item_form_data.title,
        item_form_data.is_active,
        item_form_data.alias

    )

    cursor.execute(query, values)
    new_item = cursor.fetchone()

   
    conn.commit()
    conn.close()

    if new_item:
        return RfxType(
            rfx_type_id=new_item[0],
            tenant_id=new_item[1],
            title=new_item[2],
            is_active=new_item[3],
            alias=new_item[4]
        )
    else:
        raise HTTPException(status_code=404, detail="RFx Type Detail creation failed")


def get_all_rfx_type(tenant_id: int) -> List[RfxType]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM rfx_type              
        WHERE tenant_id = %s ;
        """

    cursor.execute(query,(tenant_id, ))
    query_all_items = cursor.fetchall()

    conn.close()
    if query_all_items:
        return [
            RfxType(
                rfx_type_id=row[0],
                tenant_id=row[1],
                title=row[2],
                is_active=row[3],
                alias=row[4]
            )
            for row in query_all_items
        ]
    else:
        None


def update_rfx_type(rfx_type_id: int,  item_form_data: RfxTypeCreate) -> Optional[RfxType]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE rfx_type SET 
        title = %s,
        is_active = %s,
        alias = %s
    WHERE rfx_type_id = %s RETURNING *;
    """

    values = (
        item_form_data.title,
        item_form_data.is_active,
        item_form_data.alias,
        rfx_type_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return RfxType(
            rfx_type_id=updated_itemm[0],
            tenant_id=updated_itemm[1],
            title=updated_itemm[2],
            is_active=updated_itemm[3],
            alias=updated_itemm[4]
        )
    else:
        raise HTTPException(status_code=404, detail="RFx Type update failed")


def delete_rfx_type(rfx_type_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM rfx_type WHERE rfx_type_id = %s RETURNING rfx_type_id;"
    cursor.execute(query, (rfx_type_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False

def delete_all_rfx_type(tenant_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM rfx_type WHERE tenant_id = %s RETURNING rfx_type_id;"
    cursor.execute(query, (tenant_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False


def get_rfx_type_by_id(rfx_type_id: int) -> Optional[RfxType]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM rfx_type WHERE rfx_type_id = %s ;"

    cursor.execute(query, (rfx_type_id,))
    get_all_items = cursor.fetchone()

    conn.close()

    if get_all_items:
        return RfxType (
                rfx_type_id=get_all_items[0],
                tenant_id=get_all_items[1],
                title=get_all_items[2],
                is_active=get_all_items[3],
                alias=get_all_items[4]
            )
    else:
        return None


def get_rfx_type_by_name(title : str, tenant_id: int) -> Optional[RfxType]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM rfx_type WHERE lower(title) = %s AND tenant_id = %s RETURNING *;"

    cursor.execute(query, (title.lower(), tenant_id))
    get_item = cursor.fetchone()

    conn.close()

    if get_item:
        return RfxType(
                rfx_type_id=get_item[0],
                tenant_id=get_item[1],
                title=get_item[2],
                is_active=get_item[3],
                alias=get_item[4]
            )
    else:
        return None
    

def get_all_active_rfx_type( tenant_id: int) -> List[RfxType]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM rfx_type WHERE is_active = %s AND tenant_id = %s;"

    cursor.execute(query, (True, tenant_id,))
    all_records = cursor.fetchall()

    conn.close()
    if all_records:
        return [
            RfxType (
                rfx_type_id=row[0],
                tenant_id=row[1],
                title=row[2],
                is_active=row[3],
                alias=row[4]
            )
            for row in all_records
        ]
    else:
        return None
    
def get_all_rfx_type_by_alias( tenant_id: int, alias: str) -> List[RfxType]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM rfx_type WHERE tenant_id = %s AND lower(alias) = %s;"

    cursor.execute(query, (tenant_id, alias))
    all_records = cursor.fetchall()

    conn.close()
    if all_records:
        return [
            RfxType (
                rfx_type_id=row[0],
                tenant_id=row[1],
                title=row[2],
                is_active=row[3],
                alias=row[4]
            )
            for row in all_records
        ]
    else:
        return None
