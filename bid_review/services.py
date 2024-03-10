from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from bid_review.schemas import BidReviewCreate, BidReview, BidReviewUpdateScore, BidReviewUpdateStatus, BidReviewUpdateTemplate, BidReviewGet


def create_bid_review(item_form_data: BidReviewCreate) -> BidReview:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO bid_review (
        	rfx_id,
            bid_review_templates_id,
            template_data,
            review_Key,
            score_value,
            score_name,
            score_description,
            issued_date,
            due_date,
            status,
            skip_review,
            skip_reason,
            required_revision,
            review_approved,
            review_approved_notes,
            review_declined,
            review_declined_notes,
            review_revison,
            review_revison_notes,
            created_at,
            updated_at,
            temp_title,
            temp_ref_number
            
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        item_form_data.rfx_id,
        item_form_data.bid_review_templates_id,
        item_form_data.template_data,
        item_form_data.review_Key,
        item_form_data.score_value,
        item_form_data.score_name,
        item_form_data.score_description,
        item_form_data.issued_date,
        item_form_data.due_date,
        item_form_data.status,
        item_form_data.skip_review,
        item_form_data.skip_reason,
        item_form_data.required_revision,
        item_form_data.review_approved,
        item_form_data.review_approved_notes,
        item_form_data.review_declined,
        item_form_data.review_declined_notes,
        item_form_data.review_revison,
        item_form_data.review_revison_notes,
        item_form_data.created_at,
        item_form_data.updated_at,
        item_form_data.temp_title,
        item_form_data.temp_ref_number
    )

    cursor.execute(query, values)
    new_item = cursor.fetchone()
   
    conn.commit()
    conn.close()

    if new_item:
        return BidReview(
            bid_review_id=new_item[0],
            rfx_id=new_item[1],
            bid_review_templates_id=new_item[2],
            template_data=new_item[3],
            review_Key=new_item[4],
            score_value=new_item[5],
            score_name=new_item[6],
            score_description=new_item[7],
            issued_date=new_item[8],
            due_date=new_item[9],
            status=new_item[10],
            skip_review=new_item[11],
            skip_reason=new_item[12],
            required_revision=new_item[13],
            review_approved=new_item[14],
            review_approved_notes=new_item[15],
            review_declined=new_item[16],
            review_declined_notes=new_item[17],
            review_revison=new_item[18],
            review_revison_notes=new_item[19],
            created_at=new_item[20],
            updated_at=new_item[21],
            temp_title=new_item[22],
            temp_ref_number=new_item[23]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Review Detail creation failed")


def get_all_bid_review(rfx_id: int) -> List[BidReviewGet]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*,
            t.template_data AS template_data_main
            FROM bid_review b 
            LEFT JOIN bid_review_templates t ON t.bid_review_templates_id = b.bid_review_templates_id              
        WHERE b.rfx_id = %s 
        c;
        """

    cursor.execute(query,(rfx_id, ))
    query_all_items = cursor.fetchall()

    conn.close()
    
    if query_all_items:
        return [
            BidReviewGet(
                bid_review_id=row[0],
                rfx_id=row[1],
                bid_review_templates_id=row[2],
                template_data=row[3],
                review_Key=row[4],
                score_value=row[5],
                score_name=row[6],
                score_description=row[7],
                issued_date=row[8],
                due_date=row[9],
                status=row[10],
                skip_review=row[11],
                skip_reason=row[12],
                required_revision=row[13],
                review_approved=row[14],
                review_approved_notes=row[15],
                review_declined=row[16],
                review_declined_notes=row[17],
                review_revison=row[18],
                review_revison_notes=row[19],
                created_at=row[20],
                updated_at=row[21],
                temp_title=row[22],
                temp_ref_number=row[23],
                template_data_main=row[24]
            )
            for row in query_all_items
        ]
    else:
        return []


def update_bid_review(bid_review_id: int,  item_form_data: BidReviewCreate) -> Optional[BidReview]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_review SET 
        template_data = %s,
        score_value = %s,
        score_name = %s,
        score_description = %s,
        status = %s,
        required_revision = %s,
        review_approved = %s,
        review_approved_notes = %s,
        review_declined = %s,
        review_declined_notes = %s,
        review_revison = %s,
        review_revison_notes = %s,
        updated_at = %s,
        temp_title = %s,
        temp_ref_number = %s      
    WHERE bid_review_id = %s RETURNING *;
    """

    values = (
        item_form_data.template_data,
        item_form_data.score_value,
        item_form_data.score_name,
        item_form_data.score_description,
        item_form_data.status,
        item_form_data.required_revision,
        item_form_data.review_approved,
        item_form_data.review_approved_notes,
        item_form_data.review_declined,
        item_form_data.review_declined_notes,
        item_form_data.review_revison,
        item_form_data.review_revison_notes,
        item_form_data.updated_at,
        item_form_data.temp_title,
        item_form_data.temp_ref_number,
        bid_review_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return BidReview(
            bid_review_id=updated_itemm[0],
            rfx_id=updated_itemm[1],
            bid_review_templates_id=updated_itemm[2],
            template_data=updated_itemm[3],
            review_Key=updated_itemm[4],
            score_value=updated_itemm[5],
            score_name=updated_itemm[6],
            score_description=updated_itemm[7],
            issued_date=updated_itemm[8],
            due_date=updated_itemm[9],
            status=updated_itemm[10],
            skip_review=updated_itemm[11],
            skip_reason=updated_itemm[12],
            required_revision=updated_itemm[13],
            review_approved=updated_itemm[14],
            review_approved_notes=updated_itemm[15],
            review_declined=updated_itemm[16],
            review_declined_notes=updated_itemm[17],
            review_revison=updated_itemm[18],
            review_revison_notes=updated_itemm[19],
            created_at=updated_itemm[20],
            updated_at=updated_itemm[21],
            temp_title=updated_itemm[22],
            temp_ref_number=updated_itemm[23]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Review update failed")


def update_bid_review_template_data(bid_review_id: int,  item_form_data: BidReviewUpdateTemplate) -> Optional[BidReview]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_review SET 
        template_data = %s        
    WHERE bid_review_id = %s RETURNING *;
    """

    values = (
        item_form_data.template_data,
        bid_review_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return BidReview(
            bid_review_id=updated_itemm[0],
            rfx_id=updated_itemm[1],
            bid_review_templates_id=updated_itemm[2],
            template_data=updated_itemm[3],
            review_Key=updated_itemm[4],
            score_value=updated_itemm[5],
            score_name=updated_itemm[6],
            score_description=updated_itemm[7],
            issued_date=updated_itemm[8],
            due_date=updated_itemm[9],
            status=updated_itemm[10],
            skip_review=updated_itemm[11],
            skip_reason=updated_itemm[12],
            required_revision=updated_itemm[13],
            review_approved=updated_itemm[14],
            review_approved_notes=updated_itemm[15],
            review_declined=updated_itemm[16],
            review_declined_notes=updated_itemm[17],
            review_revison=updated_itemm[18],
            review_revison_notes=updated_itemm[19],
            created_at=updated_itemm[20],
            updated_at=updated_itemm[21],
            temp_title=updated_itemm[22],
            temp_ref_number=updated_itemm[23]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Review update failed")


def update_bid_review_status(bid_review_id: int,  item_form_data: BidReviewUpdateStatus) -> Optional[BidReview]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_review SET 
        status = %s,       
        updated_at = %s        
    WHERE bid_review_id = %s RETURNING *;
    """

    values = (
        item_form_data.status,
        item_form_data.updated_at,
        bid_review_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return BidReview(
            bid_review_id=updated_itemm[0],
            rfx_id=updated_itemm[1],
            bid_review_templates_id=updated_itemm[2],
            template_data=updated_itemm[3],
            review_Key=updated_itemm[4],
            score_value=updated_itemm[5],
            score_name=updated_itemm[6],
            score_description=updated_itemm[7],
            issued_date=updated_itemm[8],
            due_date=updated_itemm[9],
            status=updated_itemm[10],
            skip_review=updated_itemm[11],
            skip_reason=updated_itemm[12],
            required_revision=updated_itemm[13],
            review_approved=updated_itemm[14],
            review_approved_notes=updated_itemm[15],
            review_declined=updated_itemm[16],
            review_declined_notes=updated_itemm[17],
            review_revison=updated_itemm[18],
            review_revison_notes=updated_itemm[19],
            created_at=updated_itemm[20],
            updated_at=updated_itemm[21],
            temp_title=updated_itemm[22],
            temp_ref_number=updated_itemm[23]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Review update failed")


def update_bid_review_score(bid_review_id: int,  item_form_data: BidReviewUpdateScore) -> Optional[BidReview]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_review SET 
        score_value = %s,       
        score_name = %s,
        score_description = %s,
        updated_at = %s        
    WHERE bid_review_id = %s RETURNING *;
    """

    values = (
        item_form_data.score_value,
        item_form_data.score_name,
        item_form_data.score_description,
        item_form_data.updated_at,
        bid_review_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return BidReview(
            bid_review_id=updated_itemm[0],
            rfx_id=updated_itemm[1],
            bid_review_templates_id=updated_itemm[2],
            template_data=updated_itemm[3],
            review_Key=updated_itemm[4],
            score_value=updated_itemm[5],
            score_name=updated_itemm[6],
            score_description=updated_itemm[7],
            issued_date=updated_itemm[8],
            due_date=updated_itemm[9],
            status=updated_itemm[10],
            skip_review=updated_itemm[11],
            skip_reason=updated_itemm[12],
            required_revision=updated_itemm[13],
            review_approved=updated_itemm[14],
            review_approved_notes=updated_itemm[15],
            review_declined=updated_itemm[16],
            review_declined_notes=updated_itemm[17],
            review_revison=updated_itemm[18],
            review_revison_notes=updated_itemm[19],
            created_at=updated_itemm[20],
            updated_at=updated_itemm[21],
            temp_title=updated_itemm[22],
            temp_ref_number=updated_itemm[23]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Review update failed")


def delete_bid_review(bid_review_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM bid_review WHERE bid_review_id = %s RETURNING bid_review_id;"
    cursor.execute(query, (bid_review_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False


def get_bid_review_by_id(bid_review_id: int) -> Optional[BidReviewGet]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*,
            t.template_data AS template_data_main
            FROM bid_review b 
            LEFT JOIN bid_review_templates t ON t.bid_review_templates_id = b.bid_review_templates_id              
        WHERE b.bid_review_id = %s ;
        """

    cursor.execute(query, (bid_review_id,))
    get_all_items = cursor.fetchone()

    conn.close()

    if get_all_items:
        return BidReviewGet(
                bid_review_id=get_all_items[0],
                rfx_id=get_all_items[1],
                bid_review_templates_id=get_all_items[2],
                template_data=get_all_items[3],
                review_Key=get_all_items[4],
                score_value=get_all_items[5],
                score_name=get_all_items[6],
                score_description=get_all_items[7],
                issued_date=get_all_items[8],
                due_date=get_all_items[9],
                status=get_all_items[10],
                skip_review=get_all_items[11],
                skip_reason=get_all_items[12],
                required_revision=get_all_items[13],
                review_approved=get_all_items[14],
                review_approved_notes=get_all_items[15],
                review_declined=get_all_items[16],
                review_declined_notes=get_all_items[17],
                review_revison=get_all_items[18],
                review_revison_notes=get_all_items[19],
                created_at=get_all_items[20],
                updated_at=get_all_items[21],
                temp_title=get_all_items[22],
                temp_ref_number=get_all_items[23],
                template_data_main=get_all_items[24]
            )
    else:
        return None


def get_bid_review_by_key(rfx_id : int, review_key: str) -> List[BidReviewGet]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*,
            t.template_data AS template_data_main
            FROM bid_review b 
            LEFT JOIN bid_review_templates t ON t.bid_review_templates_id = b.bid_review_templates_id              
        WHERE lower(b.review_key) = %s AND b.rfx_id = %s 
        ORDER BY b.created_at DESC;
        """

    cursor.execute(query, (review_key.lower(), rfx_id))
    get_items = cursor.fetchall()

    conn.close()

    if get_items:
        return [
                BidReviewGet(
                bid_review_id=row[0],
                rfx_id=row[1],
                bid_review_templates_id=row[2],
                template_data=row[3],
                review_Key=row[4],
                score_value=row[5],
                score_name=row[6],
                score_description=row[7],
                issued_date=row[8],
                due_date=row[9],
                status=row[10],
                skip_review=row[11],
                skip_reason=row[12],
                required_revision=row[13],
                review_approved=row[14],
                review_approved_notes=row[15],
                review_declined=row[16],
                review_declined_notes=row[17],
                review_revison=row[18],
                review_revison_notes=row[19],
                created_at=row[20],
                updated_at=row[21],
                temp_title=row[22],
                temp_ref_number=row[23],
                template_data_main=row[24]
            )
            for row in get_items
            ]
    else:
        return None
    

def get_all_bid_review_by_status( rfx_id: int, status: str) -> List[BidReviewGet]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*,
            t.template_data AS template_data_main
            FROM bid_review b 
            LEFT JOIN bid_review_templates t ON t.bid_review_templates_id = b.bid_review_templates_id              
        WHERE lower(b.status) = %s AND b.rfx_id = %s ;
        """

    cursor.execute(query, (status.lower(), rfx_id,))
    all_records = cursor.fetchall()

    conn.close()
    if all_records:
        return [
            BidReviewGet(
                bid_review_id=row[0],
                rfx_id=row[1],
                bid_review_templates_id=row[2],
                template_data=row[3],
                review_Key=row[4],
                score_value=row[5],
                score_name=row[6],
                score_description=row[7],
                issued_date=row[8],
                due_date=row[9],
                status=row[10],
                skip_review=row[11],
                skip_reason=row[12],
                required_revision=row[13],
                review_approved=row[14],
                review_approved_notes=row[15],
                review_declined=row[16],
                review_declined_notes=row[17],
                review_revison=row[18],
                review_revison_notes=row[19],
                created_at=row[20],
                updated_at=row[21],
                temp_title=row[22],
                temp_ref_number=row[23],
                template_data_main=row[24]
            )
            for row in all_records
        ]
    else:
        return None
    


