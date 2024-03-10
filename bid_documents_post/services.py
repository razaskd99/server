from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import BidDocumentsPostCreate, BidDocumentsPost
from datetime import datetime


def create_bid_document_post(bid_document_post_data: BidDocumentsPostCreate) -> BidDocumentsPost:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_documents_post (
        bid_documents_id,
        posted_by,
        post_number,
        posted_on,
        title,
        comment
    ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_document_post_data.bid_documents_id,
        bid_document_post_data.posted_by,
        bid_document_post_data.post_number,
        bid_document_post_data.posted_on,
        bid_document_post_data.title,
        bid_document_post_data.comment
    )

    cursor.execute(query, values)
    new_bid_document_post = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_bid_document_post:
        return BidDocumentsPost(
            bid_documents_post_id=new_bid_document_post[0],
            bid_documents_id=new_bid_document_post[1],
            posted_by=new_bid_document_post[2],
            post_number=new_bid_document_post[3],
            posted_on=new_bid_document_post[4],
            title=new_bid_document_post[5],
            comment=new_bid_document_post[6]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Documents Post creation failed")


def get_all_bid_document_posts(bid_documents_id: int) -> List[BidDocumentsPost]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_documents_post WHERE bid_documents_id = %s;"
    cursor.execute(query, (bid_documents_id,))
    bid_document_posts = cursor.fetchall()

    conn.close()

    return [
        BidDocumentsPost(
            bid_documents_post_id=row[0],
            bid_documents_id=row[1],
            posted_by=row[2],
            post_number=row[3],
            posted_on=row[4],
            title=row[5],
            comment=row[6]
        )
        for row in bid_document_posts
    ]


def update_bid_document_post(bid_documents_post_id: int, bid_document_post_data: BidDocumentsPostCreate) -> BidDocumentsPost:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE bid_documents_post SET 
            posted_by = %s,
            post_number = %s,
            posted_on = %s,
            title = %s,
            comment = %s
        WHERE bid_documents_post_id = %s RETURNING *;
        """

    values = (
        bid_document_post_data.posted_by,
        bid_document_post_data.post_number,
        bid_document_post_data.posted_on,
        bid_document_post_data.title,
        bid_document_post_data.comment,
        bid_documents_post_id
    )

    cursor.execute(query, values)
    updated_bid_document_post = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_document_post:
        return BidDocumentsPost(
            bid_documents_post_id=updated_bid_document_post[0],
            bid_documents_id=updated_bid_document_post[1],
            posted_by=updated_bid_document_post[2],
            post_number=updated_bid_document_post[3],
            posted_on=updated_bid_document_post[4],
            title=updated_bid_document_post[5],
            comment=updated_bid_document_post[6]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Documents Post update failed")


def delete_bid_document_post(bid_documents_post_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "DELETE FROM bid_documents_meta WHERE bid_documents_post_id = %s RETURNING bid_documents_post_id;"
        cursor.execute(query, (bid_documents_post_id,))
        deleted_bid_document_meta = cursor.fetchone()
    except:
        None
        
    query = "DELETE FROM bid_documents_post WHERE bid_documents_post_id = %s RETURNING bid_documents_post_id;"
    cursor.execute(query, (bid_documents_post_id,))
    deleted_bid_document_post = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_bid_document_post:
        return True
    else:
        return False


def get_bid_document_post_by_id(bid_documents_post_id: int) -> Optional[BidDocumentsPost]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_documents_post WHERE bid_documents_post_id = %s;"
    cursor.execute(query, (bid_documents_post_id,))
    bid_document_post = cursor.fetchone()

    conn.close()

    if bid_document_post:
        return BidDocumentsPost(
            bid_documents_post_id=bid_document_post[0],
            bid_documents_id=bid_document_post[1],
            posted_by=bid_document_post[2],
            post_number=bid_document_post[3],
            posted_on=bid_document_post[4],
            title=bid_document_post[5],
            comment=bid_document_post[6]
        )
    else:
        return None


def get_bid_document_post_by_title(bid_documents_post_id: int, title: str) -> Optional[BidDocumentsPost]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_documents_post WHERE bid_documents_post_id = %s AND lower(title) = %s;"
    cursor.execute(query, (bid_documents_post_id, title.lower()))
    bid_document_post = cursor.fetchone()

    conn.close()

    if bid_document_post:
        return BidDocumentsPost(
            bid_documents_post_id=bid_document_post[0],
            bid_documents_id=bid_document_post[1],
            posted_by=bid_document_post[2],
            post_number=bid_document_post[3],
            posted_on=bid_document_post[4],
            title=bid_document_post[5],
            comment=bid_document_post[6]
        )
    else:
        return None
