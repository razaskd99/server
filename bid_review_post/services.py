from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from bid_review_post.schemas import BidReviewPostCreate, BidReviewPost, GetBidReviewPost


def create_bid_review_post(bid_review_post_data: BidReviewPostCreate) -> BidReviewPost:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_review_post (
        bid_review_id,
        title,
        comment,
        status,
        posted_by,
        posted_at
    ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_review_post_data.bid_review_id,
        bid_review_post_data.title,
        bid_review_post_data.comment,
        bid_review_post_data.status,
        bid_review_post_data.posted_by,
        bid_review_post_data.posted_at
    )

    cursor.execute(query, values)
    new_bid_review_post = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if new_bid_review_post:
        return BidReviewPost(
            bid_review_post_id=new_bid_review_post[0],
            bid_review_id=new_bid_review_post[1],
            title=new_bid_review_post[2],
            comment=new_bid_review_post[3],
            status=new_bid_review_post[4],
            posted_by=new_bid_review_post[5],
            posted_at=new_bid_review_post[6]            
        )
    else:
        raise HTTPException(status_code=404, detail="Bid review post Detail creation failed")


def get_all_bid_review_post(bid_review_id: int) -> List[GetBidReviewPost]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*, 
            u.user_name, u.email, u.first_name, u.middle_name, u.last_name,
            u.user_role, u.role_level, u.user_profile_photo,
			t.team_role,
			d.title AS designation_title
            FROM bid_review_post b
			LEFT JOIN users u  ON u.user_id  = b.posted_by
			LEFT JOIN team t ON t.team_id = u.team_id
			LEFT JOIN designation d ON d.designation_id = u.designation_id 
        WHERE bid_review_id = %s;
        """

    cursor.execute(query,(bid_review_id,))
    bid_review_post = cursor.fetchall()

    conn.close()
    if bid_review_post:
        return [
            GetBidReviewPost(
                bid_review_post_id=row[0],
                bid_review_id=row[1],
                title=row[2],
                comment=row[3],
                status=row[4],
                posted_by=row[5],
                posted_at=row[6],
                user_name=row[7],
                email=row[8],
                first_name=row[9],
                middle_name=row[10],
                last_name=row[11],
                user_role=row[12],
                role_level=row[13],
                user_profile_photo=row[14],
                team_role=row[15],
                designation_title=row[16]
            )
            for row in bid_review_post
        ]
    else:
        None


def update_bid_review_post(bid_review_post_id: int, bid_review_post_data: BidReviewPostCreate) -> Optional[BidReviewPost]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_review_post SET 
        title = %s,
        comment = %s,
        status = %s,
        posted_by = %s,
        posted_at = %s
    WHERE bid_review_post_id = %s RETURNING *;
    """

    values = (
        bid_review_post_data.title,
        bid_review_post_data.comment,
        bid_review_post_data.status,
        bid_review_post_data.posted_by,
        bid_review_post_data.posted_at,
        bid_review_post_id
    )

    cursor.execute(query, values)
    updated_bid_review_post = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_review_post:
        return BidReviewPost(            
            bid_review_post_id=updated_bid_review_post[0],
            bid_review_id=updated_bid_review_post[1],
            title=updated_bid_review_post[2],
            comment=updated_bid_review_post[3],
            status=updated_bid_review_post[4],
            posted_by=updated_bid_review_post[5],
            posted_at=updated_bid_review_post[6]    
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Review post update failed")


def delete_bid_review_post(bid_review_post_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "DELETE FROM bid_review_post WHERE bid_review_post_id = %s RETURNING bid_review_post_id;"
    cursor.execute(query, (bid_review_post_id,))
    deleted_bid_review_post = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if deleted_bid_review_post:
        return True
    else:
        return False


def get_bid_review_post_by_id(bid_review_post_id: int) -> Optional[GetBidReviewPost]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*, 
            u.user_name, u.email, u.first_name, u.middle_name, u.last_name,
            u.user_role, u.role_level, u.user_profile_photo,
			t.team_role,
			d.title AS designation_title
            FROM bid_review_post b
			LEFT JOIN users u  ON u.user_id  = b.posted_by
			LEFT JOIN team t ON t.team_id = u.team_id
			LEFT JOIN designation d ON d.designation_id = u.designation_id
        WHERE bid_review_post_id = %s;
        """
    cursor.execute(query, (bid_review_post_id,))
    bid_review_post = cursor.fetchone()

    conn.close()

    if bid_review_post:
        return GetBidReviewPost (
                bid_review_post_id=bid_review_post[0],
                bid_review_id=bid_review_post[1],
                title=bid_review_post[2],
                comment=bid_review_post[3],
                status=bid_review_post[4],
                posted_by=bid_review_post[5],
                posted_at=bid_review_post[6],
                user_name=bid_review_post[7],
                email=bid_review_post[8],
                first_name=bid_review_post[9],
                middle_name=bid_review_post[10],
                last_name=bid_review_post[11],
                user_role=bid_review_post[12],
                role_level=bid_review_post[13],
                user_profile_photo=bid_review_post[14],
                team_role=bid_review_post[15],
                designation_title=bid_review_post[16]    
            )
    
    else:
        return None


