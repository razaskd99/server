from typing import Optional, List
from fastapi import HTTPException
from datetime import datetime
from db.connection import get_db_connection
from rfx_clarification_post.schemas import RfxClarificationPost, RfxClarificationPostCreate, RfxClarificationPostGetOneRecord


def create_rfx_clarification_post(post_data: RfxClarificationPostCreate) -> RfxClarificationPostGetOneRecord:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO rfx_clarification_post (rfx_clarification_id, posted_by, post_number, posted_on, title, comment, parent_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING *;
    """

    values = (
        post_data.rfx_clarification_id,
        post_data.posted_by,
        post_data.post_number,
        post_data.posted_on,
        post_data.title,
        post_data.comment,
        post_data.parent_id
    )

    cursor.execute(query, values)
    new_post = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_post:
        return RfxClarificationPostGetOneRecord(
            rfx_clarification_post_id=new_post[0],
            rfx_clarification_id=new_post[1],
            posted_by=new_post[2],
            post_number=new_post[3],
            posted_on=new_post[4],
            title=new_post[5],
            comment=new_post[6],
            parent_id=new_post[7]
        )
    else:
        raise HTTPException(status_code=404, detail="Rfx Clarification Post creation failed")

def get_all_rfx_clarification_posts(rfx_clarification_id: int) -> List[RfxClarificationPost]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT c.*, 
            u.first_name, u.middle_name, u.last_name, u.user_profile_photo
            FROM rfx_clarification_post c
            LEFT JOIN users u ON u.user_id=c.posted_by   
        WHERE c.rfx_clarification_id = %s;
        """
    cursor.execute(query, (rfx_clarification_id,))
    posts = cursor.fetchall()

    conn.close()

    return [
        RfxClarificationPost(
            rfx_clarification_post_id=row[0],
            rfx_clarification_id=row[1],
            posted_by=row[2],
            post_number=row[3],
            posted_on=row[4],
            title=row[5],
            comment=row[6],
            parent_id=row[7],
            first_name=row[8],
            middle_name=row[9],
            last_name=row[10],
            user_profile_photo=row[11]
        )
        for row in posts
    ]


def get_rfx_clarification_post_by_id(post_id: int) -> Optional[RfxClarificationPost]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT c.*, 
            u.first_name, u.middle_name, u.last_name, u.user_profile_photo
            FROM rfx_clarification_post c
            LEFT JOIN users u ON u.user_id=c.posted_by  
        WHERE c.rfx_clarification_post_id = %s;
        """
    cursor.execute(query, (post_id,))
    post = cursor.fetchone()

    conn.close()

    if post:
        return RfxClarificationPost(
            rfx_clarification_post_id=post[0],
            rfx_clarification_id=post[1],
            posted_by=post[2],
            post_number=post[3],
            posted_on=post[4],
            title=post[5],
            comment=post[6],
            parent_id=post[7],
            first_name=post[8],
            middle_name=post[9],
            last_name=post[10],
            user_profile_photo=post[11]
        )
    else:
        return None

    
def update_rfx_clarification_post(post_id: int, post_data: RfxClarificationPostCreate) -> Optional[RfxClarificationPostGetOneRecord]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE rfx_clarification_post
        SET rfx_clarification_id = %s,
            posted_by = %s,
            post_number = %s,
            posted_on = %s,
            title = %s,
            comment = %s
        WHERE rfx_clarification_post_id = %s
        RETURNING *;
        """

    values = (
        post_data.rfx_clarification_id,
        post_data.posted_by,
        post_data.post_number,
        post_data.posted_on,
        post_data.title,
        post_data.comment,
        post_id,
    )

    cursor.execute(query, values)
    updated_post = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_post:
        return RfxClarificationPostGetOneRecord(
            rfx_clarification_post_id=updated_post[0],
            rfx_clarification_id=updated_post[1],
            posted_by=updated_post[2],
            post_number=updated_post[3],
            posted_on=updated_post[4],
            title=updated_post[5],
            comment=updated_post[6],
            parent_id=updated_post[7]
        )
    else:
        raise HTTPException(status_code=404, detail="Rfx Clarification Post update failed")   
    
    
def delete_rfx_clarification_post(post_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "DELETE FROM rfx_clarification_meta WHERE rfx_clarification_meta_id = %s RETURNING rfx_clarification_meta_id;"
        cursor.execute(query, (post_id,))
        deleted_meta = cursor.fetchone()
    except:
        None
        
    query = "DELETE FROM rfx_clarification_post WHERE rfx_clarification_post_id = %s RETURNING rfx_clarification_post_id;"
    cursor.execute(query, (post_id,))
    deleted_post = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_post:
        return True
    else:
        return False

 