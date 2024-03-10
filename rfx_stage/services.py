from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from rfx_stage.schemas import RfxStageCreate, RfxStage


def create_rfx_stage(item_form_data: RfxStageCreate) -> RfxStage:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO rfx_stage (
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
        return RfxStage(
            rfx_stage_id=new_item[0],
            tenant_id=new_item[1],
            title=new_item[2],
            is_active=new_item[3],
            alias=new_item[4]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Validity Detail creation failed")


def get_all_rfx_stage(tenant_id: int) -> List[RfxStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM rfx_stage              
        WHERE tenant_id = %s;
        """

    cursor.execute(query,(tenant_id, ))
    query_all_items = cursor.fetchall()

    conn.close()
    if query_all_items:
        return [
            RfxStage(
                rfx_stage_id=row[0],
                tenant_id=row[1],
                title=row[2],
                is_active=row[3],
                alias=row[4]
            )
            for row in query_all_items
        ]
    else:
        None


def update_rfx_stage(rfx_stage_id: int,  item_form_data: RfxStageCreate) -> Optional[RfxStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE rfx_stage SET 
        title = %s,
        is_active = %s,
        alias = %s
    WHERE rfx_stage_id = %s RETURNING *;
    """

    values = (
        item_form_data.title,
        item_form_data.is_active,
        item_form_data.alias,
        rfx_stage_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return RfxStage(
            rfx_stage_id=updated_itemm[0],
            tenant_id=updated_itemm[1],
            title=updated_itemm[2],
            is_active=updated_itemm[3],
            alias=updated_itemm[4]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Validity update failed")


def delete_rfx_stage(rfx_stage_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM rfx_stage WHERE rfx_stage_id = %s RETURNING rfx_stage_id;"
    cursor.execute(query, (rfx_stage_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False

def delete_all_rfx_stage(tenant_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM rfx_stage WHERE tenant_id = %s RETURNING rfx_stage_id;"
    cursor.execute(query, (tenant_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False


def get_rfx_stage_by_id(rfx_stage_id: int) -> List[RfxStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT * FROM rfx_stage WHERE rfx_stage_id = %s;
    """

    cursor.execute(query, (rfx_stage_id,))
    get_all_items = cursor.fetchall()

    conn.close()

    if get_all_items:
        return [
            RfxStage (
                rfx_stage_id=row[0],
                tenant_id=row[1],
                title=row[2],
                is_active=row[3],
                alias=row[4]
            )
            for row in get_all_items
        ]
    else:
        return None


def get_rfx_stage_by_name(tenant_id: int, title : str) -> List[RfxStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT * FROM rfx_stage WHERE tenant_id = %s AND lower(title) = %s;
    """

    cursor.execute(query, (tenant_id, title.lower()))
    get_item = cursor.fetchall()

    conn.close()

    if get_item:
        return [
            RfxStage (
                rfx_stage_id=row[0],
                tenant_id=row[1],
                title=row[2],
                is_active=row[3],
                alias=row[4]
            )
            for row in get_item
        ]
    else:
        return None
    

def get_all_active_rfx_stage( tenant_id: int) -> List[RfxStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT * FROM rfx_stage WHERE tenant_id = %s AND is_active = %s;
    """

    cursor.execute(query, (tenant_id, True))
    all_records = cursor.fetchall()

    conn.close()
    if all_records:
        return [
            RfxStage (
                rfx_stage_id=row[0],
                tenant_id=row[1],
                title=row[2],
                is_active=row[3],
                alias=row[4]
            )
            for row in all_records
        ]
    else:
        return None
    

def get_all_rfx_stage_by_alias( tenant_id: int, alias: str) -> List[RfxStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT * FROM rfx_stage WHERE tenant_id = %s AND lower(alias) = %s;
    """

    cursor.execute(query, (tenant_id, alias.lower()))
    all_records = cursor.fetchall()

    conn.close()
    if all_records:
        return [
            RfxStage (
                rfx_stage_id=row[0],
                tenant_id=row[1],
                title=row[2],
                is_active=row[3],
                alias=row[4]
            )
            for row in all_records
        ]
    else:
        return None
