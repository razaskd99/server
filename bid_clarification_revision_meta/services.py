from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import BidClarificationRevisionMetaCreate, BidClarificationRevisionMeta

# Create a Bid Clarification Revision Meta
def create_bid_clarification_revision_meta(bid_clarification_revision_meta_data: BidClarificationRevisionMetaCreate) -> BidClarificationRevisionMeta:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_clarification_revision_meta (
        rfx_id, bid_clarification_id, bid_clarification_revision_line_id, meta_key, meta_id
    ) VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_clarification_revision_meta_data.rfx_id,
        bid_clarification_revision_meta_data.bid_clarification_id,
        bid_clarification_revision_meta_data.bid_clarification_revision_line_id,
        bid_clarification_revision_meta_data.meta_key,
        bid_clarification_revision_meta_data.meta_id,
    )

    cursor.execute(query, values)
    new_bid_clarification_revision_meta = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_bid_clarification_revision_meta:
        return BidClarificationRevisionMeta(
            bid_clarification_revision_meta_id=new_bid_clarification_revision_meta[0],
            rfx_id=new_bid_clarification_revision_meta[1],
            bid_clarification_id=new_bid_clarification_revision_meta[2],
            bid_clarification_revision_line_id=new_bid_clarification_revision_meta[3],
            meta_key=new_bid_clarification_revision_meta[4],
            meta_id=new_bid_clarification_revision_meta[5],
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Clarification Revision Meta creation failed")

# Get all Bid Clarification Revision Metas
def get_all_bid_clarification_revision_metas() -> List[BidClarificationRevisionMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_clarification_revision_meta;"
    cursor.execute(query)
    bid_clarification_revision_metas = cursor.fetchall()

    conn.close()

    return [
        BidClarificationRevisionMeta(
            bid_clarification_revision_meta_id=row[0],
            rfx_id=row[1],
            bid_clarification_id=row[2],
            bid_clarification_revision_line_id=row[3],
            meta_key=row[4],
            meta_id=row[5],
        )
        for row in bid_clarification_revision_metas
    ]

# Delete Bid Clarification Revision Meta by ID
def delete_bid_clarification_revision_meta(bid_clarification_revision_meta_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM bid_clarification_revision_meta WHERE id_clarification_revision_meta_id = %s RETURNING *;"
    cursor.execute(query, (bid_clarification_revision_meta_id,))
    deleted_bid_clarification_revision_meta = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_bid_clarification_revision_meta:
        return True
    else:
        return False

# Get Bid Clarification Revision Meta by ID
def get_bid_clarification_revision_meta_by_id(bid_clarification_revision_meta_id: int) -> Optional[BidClarificationRevisionMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_clarification_revision_meta WHERE id_clarification_revision_meta_id = %s;"
    cursor.execute(query, (bid_clarification_revision_meta_id,))
    bid_clarification_revision_meta = cursor.fetchone()

    conn.close()

    if bid_clarification_revision_meta:
        return BidClarificationRevisionMeta(
            bid_clarification_revision_meta_id=bid_clarification_revision_meta[0],
            rfx_id=bid_clarification_revision_meta[1],
            bid_clarification_id=bid_clarification_revision_meta[2],
            bid_clarification_revision_line_id=bid_clarification_revision_meta[3],
            meta_key=bid_clarification_revision_meta[4],
            meta_id=bid_clarification_revision_meta[5],
        )
    else:
        return None

# Update Bid Clarification Revision Meta by ID
def update_bid_clarification_revision_meta(bid_clarification_revision_meta_id: int, new_data: BidClarificationRevisionMetaCreate) -> Optional[BidClarificationRevisionMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_clarification_revision_meta
    SET rfx_id = %s, bid_clarification_id = %s, bid_clarification_revision_line_id = %s, meta_key = %s, meta_id = %s
    WHERE id_clarification_revision_meta_id = %s RETURNING *;
    """

    values = (
        new_data.rfx_id,
        new_data.bid_clarification_id,
        new_data.bid_clarification_revision_line_id,
        new_data.meta_key,
        new_data.meta_id,
        bid_clarification_revision_meta_id
    )

    cursor.execute(query, values)
    updated_bid_clarification_revision_meta = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_clarification_revision_meta:
        return BidClarificationRevisionMeta(
            bid_clarification_revision_meta_id=updated_bid_clarification_revision_meta[0],
            rfx_id=updated_bid_clarification_revision_meta[1],
            bid_clarification_id=updated_bid_clarification_revision_meta[2],
            bid_clarification_revision_line_id=updated_bid_clarification_revision_meta[3],
            meta_key=updated_bid_clarification_revision_meta[4],
            meta_id=updated_bid_clarification_revision_meta[5],
        )
    else:
        return None
