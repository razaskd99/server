from typing import Optional, List
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import RfxClarificationMetaCreate, RfxClarificationMeta

# Function to create RfxClarificationMeta
def create_rf_clarification_meta(rfx_clarification_meta_data: RfxClarificationMetaCreate) -> Optional[RfxClarificationMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO rfx_clarification_meta (
        rfx_id,
        rfx_clarification_id,
        rfx_clarification_post_id,
        meta_key,
        meta_id
    ) VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        rfx_clarification_meta_data.rfx_id,
        rfx_clarification_meta_data.rfx_clarification_id,
        rfx_clarification_meta_data.rfx_clarification_post_id,
        rfx_clarification_meta_data.meta_key,
        rfx_clarification_meta_data.meta_id,
    )

    cursor.execute(query, values)
    new_rf_clarification_meta = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_rf_clarification_meta:
        return RfxClarificationMeta(
            rfx_clarification_meta_id=new_rf_clarification_meta[0],
            **rfx_clarification_meta_data.dict(),
        )
    else:
        raise HTTPException(status_code=404, detail="Rfx Clarification Meta creation failed")


# Function to get all RfxClarificationMeta
def get_all_rf_clarification_meta(rfx_clarification_id: int) -> List[RfxClarificationMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM rfx_clarification_meta  WHERE rfx_clarification_id = %s;"
    cursor.execute(query, (rfx_clarification_id,))
    rf_clarification_metas = cursor.fetchall()

    conn.close()

    return [
        RfxClarificationMeta(
            rfx_clarification_meta_id=row[0],
            rfx_id=row[1],
            rfx_clarification_id=row[2],
            rfx_clarification_post_id=row[3],
            meta_key=row[4],
            meta_id=row[5],
        )
        for row in rf_clarification_metas
    ]


# Function to update RfxClarificationMeta
def update_rf_clarification_meta(rfx_clarification_meta_id: int, rfx_clarification_meta_data: RfxClarificationMetaCreate) -> Optional[RfxClarificationMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE rfx_clarification_meta SET 
        rfx_id = %s,
        rfx_clarification_id = %s,
        rfx_clarification_post_id = %s,
        meta_key = %s,
        meta_id = %s
    WHERE rfx_clarification_meta_id = %s RETURNING *;
    """

    values = (
        rfx_clarification_meta_data.rfx_id,
        rfx_clarification_meta_data.rfx_clarification_id,
        rfx_clarification_meta_data.rfx_clarification_post_id,
        rfx_clarification_meta_data.meta_key,
        rfx_clarification_meta_data.meta_id,
        rfx_clarification_meta_id
    )

    cursor.execute(query, values)
    updated_rf_clarification_meta = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_rf_clarification_meta:
        return RfxClarificationMeta(
            rfx_clarification_meta_id=updated_rf_clarification_meta[0],
            **rfx_clarification_meta_data.dict(),
        )
    else:
        raise HTTPException(status_code=404, detail="Rfx Clarification Meta update failed")

# Function to delete RfxClarificationMeta
def delete_rf_clarification_meta(rfx_clarification_meta_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM rfx_clarification_meta WHERE rfx_clarification_meta_id = %s RETURNING rfx_clarification_meta_id;"
    cursor.execute(query, (rfx_clarification_meta_id,))
    deleted_rf_clarification_meta = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_rf_clarification_meta:
        return True
    else:
        return False

# Function to get RfxClarificationMeta by ID
def get_rf_clarification_meta_by_id(rfx_clarification_meta_id: int) -> Optional[RfxClarificationMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM rfx_clarification_meta WHERE rfx_clarification_meta_id = %s;"
    cursor.execute(query, (rfx_clarification_meta_id,))
    rf_clarification_meta = cursor.fetchone()

    conn.close()

    if rf_clarification_meta:
        return RfxClarificationMeta(
            rfx_clarification_meta_id=rf_clarification_meta[0],
            rfx_id=rf_clarification_meta[1],
            rfx_clarification_id=rf_clarification_meta[2],
            rfx_clarification_post_id=rf_clarification_meta[3],
            meta_key=rf_clarification_meta[4],
            meta_id=rf_clarification_meta[5],
        )
    else:
        return None

# Function to get RfxClarificationMeta by rfx_clarification_post_id
def get_rf_clarification_meta_by_post_id(rfx_clarification_post_id: int) -> List[RfxClarificationMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM rfx_clarification_meta WHERE rfx_clarification_post_id = %s;"
    cursor.execute(query, (rfx_clarification_post_id,))
    rf_clarification_metas = cursor.fetchall()

    conn.close()

    return[ 
        RfxClarificationMeta(
            rfx_clarification_meta_id=rf_clarification_meta[0],
            rfx_id=rf_clarification_meta[1],
            rfx_clarification_id=rf_clarification_meta[2],
            rfx_clarification_post_id=rf_clarification_meta[3],
            meta_key=rf_clarification_meta[4],
            meta_id=rf_clarification_meta[5]
        ) 
        for rf_clarification_meta in rf_clarification_metas
    ]
   

# Function to get RfxClarificationMeta by Meta Key
def get_rf_clarification_meta_by_key(rfx_clarification_id: int, meta_key: str) -> List[RfxClarificationMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM rfx_clarification_meta WHERE rfx_clarification_id = %s AND lower(meta_key) = %s;"
    cursor.execute(query, (rfx_clarification_id, meta_key.lower()))
    rf_clarification_metas = cursor.fetchall()

    conn.close()

    return[ 
        RfxClarificationMeta(
            rfx_clarification_meta_id=rf_clarification_meta[0],
            rfx_id=rf_clarification_meta[1],
            rfx_clarification_id=rf_clarification_meta[2],
            rfx_clarification_post_id=rf_clarification_meta[3],
            meta_key=rf_clarification_meta[4],
            meta_id=rf_clarification_meta[5]
        ) 
        for rf_clarification_meta in rf_clarification_metas
    ]
    
    
# Function to get RfxClarification Meta by Post ID & Key
def get_rf_clarification_meta_by_post_id_and_key(rfx_clarification_id: int, rfx_clarification_post_id: int, meta_key: str) -> List[RfxClarificationMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM rfx_clarification_meta WHERE rfx_clarification_id = %s AND rfx_clarification_post_id = %s AND lower(meta_key) = %s;"
    cursor.execute(query, (rfx_clarification_id, rfx_clarification_post_id, meta_key.lower()))
    rf_clarification_metas = cursor.fetchall()

    conn.close()

    return[ 
        RfxClarificationMeta(
            rfx_clarification_meta_id=rf_clarification_meta[0],
            rfx_id=rf_clarification_meta[1],
            rfx_clarification_id=rf_clarification_meta[2],
            rfx_clarification_post_id=rf_clarification_meta[3],
            meta_key=rf_clarification_meta[4],
            meta_id=rf_clarification_meta[5]
        ) 
        for rf_clarification_meta in rf_clarification_metas
    ]
