from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from datetime import date
from .schemas import BidOrderPostCreate, BidOrderPost, BidOrderPostGetOneRecord

# Create a Bid Order Post
def create_bid_order_post(bid_order_post_data: BidOrderPostCreate) -> BidOrderPostGetOneRecord:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_order_post (bid_order_id, posted_by, post_number, posted_on, title, comment, parent_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_order_post_data.bid_order_id,
        bid_order_post_data.posted_by,
        bid_order_post_data.post_number,
        bid_order_post_data.posted_on,
        bid_order_post_data.title,
        bid_order_post_data.comment,
        bid_order_post_data.parent_id

    )

    cursor.execute(query, values)
    new_bid_order_post = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_bid_order_post:
        return BidOrderPostGetOneRecord(
            bid_order_post_id=new_bid_order_post[0],
            bid_order_id=new_bid_order_post[1],
            posted_by=new_bid_order_post[2],
            post_number=new_bid_order_post[3],
            posted_on=new_bid_order_post[4],
            title=new_bid_order_post[5],
            comment=new_bid_order_post[6],
            parent_id=new_bid_order_post[7]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Order Post creation failed")

# Get all Bid Order Posts
def get_all_bid_order_posts(bid_order_id: int) -> List[BidOrderPost]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*, 
            u.first_name, u.middle_name, u.last_name, u.user_profile_photo,
            t.team_role,
            d.title AS designation_title
            FROM bid_order_post b
            LEFT JOIN users u ON u.user_id=b.posted_by   
            LEFT JOIN designation d ON d.designation_id = u.designation_id 
            LEFT JOIN team t ON t.team_id = u.team_id
        WHERE b.bid_order_id = %s;
        """
    cursor.execute(query,(bid_order_id,))
    bid_order_posts = cursor.fetchall()

    conn.close()

    return [
        BidOrderPost(
            bid_order_post_id=row[0],
            bid_order_id=row[1],
            posted_by=row[2],
            post_number=row[3],
            posted_on=row[4],
            title=row[5],
            comment=row[6],
            parent_id=row[7],
            first_name=row[8],
            middle_name=row[9],
            last_name=row[10],
            user_profile_photo=row[11],
            team_role=row[12],
            designation_title=row[13]
        )
        for row in bid_order_posts
    ]

# Delete Bid Order Post by ID
def delete_bid_order_post(bid_order_post_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM bid_order_post WHERE bid_order_post_id = %s RETURNING *;"
    cursor.execute(query, (bid_order_post_id,))
    deleted_bid_order_post = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_bid_order_post:
        return True
    else:
        return False

# Get Bid Order Post by ID
def get_bid_order_post_by_id(bid_order_post_id: int) -> Optional[BidOrderPost]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*, 
            u.first_name, u.middle_name, u.last_name, u.user_profile_photo,
            t.team_role,
            d.title AS designation_title
            FROM bid_order_post b
            LEFT JOIN users u ON u.user_id=b.posted_by   
            LEFT JOIN designation d ON d.designation_id = u.designation_id 
            LEFT JOIN team t ON t.team_id = u.team_id
        WHERE b.bid_order_post_id = %s;
        """
    cursor.execute(query, (bid_order_post_id,))
    bid_order_post = cursor.fetchone()

    conn.close()

    if bid_order_post:
        BidOrderPost(
            bid_order_post_id=bid_order_post[0],
            bid_order_id=bid_order_post[1],
            posted_by=bid_order_post[2],
            post_number=bid_order_post[3],
            posted_on=bid_order_post[4],
            title=bid_order_post[5],
            comment=bid_order_post[6],
            parent_id=bid_order_post[7],
            first_name=bid_order_post[8],
            middle_name=bid_order_post[9],
            last_name=bid_order_post[10],
            user_profile_photo=bid_order_post[11],
            team_role=bid_order_post[12],
            designation_title=bid_order_post[13]
        )
    else:
        return None

# Update Bid Order Post by ID
def update_bid_order_post(bid_order_post_id: int, new_data: BidOrderPostCreate) -> Optional[BidOrderPostGetOneRecord]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_order_post
    SET posted_by = %s, post_number = %s, title = %s, comment = %s, parent_id = %s
    WHERE bid_order_post_id = %s RETURNING *;
    """

    values = (
        new_data.posted_by,
        new_data.post_number,
        new_data.title,
        new_data.comment,
        new_data.parent_id,
        bid_order_post_id
    )

    cursor.execute(query, values)
    updated_bid_order_post = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_order_post:
        return  BidOrderPostGetOneRecord(
            bid_order_post_id=updated_bid_order_post[0],
            bid_order_id=updated_bid_order_post[1],
            posted_by=updated_bid_order_post[2],
            post_number=updated_bid_order_post[3],
            posted_on=updated_bid_order_post[4],
            title=updated_bid_order_post[5],
            comment=updated_bid_order_post[6],
            parent_id=updated_bid_order_post[7]
        )
    else:
        return None
