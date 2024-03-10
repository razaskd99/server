from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import BidOrderMetaCreate, BidOrderMeta

# Create Bid Order Meta
def create_bid_order_meta(bid_order_meta_data: BidOrderMetaCreate) -> BidOrderMeta:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_order_meta (rfx_id, order_post_id, meta_key, meta_id)
    VALUES (%s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_order_meta_data.rfx_id,
        bid_order_meta_data.order_post_id,
        bid_order_meta_data.meta_key,
        bid_order_meta_data.meta_id,
    )

    cursor.execute(query, values)
    new_bid_order_meta = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_bid_order_meta:
        return BidOrderMeta(
            bid_order_meta_id=new_bid_order_meta[0],
            rfx_id=new_bid_order_meta[1],
            order_post_id=new_bid_order_meta[2],
            meta_key=new_bid_order_meta[3],
            meta_id=new_bid_order_meta[4],
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Order Meta creation failed")

# Get all Bid Order Metas
def get_all_bid_order_metas() -> List[BidOrderMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_order_meta;"
    cursor.execute(query)
    bid_order_metas = cursor.fetchall()

    conn.close()

    return [
        BidOrderMeta(
            bid_order_meta_id=row[0],
            rfx_id=row[1],
            order_post_id=row[2],
            meta_key=row[3],
            meta_id=row[4],
        )
        for row in bid_order_metas
    ]

# Delete Bid Order Meta by ID
def delete_bid_order_meta(bid_order_meta_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM bid_order_meta WHERE bid_order_meta_id = %s RETURNING *;"
    cursor.execute(query, (bid_order_meta_id,))
    deleted_bid_order_meta = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_bid_order_meta:
        return True
    else:
        return False

# Get Bid Order Meta by ID
def get_bid_order_meta_by_id(bid_order_meta_id: int) -> Optional[BidOrderMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_order_meta WHERE bid_order_meta_id = %s;"
    cursor.execute(query, (bid_order_meta_id,))
    bid_order_meta = cursor.fetchone()

    conn.close()

    if bid_order_meta:
        return BidOrderMeta(
            bid_order_meta_id=bid_order_meta[0],
            rfx_id=bid_order_meta[1],
            order_post_id=bid_order_meta[2],
            meta_key=bid_order_meta[3],
            meta_id=bid_order_meta[4],
        )
    else:
        return None

# Update Bid Order Meta by ID
def update_bid_order_meta(bid_order_meta_id: int, new_data: BidOrderMetaCreate) -> Optional[BidOrderMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_order_meta
    SET rfx_id = %s, order_post_id = %s, meta_key = %s, meta_id = %s
    WHERE bid_order_meta_id = %s RETURNING *;
    """

    values = (
        new_data.rfx_id,
        new_data.order_post_id,
        new_data.meta_key,
        new_data.meta_id,
        bid_order_meta_id
    )

    cursor.execute(query, values)
    updated_bid_order_meta = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_order_meta:
        return BidOrderMeta(
            bid_order_meta_id=updated_bid_order_meta[0],
            rfx_id=updated_bid_order_meta[1],
            order_post_id=updated_bid_order_meta[2],
            meta_key=updated_bid_order_meta[3],
            meta_id=updated_bid_order_meta[4],
        )
    else:
        return None
