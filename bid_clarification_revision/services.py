from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import BidClarificationRevisionCreate, BidClarificationRevision
from datetime import date, datetime

# Create a Bid Clarification Revision
def create_bid_clarification_revision(bid_clarification_revision_data: BidClarificationRevisionCreate) -> BidClarificationRevision:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_clarification_revision (
        rfx_id, bid_clarification_id, comment, due_date, created_date, created_at, revision_completed
    ) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_clarification_revision_data.rfx_id,
        bid_clarification_revision_data.bid_clarification_id,
        bid_clarification_revision_data.comment,
        bid_clarification_revision_data.due_date,
        bid_clarification_revision_data.created_date,
        bid_clarification_revision_data.created_at,
        bid_clarification_revision_data.revision_completed,
    )

    cursor.execute(query, values)
    new_bid_clarification_revision = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_bid_clarification_revision:
        return BidClarificationRevision(
            bid_clarification_revision_id=new_bid_clarification_revision[0],
            rfx_id=new_bid_clarification_revision[1],
            bid_clarification_id=new_bid_clarification_revision[2],
            comment=new_bid_clarification_revision[3],
            due_date=new_bid_clarification_revision[4],
            created_date=new_bid_clarification_revision[5],
            created_at=new_bid_clarification_revision[6],
            revision_completed=new_bid_clarification_revision[7],
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Clarification Revision creation failed")

# Get all Bid Clarification Revisions
def get_all_bid_clarification_revisions() -> List[BidClarificationRevision]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_clarification_revision;"
    cursor.execute(query)
    bid_clarification_revisions = cursor.fetchall()

    conn.close()

    return [
        BidClarificationRevision(
            bid_clarification_revision_id=row[0],
            rfx_id=row[1],
            bid_clarification_id=row[2],
            comment=row[3],
            due_date=row[4],
            created_date=row[5],
            created_at=row[6],
            revision_completed=row[7],
        )
        for row in bid_clarification_revisions
    ]

# Update Bid Clarification Revision by ID
def update_bid_clarification_revision(bid_clarification_revision_id: int, bid_clarification_revision_data: BidClarificationRevisionCreate) -> Optional[BidClarificationRevision]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_clarification_revision SET 
        rfx_id = %s,
        bid_clarification_id = %s,
        comment = %s,
        due_date = %s,
        created_date = %s,
        created_at = %s,
        revision_completed = %s
    WHERE bid_clarification_revision_id = %s RETURNING *;
    """

    values = (
        bid_clarification_revision_data.rfx_id,
        bid_clarification_revision_data.bid_clarification_id,
        bid_clarification_revision_data.comment,
        bid_clarification_revision_data.due_date,
        bid_clarification_revision_data.created_date,
        bid_clarification_revision_data.created_at,
        bid_clarification_revision_data.revision_completed,
        bid_clarification_revision_id
    )

    cursor.execute(query, values)
    updated_bid_clarification_revision = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_clarification_revision:
        return BidClarificationRevision(
            bid_clarification_revision_id=updated_bid_clarification_revision[0],
            rfx_id=updated_bid_clarification_revision[1],
            bid_clarification_id=updated_bid_clarification_revision[2],
            comment=updated_bid_clarification_revision[3],
            due_date=updated_bid_clarification_revision[4],
            created_date=updated_bid_clarification_revision[5],
            created_at=updated_bid_clarification_revision[6],
            revision_completed=updated_bid_clarification_revision[7],
        )
    else:
        return None

# Delete Bid Clarification Revision by ID
def delete_bid_clarification_revision(bid_clarification_revision_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM bid_clarification_revision WHERE bid_clarification_revision_id = %s RETURNING *;"
    cursor.execute(query, (bid_clarification_revision_id,))
    deleted_bid_clarification_revision = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_bid_clarification_revision:
        return True
    else:
        return False

# Get Bid Clarification Revision by ID
def get_bid_clarification_revision_by_id(bid_clarification_revision_id: int) -> Optional[BidClarificationRevision]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_clarification_revision WHERE bid_clarification_revision_id = %s;"
    cursor.execute(query, (bid_clarification_revision_id,))
    bid_clarification_revision = cursor.fetchone()

    conn.close()

    if bid_clarification_revision:
        return BidClarificationRevision(
            bid_clarification_revision_id=bid_clarification_revision[0],
            rfx_id=bid_clarification_revision[1],
            bid_clarification_id=bid_clarification_revision[2],
            comment=bid_clarification_revision[3],
            due_date=bid_clarification_revision[4],
            created_date=bid_clarification_revision[5],
            created_at=bid_clarification_revision[6],
            revision_completed=bid_clarification_revision[7],
        )
    else:
        return None
