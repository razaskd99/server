from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection  # Replace with your database connection function
from datetime import date, datetime
from .schemas import BidDocumentsCreate, BidDocuments

def create_bid_document(bid_document_data: BidDocumentsCreate) -> BidDocuments:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO bid_documents (
            rfx_id, 
            submit_to_customer, 
            assigned_to, 
            submitted_to, 
            title, 
            reference_num, 
            document_type, 
            request_revision, 
            status, 
            comment
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
        """
    
    values = (
        bid_document_data.rfx_id,
        bid_document_data.submit_to_customer,
        bid_document_data.assigned_to,
        bid_document_data.submitted_to,
        bid_document_data.title,
        bid_document_data.reference_num,
        bid_document_data.document_type,
        bid_document_data.request_revision,
        bid_document_data.status,
        bid_document_data.comment,
    )

    cursor.execute(query, values)
    new_bid_document = cursor.fetchone()
    
    query = """
    INSERT INTO bid_documents_acknowledgement (
        bid_documents_id,
        rfx_id,
        acknowledged_by,
        acknowledgement_date,
        acknowledgement_comment, 
        acknowledged,
        acknowledgement_document, 
        acknowledgement_submitted_on       
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """
    
    values = (
        new_bid_document[0],
        bid_document_data.rfx_id,
        bid_document_data.acknowledged_by,
        bid_document_data.acknowledgement_date,
        bid_document_data.acknowledgement_comment,
        bid_document_data.acknowledged,
        bid_document_data.acknowledgement_document,
        bid_document_data.acknowledgement_submitted_on
    )

    cursor.execute(query, values)
    new_acknowledgement = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if new_bid_document:
        return BidDocuments(
            bid_documents_id=new_bid_document[0],
            rfx_id=new_bid_document[1],
            submit_to_customer=new_bid_document[2],
            assigned_to=new_bid_document[3],
            submitted_to=new_bid_document[4],
            title=new_bid_document[5],
            reference_num=new_bid_document[6],
            document_type=new_bid_document[7],
            request_revision=new_bid_document[8],
            status=new_bid_document[9],
            comment=new_bid_document[10],
            # acknowledgement
            acknowledged_by=new_acknowledgement[3],
            acknowledgement_date=new_acknowledgement[4],
            acknowledgement_comment=new_acknowledgement[5],
            acknowledged=new_acknowledgement[6],
            acknowledgement_document=new_acknowledgement[7],
            acknowledgement_submitted_on=new_acknowledgement[8]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Document creation failed")


def get_all_bid_documents(rfx_id: int) -> List[BidDocuments]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*, 
            a.acknowledged_by, a.acknowledgement_date, a.acknowledgement_comment,            
            a.acknowledged, a.acknowledgement_document, a.acknowledgement_submitted_on
            FROM bid_documents b
            INNER JOIN bid_documents_acknowledgement a ON a.bid_documents_id=b.bid_documents_id            
        WHERE b.rfx_id = %s;
        """
    
    cursor.execute(query, (rfx_id,))
    bid_documents = cursor.fetchall()
    
    conn.close()

    return [
        BidDocuments(
            bid_documents_id=row[0],
            rfx_id=row[1],
            submit_to_customer=row[2],
            assigned_to=row[3],
            submitted_to=row[4],
            title=row[5],
            reference_num=row[6],
            document_type=row[7],
            request_revision=row[8],
            status=row[9],
            comment=row[10],
            # acknowledgement
            acknowledged_by=row[11],
            acknowledgement_date=row[12],
            acknowledgement_comment=row[13],
            acknowledged=row[14],
            acknowledgement_document=row[15],
            acknowledgement_submitted_on=row[16]
        )
        for row in bid_documents
    ]


def get_bid_document_by_id(bid_documents_id: int) -> Optional[BidDocuments]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*, 
            a.acknowledged_by, a.acknowledgement_date, a.acknowledgement_comment,            
            a.acknowledged, a.acknowledgement_document, a.acknowledgement_submitted_on
            FROM bid_documents b
            INNER JOIN bid_documents_acknowledgement a ON a.bid_documents_id=b.bid_documents_id 
        WHERE b.bid_documents_id = %s;
        """
    cursor.execute(query, (bid_documents_id,))
    bid_document = cursor.fetchone()

    conn.close()
    print(bid_document)
    if bid_document:
        return BidDocuments(
            bid_documents_id=bid_document[0],
            rfx_id=bid_document[1],
            submit_to_customer=bid_document[2],
            assigned_to=bid_document[3],
            submitted_to=bid_document[4],
            title=bid_document[5],
            reference_num=bid_document[6],
            document_type=bid_document[7],
            request_revision=bid_document[8],
            status=bid_document[9],
            comment=bid_document[10],
            # acknowledgement
            acknowledged_by=bid_document[11],
            acknowledgement_date=bid_document[12],
            acknowledgement_comment=bid_document[13],
            acknowledged=bid_document[14],
            acknowledgement_document=bid_document[15],
            acknowledgement_submitted_on=bid_document[16]
        )
    else:
        return None


def update_bid_document(bid_documents_id: int, bid_document_data: BidDocumentsCreate) -> Optional[BidDocuments]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE bid_documents SET 
            submit_to_customer = %s,
            assigned_to = %s,
            submitted_to = %s,
            title = %s,
            reference_num = %s,
            document_type = %s,
            request_revision = %s,
            status = %s,
            comment = %s
        WHERE bid_documents_id = %s RETURNING *;
        """

    values = (
        bid_document_data.submit_to_customer,
        bid_document_data.assigned_to,
        bid_document_data.submitted_to,
        bid_document_data.title,
        bid_document_data.reference_num,
        bid_document_data.document_type,
        bid_document_data.request_revision,
        bid_document_data.status,
        bid_document_data.comment,
        bid_documents_id
    )

    cursor.execute(query, values)
    updated_bid_document = cursor.fetchone()

    query = """
        UPDATE bid_documents_acknowledgement SET 
            acknowledged_by = %s,
            acknowledgement_date = %s,
            acknowledgement_comment = %s,
            acknowledged = %s,
            acknowledgement_document = %s,
            acknowledgement_submitted_on = %s
        WHERE bid_documents_id = %s RETURNING *;
        """
    
    values = (
        bid_document_data.acknowledged_by,
        bid_document_data.acknowledgement_date,
        bid_document_data.acknowledgement_comment,
        bid_document_data.acknowledged,
        bid_document_data.acknowledgement_document,
        bid_document_data.acknowledgement_submitted_on,
        bid_documents_id
    )

    cursor.execute(query, values)
    updated_bid_acknowledgement = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_document:
        return BidDocuments(
            bid_documents_id=updated_bid_document[0],
            rfx_id=updated_bid_document[1],
            submit_to_customer=updated_bid_document[2],
            assigned_to=updated_bid_document[3],
            submitted_to=updated_bid_document[4],
            title=updated_bid_document[5],
            reference_num=updated_bid_document[6],
            document_type=updated_bid_document[7],
            request_revision=updated_bid_document[8],
            status=updated_bid_document[9],
            comment=updated_bid_document[10],
            # acknowledgement
            acknowledged_by=updated_bid_acknowledgement[3],
            acknowledgement_date=updated_bid_acknowledgement[4],
            acknowledgement_comment=updated_bid_acknowledgement[5],
            acknowledged=updated_bid_acknowledgement[6],
            acknowledgement_document=updated_bid_acknowledgement[7],
            acknowledgement_submitted_on=updated_bid_acknowledgement[8]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Document update failed")


def delete_bid_document(bid_documents_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "DELETE FROM bid_documents_acknowledgement WHERE bid_documents_id = %s RETURNING bid_documents_id;"
        cursor.execute(query, (bid_documents_id,))
        deleted_bid_document = cursor.fetchone()
    except:
        None
        
    query = "DELETE FROM bid_documents WHERE bid_documents_id = %s RETURNING bid_documents_id;"
    cursor.execute(query, (bid_documents_id,))
    deleted_bid_document = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_bid_document:
        return True
    else:
        return False


def get_bid_document_by_title(rfx_id: int, title: str) -> Optional[BidDocuments]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*, 
            a.acknowledged_by, a.acknowledgement_date, a.acknowledgement_comment,            
            a.acknowledged, a.acknowledgement_document, a.acknowledgement_submitted_on
            FROM bid_documents b
            INNER JOIN bid_documents_acknowledgement a ON a.bid_documents_id=b.bid_documents_id 
        WHERE a.rfx_id =%s AND lower(b.title) = %s;
        """
    cursor.execute(query, (rfx_id, title.lower()))
    bid_document = cursor.fetchone()

    conn.close()

    if bid_document:
        return BidDocuments(
            bid_documents_id=bid_document[0],
            rfx_id=bid_document[1],
            submit_to_customer=bid_document[2],
            assigned_to=bid_document[3],
            submitted_to=bid_document[4],
            title=bid_document[5],
            reference_num=bid_document[6],
            document_type=bid_document[7],
            request_revision=bid_document[8],
            status=bid_document[9],
            comment=bid_document[10],
            # acknowledgement
            acknowledged_by=bid_document[11],
            acknowledgement_date=bid_document[12],
            acknowledgement_comment=bid_document[13],
            acknowledged=bid_document[14],
            acknowledgement_document=bid_document[15],
            acknowledgement_submitted_on=bid_document[16]
        )
    else:
        return None
    
    
def get_bid_document_by_status(rfx_id: int, status: str) -> List[BidDocuments]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*, 
            a.acknowledged_by, a.acknowledgement_date, a.acknowledgement_comment,            
            a.acknowledged, a.acknowledgement_document, a.acknowledgement_submitted_on
            FROM bid_documents b
            INNER JOIN bid_documents_acknowledgement a ON a.bid_documents_id=b.bid_documents_id 
        WHERE a.rfx_id = %s AND lower(b.status) = %s;
        """
    cursor.execute(query, (rfx_id, status.lower()))
    bid_document = cursor.fetchall()

    conn.close()

    return[
        BidDocuments(
            bid_documents_id=row[0],
            rfx_id=row[1],
            submit_to_customer=row[2],
            assigned_to=row[3],
            submitted_to=row[4],
            title=row[5],
            reference_num=row[6],
            document_type=row[7],
            request_revision=row[8],
            status=row[9],
            comment=row[10],
            # acknowledgement
            acknowledged_by=row[11],
            acknowledgement_date=row[12],
            acknowledgement_comment=row[13],
            acknowledged=row[14],
            acknowledgement_document=row[15],
            acknowledgement_submitted_on=row[16]
        ) 
        for row in bid_document
    ]