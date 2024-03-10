from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from review_templates.schemas import ReviewTemplatesCreate, ReviewTemplates

def create_review_templates(item_form_data: ReviewTemplatesCreate) -> ReviewTemplates:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO review_templates(
        tenant_id,
        parent_id,
        child_id,
        item_title,
        item_type,
        item_value,
        item_checked,
        item_status,
        is_active
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        item_form_data.tenant_id,
        item_form_data.parent_id,
        item_form_data.child_id,
        item_form_data.item_title,
        item_form_data.item_type,
        item_form_data.item_value,
        item_form_data.item_checked,
        item_form_data.item_status,
        item_form_data.is_active
    )

    cursor.execute(query, values)
    new_item = cursor.fetchone()
         
    conn.commit()
    conn.close()

    if new_item:
        return ReviewTemplates(
            review_templates_id=new_item[0],
            tenant_id=new_item[1],
            parent_id=new_item[2],
            child_id=new_item[3],
            item_title=new_item[4],
            item_type=new_item[5],
            item_value=new_item[6],
            item_checked=new_item[7],
            item_status=new_item[8],
            is_active=new_item[9]
            )
    else:
        raise HTTPException(status_code=404, detail="Review Templates creation failed")


def get_all_review_templates(tenant_id: int) -> List[ReviewTemplates]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM review_templates            
        WHERE tenant_id = %s ;
        """

    cursor.execute(query,(tenant_id, ))
    query_all_items = cursor.fetchall()

    conn.close()
    if query_all_items:
        return [
            ReviewTemplates(
            review_templates_id=row[0],
            tenant_id=row[1],
            parent_id=row[2],
            child_id=row[3],
            item_title=row[4],
            item_type=row[5],
            item_value=row[6],
            item_checked=row[7],
            item_status=row[8],
            is_active=row[9]
            )
            for row in query_all_items
        ]
    else:
        None

def update_review_templates(review_templates_id: int , item_form_data: ReviewTemplatesCreate) -> Optional[ReviewTemplates]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE review_templates SET
        item_title = %s,
        item_type = %s,
        item_value = %s,
        item_checked = %s,
        item_status = %s,
        is_active = %s
    WHERE review_templates_id = %s RETURNING *;
    """

    values = (
        item_form_data.item_title,
        item_form_data.item_type,
        item_form_data.item_value,
        item_form_data.item_checked,
        item_form_data.item_status,
        item_form_data.is_active,
        review_templates_id
    )
    
    cursor.execute(query, values)
    new_item = cursor.fetchone()

   
    conn.commit()
    conn.close()

    if new_item:
        return ReviewTemplates(
            review_templates_id=new_item[0],
            tenant_id=new_item[1],
            parent_id=new_item[2],
            child_id=new_item[3],
            item_title=new_item[4],
            item_type=new_item[5],
            item_value=new_item[6],
            item_checked=new_item[7],
            item_status=new_item[8],
            is_active=new_item[9]
            )
    else:
        raise HTTPException(status_code=404, detail="Review Templates update failed")


def delete_review_templates(review_templates_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM review_templates WHERE review_templates_id = %s RETURNING review_templates_id;"
    cursor.execute(query, (review_templates_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False


def get_review_templates_by_id(review_templates_id: int) -> Optional[ReviewTemplates]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM review_templates WHERE review_templates_id = %s;
        """

    cursor.execute(query, (review_templates_id,))
    new_item = cursor.fetchone()

    conn.close()

    if new_item:
        return ReviewTemplates(
            review_templates_id=new_item[0],
            tenant_id=new_item[1],
            parent_id=new_item[2],
            child_id=new_item[3],
            item_title=new_item[4],
            item_type=new_item[5],
            item_value=new_item[6],
            item_checked=new_item[7],
            item_status=new_item[8],
            is_active=new_item[9]
            )
        
    else:
        return None

def get_all_review_templates_by_active(tenant_id: int) -> List[ReviewTemplates]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM review_templates            
        WHERE tenant_id = %s AND is_active = %s ;
        """

    cursor.execute(query,(tenant_id, True))
    query_all_items = cursor.fetchall()

    conn.close()
    if query_all_items:
        return [
            ReviewTemplates(
            review_templates_id=row[0],
            tenant_id=row[1],
            parent_id=row[2],
            child_id=row[3],
            item_title=row[4],
            item_type=row[5],
            item_value=row[6],
            item_checked=row[7],
            item_status=row[8],
            is_active=row[9]
            )
            for row in query_all_items
        ]
    else:
        None
