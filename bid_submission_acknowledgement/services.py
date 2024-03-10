from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from bid_submission_acknowledgement.schemas import BidSubmissionAcknowledgementCreate, BidSubmissionAcknowledgement


def create_bid_submission_acknowledgement(item_form_data: BidSubmissionAcknowledgementCreate) -> BidSubmissionAcknowledgement:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO bid_submission_acknowledgement (
        bid_submission_id,
        acknowledgement_deadline,
        acknowledgement_comment,
        acknowledged_by,
        acknowledgement_date,
        acknowledged_on,
        acknowledged
    ) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        item_form_data.bid_submission_id,
        item_form_data.acknowledgement_deadline,
        item_form_data.acknowledgement_comment,
        item_form_data.acknowledged_by,
        item_form_data.acknowledgement_date,
        item_form_data.acknowledged_on,
        item_form_data.acknowledged
    )

    cursor.execute(query, values)
    new_item = cursor.fetchone()

   
    conn.commit()
    conn.close()

    if new_item:
        return BidSubmissionAcknowledgement(
            bid_submission_acknowledgement_id=new_item[0],
            bid_submission_id=new_item[1],
            acknowledgement_deadline=new_item[2],
            acknowledgement_comment=new_item[3],
            acknowledged_by=new_item[4],
            acknowledgement_date=new_item[5],
            acknowledged_on=new_item[6],
            acknowledged=new_item[7]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Submission Acknowledgement Detail creation failed")


def get_bid_submission_acknowledgement(bid_submission_id: int) -> BidSubmissionAcknowledgement:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bid_submission_acknowledgement              
        WHERE bid_submission_id = %s ;
        """

    cursor.execute(query,(bid_submission_id, ))
    get_item = cursor.fetchone()

    conn.close()
    if get_item:
        return BidSubmissionAcknowledgement(
                bid_submission_acknowledgement_id=get_item[0],
                bid_submission_id=get_item[1],
                acknowledgement_deadline=get_item[2],
                acknowledgement_comment=get_item[3],
                acknowledged_by=get_item[4],
                acknowledgement_date=get_item[5],
                acknowledged_on=get_item[6],
                acknowledged=get_item[7]
            )
            
    else:
        None


def update_bid_submission_acknowledgement(bid_submission_acknowledgement_id: int,  item_form_data: BidSubmissionAcknowledgementCreate) -> Optional[BidSubmissionAcknowledgement]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_submission_acknowledgement SET 
        acknowledgement_deadline = %s,
        acknowledgement_comment = %s,
        acknowledged_by = %s,
        acknowledgement_date = %s,
        acknowledged_on = %s,
        acknowledged = %s
    WHERE bid_submission_acknowledgement_id = %s RETURNING *;
    """

    values = (
        item_form_data.acknowledgement_deadline,
        item_form_data.acknowledgement_comment,
        item_form_data.acknowledged_by,
        item_form_data.acknowledgement_date,
        item_form_data.acknowledged_on,
        item_form_data.acknowledged,
        bid_submission_acknowledgement_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return BidSubmissionAcknowledgement(
            bid_submission_acknowledgement_id=updated_itemm[0],
            bid_submission_id=updated_itemm[1],
            acknowledgement_deadline=updated_itemm[2],
            acknowledgement_comment=updated_itemm[3],
            acknowledged_by=updated_itemm[4],
            acknowledgement_date=updated_itemm[5],
            acknowledged_on=updated_itemm[6],
            acknowledged=updated_itemm[7]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Submission Acknowledgement update failed")
    
    
def update_bid_submission_acknowledgement_by_submission_id(bid_submission_id: int,  item_form_data: BidSubmissionAcknowledgementCreate) -> Optional[BidSubmissionAcknowledgement]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_submission_acknowledgement SET 
        acknowledgement_comment = %s,
        acknowledged_by = %s,
        acknowledgement_date = %s,
        acknowledged_on = %s,
        acknowledged = %s
    WHERE bid_submission_id = %s RETURNING *;
    """

    values = (
        item_form_data.acknowledgement_comment,
        item_form_data.acknowledged_by,
        item_form_data.acknowledgement_date,
        item_form_data.acknowledged_on,
        item_form_data.acknowledged,
        bid_submission_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return BidSubmissionAcknowledgement(
            bid_submission_acknowledgement_id=updated_itemm[0],
            bid_submission_id=updated_itemm[1],
            acknowledgement_deadline=updated_itemm[2],
            acknowledgement_comment=updated_itemm[3],
            acknowledged_by=updated_itemm[4],
            acknowledgement_date=updated_itemm[5],
            acknowledged_on=updated_itemm[6],
            acknowledged=updated_itemm[7]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Submission Acknowledgement update failed")


def delete_bid_submission_acknowledgement(bid_submission_acknowledgement_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM bid_submission_acknowledgement WHERE bid_submission_acknowledgement_id = %s RETURNING bid_submission_acknowledgement_id;"
    cursor.execute(query, (bid_submission_acknowledgement_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False


def get_bid_submission_acknowledgement_by_submission_id(bid_submission_id: int) -> Optional[BidSubmissionAcknowledgement]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_submission_acknowledgement WHERE bid_submission_id = %s ;"

    cursor.execute(query, (bid_submission_id,))
    get_item = cursor.fetchone()

    conn.close()

    if get_item:
        return BidSubmissionAcknowledgement (
            bid_submission_acknowledgement_id=get_item[0],
            bid_submission_id=get_item[1],
            acknowledgement_deadline=get_item[2],
            acknowledgement_comment=get_item[3],
            acknowledged_by=get_item[4],
            acknowledgement_date=get_item[5],
            acknowledged_on=get_item[6],
            acknowledged=get_item[7]
            )
    else:
        return None


