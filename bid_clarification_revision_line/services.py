from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import BidClarificationRevisionLineCreate, BidClarificationRevisionLine

# Create a Bid Clarification Revision Line
def create_bid_clarification_revision_line(bid_clarification_revision_line_data: BidClarificationRevisionLineCreate) -> BidClarificationRevisionLine:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_clarification_revision_line (
        bid_clarification_id, bid_clarification_revision_id
    ) VALUES (%s, %s) RETURNING *;
    """

    values = (
        bid_clarification_revision_line_data.bid_clarification_id,
        bid_clarification_revision_line_data.bid_clarification_revision_id,
    )

    cursor.execute(query, values)
    new_bid_clarification_revision_line = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_bid_clarification_revision_line:
        return BidClarificationRevisionLine(
            bid_clarification_revision_line_id=new_bid_clarification_revision_line[0],
            bid_clarification_id=new_bid_clarification_revision_line[1],
            bid_clarification_revision_id=new_bid_clarification_revision_line[2],
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Clarification Revision Line creation failed")

# Get all Bid Clarification Revision Lines
def get_all_bid_clarification_revision_lines() -> List[BidClarificationRevisionLine]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_clarification_revision_line;"
    cursor.execute(query)
    bid_clarification_revision_lines = cursor.fetchall()

    conn.close()

    return [
        BidClarificationRevisionLine(
            bid_clarification_revision_line_id=row[0],
            bid_clarification_id=row[1],
            bid_clarification_revision_id=row[2],
        )
        for row in bid_clarification_revision_lines
    ]

# Delete Bid Clarification Revision Line by ID
def delete_bid_clarification_revision_line(bid_clarification_revision_line_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM bid_clarification_revision_line WHERE bid_clarification_revision_line_id = %s RETURNING *;"
    cursor.execute(query, (bid_clarification_revision_line_id,))
    deleted_bid_clarification_revision_line = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_bid_clarification_revision_line:
        return True
    else:
        return False

# Get Bid Clarification Revision Line by ID
def get_bid_clarification_revision_line_by_id(bid_clarification_revision_line_id: int) -> Optional[BidClarificationRevisionLine]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_clarification_revision_line WHERE bid_clarification_revision_line_id = %s;"
    cursor.execute(query, (bid_clarification_revision_line_id,))
    bid_clarification_revision_line = cursor.fetchone()

    conn.close()

    if bid_clarification_revision_line:
        return BidClarificationRevisionLine(
            bid_clarification_revision_line_id=bid_clarification_revision_line[0],
            bid_clarification_id=bid_clarification_revision_line[1],
            bid_clarification_revision_id=bid_clarification_revision_line[2],
        )
    else:
        return None

# Update Bid Clarification Revision Line
def update_bid_clarification_revision_line(bid_clarification_revision_line_id: int, bid_clarification_revision_line_data: BidClarificationRevisionLineCreate) -> Optional[BidClarificationRevisionLine]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_clarification_revision_line SET 
        bid_clarification_id = %s,
        bid_clarification_revision_id = %s
    WHERE bid_clarification_revision_line_id = %s RETURNING *;
    """

    values = (
        bid_clarification_revision_line_data.bid_clarification_id,
        bid_clarification_revision_line_data.bid_clarification_revision_id,
        bid_clarification_revision_line_id,
    )

    cursor.execute(query, values)
    updated_bid_clarification_revision_line = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_clarification_revision_line:
        return BidClarificationRevisionLine(
            bid_clarification_revision_line_id=updated_bid_clarification_revision_line[0],
            bid_clarification_id=updated_bid_clarification_revision_line[1],
            bid_clarification_revision_id=updated_bid_clarification_revision_line[2],
        )
    else:
        return None
