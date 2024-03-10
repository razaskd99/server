from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from bid_submission.schemas import BidSubmissionCreate, BidSubmission, UpdateAssignToID


def create_bid_submission(bid_submission_data: BidSubmissionCreate) -> BidSubmission:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_submission (
        rfx_id,
        bid_type,
        bid_stage,
        assign_to_id,
        submitted_by,
        reference_number,
        description,
        status,
        issued_date,
        due_date,
        created_on
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_submission_data.rfx_id,
        bid_submission_data.bid_type,
        bid_submission_data.bid_stage,
        bid_submission_data.assign_to_id,
        bid_submission_data.submitted_by,
        bid_submission_data.reference_number,
        bid_submission_data.description,
        bid_submission_data.status,
        bid_submission_data.issued_date,
        bid_submission_data.due_date,
        bid_submission_data.created_on
    )

    cursor.execute(query, values)
    new_submission = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if new_submission:
        return BidSubmission(
            bid_submission_id=new_submission[0],
            rfx_id=new_submission[1],
            bid_type=new_submission[2],
            bid_stage=new_submission[3],
            assign_to_id=new_submission[4],
            submitted_by=new_submission[5],
            reference_number=new_submission[6],
            description=new_submission[7],
            status=new_submission[8],
            issued_date=new_submission[9],
            due_date=new_submission[10],
            created_on=new_submission[11]            
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Submission creation failed")


def get_all_bid_submission(rfx_id: int) -> List[BidSubmission]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bid_submission WHERE rfx_id = %s
        ORDER BY created_on DESC;
        """

    cursor.execute(query,(rfx_id,))
    bid_submission = cursor.fetchall()

    conn.close()
    if bid_submission:
        return [
            BidSubmission(
                bid_submission_id=row[0],
                rfx_id=row[1],
                bid_type=row[2],
                bid_stage=row[3],
                assign_to_id=row[4],
                submitted_by=row[5],
                reference_number=row[6],
                description=row[7],
                status=row[8],
                issued_date=row[9],
                due_date=row[10],
                created_on=row[11] 
            )
            for row in bid_submission
        ]
    else:
        None
        
def update_bid_submission(bid_submission_id: int, bid_submission_data: BidSubmissionCreate) -> Optional[BidSubmission]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_submission SET 
        assign_to_id = %s,
        reference_number = %s,
        description = %s,
        status = %s,
        issued_date = %s,
        due_date = %s
    WHERE bid_submission_id = %s RETURNING *;
    """
    
    values = (
        bid_submission_data.assign_to_id,
        bid_submission_data.reference_number,
        bid_submission_data.description,
        bid_submission_data.status,
        bid_submission_data.issued_date,
        bid_submission_data.due_date,
        bid_submission_id
    )

    cursor.execute(query, values)
    bid_submission = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if bid_submission:
        return BidSubmission(
                bid_submission_id=bid_submission[0],
                rfx_id=bid_submission[1],
                bid_type=bid_submission[2],
                bid_stage=bid_submission[3],
                assign_to_id=bid_submission[4],
                submitted_by=bid_submission[5],
                reference_number=bid_submission[6],
                description=bid_submission[7],
                status=bid_submission[8],
                issued_date=bid_submission[9],
                due_date=bid_submission[10],
                created_on=bid_submission[11]
            )      
    else:
        None
 

def update_bid_submission_assign_to_id(bid_submission_id: int, bid_submission_data: UpdateAssignToID) -> Optional[BidSubmission]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_submission SET 
        assign_to_id = %s
    WHERE bid_submission_id = %s RETURNING *;
    """
      
    values = (
        bid_submission_data.assign_to_id,
        bid_submission_id
    )

    cursor.execute(query, values)
    bid_submission = cursor.fetchone()
    
    conn.commit()
    conn.close()
    if bid_submission:
        return BidSubmission(
                bid_submission_id=bid_submission[0],
                rfx_id=bid_submission[1],
                bid_type=bid_submission[2],
                bid_stage=bid_submission[3],
                assign_to_id=bid_submission[4],
                submitted_by=bid_submission[5],
                reference_number=bid_submission[6],
                description=bid_submission[7],
                status=bid_submission[8],
                issued_date=bid_submission[9],
                due_date=bid_submission[10],
                created_on=bid_submission[11]
            )
           
        
    else:
        None
       
def delete_bid_submission(bid_submission_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "DELETE FROM bid_submission WHERE bid_submission_id = %s RETURNING bid_submission_id;"
    cursor.execute(query, (bid_submission_id,))
    deleted_bid_submission = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if deleted_bid_submission:
        return True
    else:
        return False


def get_bid_submission_by_id(bid_submission_id: int) -> Optional[BidSubmission]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bid_submission WHERE bid_submission_id = %s
        ORDER BY created_on DESC;
        """

    cursor.execute(query,(bid_submission_id,))
    bid_submission = cursor.fetchone()

    conn.close()
    if bid_submission:
        return BidSubmission(
                bid_submission_id=bid_submission[0],
                rfx_id=bid_submission[1],
                bid_type=bid_submission[2],
                bid_stage=bid_submission[3],
                assign_to_id=bid_submission[4],
                submitted_by=bid_submission[5],
                reference_number=bid_submission[6],
                description=bid_submission[7],
                status=bid_submission[8],
                issued_date=bid_submission[9],
                due_date=bid_submission[10],
                created_on=bid_submission[11]
            )
    else:
        None