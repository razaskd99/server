from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import BidClarificationMetaCreate, BidClarificationMeta

# Create Bid Clarification Meta
def create_bid_clarification_meta(bid_clarification_meta_data: BidClarificationMetaCreate) -> BidClarificationMeta:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_clarification_meta (rfx_id, bid_clarification_id, meta_key, meta_id)
    VALUES (%s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_clarification_meta_data.rfx_id,
        bid_clarification_meta_data.bid_clarification_id,
        bid_clarification_meta_data.meta_key,
        bid_clarification_meta_data.meta_id,
    )

    cursor.execute(query, values)
    new_bid_clarification_meta = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_bid_clarification_meta:
        return BidClarificationMeta(
            bid_clarification_meta_id=new_bid_clarification_meta[0],
            rfx_id=new_bid_clarification_meta[1],
            bid_clarification_id=new_bid_clarification_meta[2],
            meta_key=new_bid_clarification_meta[3],
            meta_id=new_bid_clarification_meta[4],
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Clarification Meta creation failed")

# Get all Bid Clarification Meta
def get_all_bid_clarification_meta() -> List[BidClarificationMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_clarification_meta;"
    cursor.execute(query)
    bid_clarification_meta_list = cursor.fetchall()

    conn.close()

    return [
        BidClarificationMeta(
            bid_clarification_meta_id=row[0],
            rfx_id=row[1],
            bid_clarification_id=row[2],
            meta_key=row[3],
            meta_id=row[4],
        )
        for row in bid_clarification_meta_list
    ]

# Update Bid Clarification Meta by ID
def update_bid_clarification_meta(bid_clarification_meta_id: int, bid_clarification_meta_data: BidClarificationMetaCreate) -> Optional[BidClarificationMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_clarification_meta
    SET
        rfx_id = %s,
        bid_clarification_id = %s,
        meta_key = %s,
        meta_id = %s
    WHERE bid_clarification_meta_id = %s RETURNING *;
    """

    values = (
        bid_clarification_meta_data.rfx_id,
        bid_clarification_meta_data.bid_clarification_id,
        bid_clarification_meta_data.meta_key,
        bid_clarification_meta_data.meta_id,
        bid_clarification_meta_id,
    )

    cursor.execute(query, values)
    updated_bid_clarification_meta = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_clarification_meta:
        return BidClarificationMeta(
            bid_clarification_meta_id=updated_bid_clarification_meta[0],
            rfx_id=updated_bid_clarification_meta[1],
            bid_clarification_id=updated_bid_clarification_meta[2],
            meta_key=updated_bid_clarification_meta[3],
            meta_id=updated_bid_clarification_meta[4],
        )
    else:
        return None

# Delete Bid Clarification Meta by ID
def delete_bid_clarification_meta(bid_clarification_meta_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM bid_clarification_meta WHERE bid_clarification_meta_id = %s RETURNING *;"
    cursor.execute(query, (bid_clarification_meta_id,))
    deleted_bid_clarification_meta = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_bid_clarification_meta:
        return True
    else:
        return False

# Get Bid Clarification Meta by ID
def get_bid_clarification_meta_by_id(bid_clarification_meta_id: int) -> Optional[BidClarificationMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_clarification_meta WHERE bid_clarification_meta_id = %s;"
    cursor.execute(query, (bid_clarification_meta_id,))
    bid_clarification_meta = cursor.fetchone()

    conn.close()

    if bid_clarification_meta:
        return BidClarificationMeta(
            bid_clarification_meta_id=bid_clarification_meta[0],
            rfx_id=bid_clarification_meta[1],
            bid_clarification_id=bid_clarification_meta[2],
            meta_key=bid_clarification_meta[3],
            meta_id=bid_clarification_meta[4],
        )
    else:
        return None
