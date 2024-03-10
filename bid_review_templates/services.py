from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from bid_review_templates.schemas import BidReviewTemplateCreate, BidReviewTemplate


def create_bid_review_templates(bid_review_template_data: BidReviewTemplateCreate) -> BidReviewTemplate:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_review_templates (
        tenant_id,
        template_title,
        template_description,
        reference_number,
        template_data,
        template_key,
        required,
        is_active
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_review_template_data.tenant_id,
        bid_review_template_data.template_title,
        bid_review_template_data.template_description,
        bid_review_template_data.reference_number,
        bid_review_template_data.template_data,
        bid_review_template_data.template_key,
        bid_review_template_data.required,
        bid_review_template_data.is_active
    )

    cursor.execute(query, values)
    new_bid_review_template = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if new_bid_review_template:
        return BidReviewTemplate(
            bid_review_templates_id=new_bid_review_template[0],
            tenant_id=new_bid_review_template[1],
            template_title=new_bid_review_template[2],
            template_description=new_bid_review_template[3],
            reference_number=new_bid_review_template[4],
            template_data=new_bid_review_template[5],
            template_key=new_bid_review_template[6],
            required=new_bid_review_template[7],
            is_active=new_bid_review_template[8]           
        )
    else:
        raise HTTPException(status_code=404, detail="Bid review template Detail creation failed")


def get_all_bid_review_templates(tenant_id: int) -> List[BidReviewTemplate]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bid_review_templates WHERE tenant_id = %s;
        """

    cursor.execute(query,(tenant_id,))
    bid_review_template = cursor.fetchall()

    conn.close()
    if bid_review_template:
        return [
            BidReviewTemplate(
                bid_review_templates_id=row[0],
                tenant_id=row[1],
                template_title=row[2],
                template_description=row[3],
                reference_number=row[4],
                template_data=row[5],
                template_key=row[6],
                required=row[7],
                is_active=row[8]                
            )
            for row in bid_review_template
        ]
    else:
        None


def update_bid_review_templates(bid_review_templates_id: int, bid_review_template_data: BidReviewTemplateCreate) -> Optional[BidReviewTemplate]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_review_templates SET 
        template_title = %s,
        template_description = %s,
        reference_number = %s,
        template_data = %s,
        template_key = %s,
        required = %s,
        is_active = %s
    WHERE bid_review_templates_id = %s RETURNING *;
    """

    values = (
        bid_review_template_data.template_title,
        bid_review_template_data.template_description,
        bid_review_template_data.reference_number,
        bid_review_template_data.template_data,
        bid_review_template_data.template_key,
        bid_review_template_data.required,
        bid_review_template_data.is_active,
        bid_review_templates_id
    )

    cursor.execute(query, values)
    updated_bid_review_template = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_review_template:
        return BidReviewTemplate(            
            bid_review_templates_id=updated_bid_review_template[0],
            tenant_id=updated_bid_review_template[1],
            template_title=updated_bid_review_template[2],
            template_description=updated_bid_review_template[3],
            reference_number=updated_bid_review_template[4],
            template_data=updated_bid_review_template[5],
            template_key=updated_bid_review_template[6],
            required=updated_bid_review_template[7],
            is_active=updated_bid_review_template[8]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Review template update failed")


def delete_bid_review_templates(bid_review_templates_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "DELETE FROM bid_review_templates WHERE bid_review_templates_id = %s RETURNING bid_review_templates_id;"
    cursor.execute(query, (bid_review_templates_id,))
    deleted_bid_review_template = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if deleted_bid_review_template:
        return True
    else:
        return False


def get_bid_review_templates_by_id(bid_review_templates_id: int) -> Optional[BidReviewTemplate]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bid_review_templates WHERE bid_review_templates_id = %s;
        """
    cursor.execute(query, (bid_review_templates_id,))
    bid_review_template = cursor.fetchone()

    conn.close()

    if bid_review_template:
        return BidReviewTemplate (
                bid_review_templates_id=bid_review_template[0],
                tenant_id=bid_review_template[1],
                template_title=bid_review_template[2],
                template_description=bid_review_template[3],
                reference_number=bid_review_template[4],
                template_data=bid_review_template[5],
                template_key=bid_review_template[6],
                required=bid_review_template[7],
                is_active=bid_review_template[8]    
            )
    
    else:
        return None

def get_bid_review_templates_by_title(tenant_id: int, template_title: str) -> Optional[BidReviewTemplate]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bid_review_templates WHERE tenant_id = %s AND lower(template_title) = %s;
        """
    cursor.execute(query, (tenant_id,template_title.lower()))
    bid_review_template = cursor.fetchone()

    conn.close()

    if bid_review_template:
        return BidReviewTemplate (
                bid_review_templates_id=bid_review_template[0],
                tenant_id=bid_review_template[1],
                template_title=bid_review_template[2],
                template_description=bid_review_template[3],
                reference_number=bid_review_template[4],
                template_data=bid_review_template[5],
                template_key=bid_review_template[6],
                required=bid_review_template[7],
                is_active=bid_review_template[8]    
            )
    
    else:
        return None


def get_bid_review_templates_by_reference_num(tenant_id: int, reference_number: str) -> Optional[BidReviewTemplate]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bid_review_templates WHERE tenant_id = %s AND lower(reference_number) = %s;
        """
    cursor.execute(query, (tenant_id,reference_number.lower()))
    bid_review_template = cursor.fetchone()

    conn.close()

    if bid_review_template:
        return BidReviewTemplate (
                bid_review_templates_id=bid_review_template[0],
                tenant_id=bid_review_template[1],
                template_title=bid_review_template[2],
                template_description=bid_review_template[3],
                reference_number=bid_review_template[4],
                template_data=bid_review_template[5],
                template_key=bid_review_template[6],
                required=bid_review_template[7],
                is_active=bid_review_template[8]    
            )
    
    else:
        return None

