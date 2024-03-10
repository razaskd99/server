from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import BidClarificationCreate, BidClarification, UpdateBidClarificationStatus
from datetime import date

# Create a Bid Clarification
def create_bid_clarification(bid_clarification_data: BidClarificationCreate) -> BidClarification:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_clarification (
        rfx_id, submitted_by, assigned_to, reference_num, title, type, status,
        description, issued_date, due_date, completed, completed_on
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_clarification_data.rfx_id,
        bid_clarification_data.submitted_by,
        bid_clarification_data.assigned_to,
        bid_clarification_data.reference_num,
        bid_clarification_data.title,
        bid_clarification_data.type,
        bid_clarification_data.status,
        bid_clarification_data.description,
        bid_clarification_data.issued_date,
        bid_clarification_data.due_date,
        bid_clarification_data.completed,
        bid_clarification_data.completed_on
    )

    cursor.execute(query, values)
    new_bid_clarification = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_bid_clarification:
        return BidClarification(
            bid_clarification_id=new_bid_clarification[0],
            rfx_id=new_bid_clarification[1],
            submitted_by=new_bid_clarification[2],
            assigned_to=new_bid_clarification[3],
            reference_num=new_bid_clarification[4],
            title=new_bid_clarification[5],
            type=new_bid_clarification[6],
            status=new_bid_clarification[7],
            description=new_bid_clarification[8],
            issued_date=new_bid_clarification[9],
            due_date=new_bid_clarification[10],
            completed=new_bid_clarification[11],
            completed_on=new_bid_clarification[12]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Clarification creation failed")

# Get all Bid Clarifications
def get_all_bid_clarifications(rfx_id: int) -> List[BidClarification]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_clarification WHERE rfx_id = %s ORDER BY issued_date DESC;"
    cursor.execute(query, (rfx_id,))
    bid_clarifications = cursor.fetchall()

    conn.close()

    return [
        BidClarification(
            bid_clarification_id=row[0],
            rfx_id=row[1],
            submitted_by=row[2],
            assigned_to=row[3],
            reference_num=row[4],
            title=row[5],
            type=row[6],
            status=row[7],
            description=row[8],
            issued_date=row[9],
            due_date=row[10],
            completed=row[11],
            completed_on=row[12]
        )
        for row in bid_clarifications
    ]

# Update Bid Clarification by ID
def update_bid_clarification(bid_clarification_id: int, bid_clarification_data: BidClarificationCreate) -> Optional[BidClarification]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_clarification SET 
        submitted_by = %s,
        assigned_to = %s,
        reference_num = %s,
        title = %s,
        type = %s,
        status = %s,
        description = %s,
        issued_date = %s,
        due_date = %s,
        completed = %s,
        completed_on = %s
    WHERE bid_clarification_id = %s RETURNING *;
    """

    values = (
        bid_clarification_data.submitted_by,
        bid_clarification_data.assigned_to,
        bid_clarification_data.reference_num,
        bid_clarification_data.title,
        bid_clarification_data.type,
        bid_clarification_data.status,
        bid_clarification_data.description,
        bid_clarification_data.issued_date,
        bid_clarification_data.due_date,
        bid_clarification_data.completed,
        bid_clarification_data.completed_on,
        bid_clarification_id
    )

    cursor.execute(query, values)
    updated_bid_clarification = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_clarification:
        return BidClarification(
            bid_clarification_id=updated_bid_clarification[0],
            rfx_id=updated_bid_clarification[1],
            submitted_by=updated_bid_clarification[2],
            assigned_to=updated_bid_clarification[3],
            reference_num=updated_bid_clarification[4],
            title=updated_bid_clarification[5],
            type=updated_bid_clarification[6],
            status=updated_bid_clarification[7],
            description=updated_bid_clarification[8],
            issued_date=updated_bid_clarification[9],
            due_date=updated_bid_clarification[10],
            completed=updated_bid_clarification[11],
            completed_on=updated_bid_clarification[12]
        )
    else:
        return None

# Delete Bid Clarification by ID
def delete_bid_clarification(bid_clarification_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM bid_clarification WHERE bid_clarification_id = %s RETURNING bid_clarification_id;"
    cursor.execute(query, (bid_clarification_id,))
    deleted_bid_clarification = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_bid_clarification:
        return True
    else:
        return False

# Get Bid Clarification by ID
def get_bid_clarification_by_id(bid_clarification_id: int) -> Optional[BidClarification]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_clarification WHERE bid_clarification_id = %s ORDER BY issued_date DESC;"
    cursor.execute(query, (bid_clarification_id,))
    bid_clarification = cursor.fetchone()

    conn.close()

    if bid_clarification:
        return BidClarification(
            bid_clarification_id=bid_clarification[0],
            rfx_id=bid_clarification[1],
            submitted_by=bid_clarification[2],
            assigned_to=bid_clarification[3],
            reference_num=bid_clarification[4],
            title=bid_clarification[5],
            type=bid_clarification[6],
            status=bid_clarification[7],
            description=bid_clarification[8],
            issued_date=bid_clarification[9],
            due_date=bid_clarification[10],
            completed=bid_clarification[11],
            completed_on=bid_clarification[12]
        )
    else:
        return None

# Get Bid Clarification by title
def get_bid_clarification_by_title(rfx_id: int, title: str) -> Optional[BidClarification]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_clarification WHERE rfx_id = %s AND lower(title) = %s ORDER BY issued_date DESC;"
    cursor.execute(query, (rfx_id, title.lower()))
    bid_clarification = cursor.fetchone()

    conn.close()

    if bid_clarification:
        return BidClarification(
            bid_clarification_id=bid_clarification[0],
            rfx_id=bid_clarification[1],
            submitted_by=bid_clarification[2],
            assigned_to=bid_clarification[3],
            reference_num=bid_clarification[4],
            title=bid_clarification[5],
            type=bid_clarification[6],
            status=bid_clarification[7],
            description=bid_clarification[8],
            issued_date=bid_clarification[9],
            due_date=bid_clarification[10],
            completed=bid_clarification[11],
            completed_on=bid_clarification[12]
        )
    else:
        return None
    
# Get Bid Clarification by status
def get_bid_clarification_by_status(rfx_id: int, status: str) -> List[BidClarification]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_clarification WHERE rfx_id = %s AND lower(status) = %s ORDER BY issued_date DESC;"
    cursor.execute(query, (rfx_id, status.lower()))
    bid_clarification = cursor.fetchall()

    conn.close()

    return [
        BidClarification(
            bid_clarification_id=row[0],
            rfx_id=row[1],
            submitted_by=row[2],
            assigned_to=row[3],
            reference_num=row[4],
            title=row[5],
            type=row[6],
            status=row[7],
            description=row[8],
            issued_date=row[9],
            due_date=row[10],
            completed=row[11],
            completed_on=row[12]
        )
        for row in bid_clarification
    ]

def update_bid_clarification_status(bid_clarification_id: int, bid_clarification_data: UpdateBidClarificationStatus) -> Optional[BidClarification]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_clarification SET        
        status = %s,
        completed = %s,
        completed_on = %s
    WHERE bid_clarification_id = %s RETURNING *;
    """

    values = (
        bid_clarification_data.status,
        bid_clarification_data.completed,
        bid_clarification_data.completed_on,
        bid_clarification_id
    )

    cursor.execute(query, values)
    updated_bid_clarification = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_clarification:
        return BidClarification(
            bid_clarification_id=updated_bid_clarification[0],
            rfx_id=updated_bid_clarification[1],
            submitted_by=updated_bid_clarification[2],
            assigned_to=updated_bid_clarification[3],
            reference_num=updated_bid_clarification[4],
            title=updated_bid_clarification[5],
            type=updated_bid_clarification[6],
            status=updated_bid_clarification[7],
            description=updated_bid_clarification[8],
            issued_date=updated_bid_clarification[9],
            due_date=updated_bid_clarification[10],
            completed=updated_bid_clarification[11],
            completed_on=updated_bid_clarification[12]
        )
    else:
        return None
