from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from bid_submission_post.schemas import BidSubmissionPostCreate, BidSubmissionPost, GetBidSubmissionPost


def create_bid_submission_post(bid_submission_post_data: BidSubmissionPostCreate) -> BidSubmissionPost:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_submission_post (
        bid_submission_id,
        title,
        comment,
        status,
        posted_by,
        posted_on
    ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_submission_post_data.bid_submission_id,
        bid_submission_post_data.title,
        bid_submission_post_data.comment,
        bid_submission_post_data.status,
        bid_submission_post_data.posted_by,
        bid_submission_post_data.posted_on
    )

    cursor.execute(query, values)
    new_bid_submission_post = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if new_bid_submission_post:
        return BidSubmissionPost(
            bid_submission_post_id=new_bid_submission_post[0],
            bid_submission_id=new_bid_submission_post[1],
            title=new_bid_submission_post[2],
            comment=new_bid_submission_post[3],
            status=new_bid_submission_post[4],
            posted_by=new_bid_submission_post[5],
            posted_on=new_bid_submission_post[6]            
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Submission Post creation failed")


def get_all_bid_submission_post(bid_submission_id: int) -> List[GetBidSubmissionPost]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*, 
            u.user_name, u.email, u.first_name, u.middle_name, u.last_name,
            u.user_role, u.role_level, u.user_profile_photo,
			t.team_role,
			d.title AS designation_title
            FROM bid_submission_post b
			LEFT JOIN users u  ON u.user_id  = b.posted_by
			LEFT JOIN team t ON t.team_id = u.team_id
			LEFT JOIN designation d ON d.designation_id = u.designation_id 
        WHERE bid_submission_id = %s;
        """

    cursor.execute(query,(bid_submission_id,))
    bid_submission_post = cursor.fetchall()

    conn.close()
    if bid_submission_post:
        return [
            GetBidSubmissionPost(
                bid_submission_post_id=row[0],
                bid_submission_id=row[1],
                title=row[2],
                comment=row[3],
                status=row[4],
                posted_by=row[5],
                posted_on=row[6],
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
            for row in bid_submission_post
        ]
    else:
        None


def update_bid_submission_post(bid_submission_post_id: int, bid_submission_post_data: BidSubmissionPostCreate) -> Optional[BidSubmissionPost]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_submission_post SET 
        title = %s,
        comment = %s,
        status = %s,
        posted_by = %s
    WHERE bid_submission_post_id = %s RETURNING *;
    """

    values = (
        bid_submission_post_data.title,
        bid_submission_post_data.comment,
        bid_submission_post_data.status,
        bid_submission_post_data.posted_by,
        bid_submission_post_id
    )

    cursor.execute(query, values)
    updated_bid_submission_post = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_submission_post:
        return BidSubmissionPost(            
            bid_submission_post_id=updated_bid_submission_post[0],
            bid_submission_id=updated_bid_submission_post[1],
            title=updated_bid_submission_post[2],
            comment=updated_bid_submission_post[3],
            status=updated_bid_submission_post[4],
            posted_by=updated_bid_submission_post[5],
            posted_on=updated_bid_submission_post[6]    
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Submission post update failed")


def delete_bid_submission_post(bid_submission_post_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "DELETE FROM bid_submission_post WHERE bid_submission_post_id = %s RETURNING bid_submission_post_id;"
    cursor.execute(query, (bid_submission_post_id,))
    deleted_bid_submission_post = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if deleted_bid_submission_post:
        return True
    else:
        return False


def get_bid_submission_post_by_id(bid_submission_post_id: int) -> Optional[GetBidSubmissionPost]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*, 
            u.user_name, u.email, u.first_name, u.middle_name, u.last_name,
            u.user_role, u.role_level, u.user_profile_photo,
			t.team_role,
			d.title AS designation_title
            FROM bid_submission_post b
			LEFT JOIN users u  ON u.user_id  = b.posted_by
			LEFT JOIN team t ON t.team_id = u.team_id
			LEFT JOIN designation d ON d.designation_id = u.designation_id
        WHERE bid_submission_post_id = %s;
        """
    cursor.execute(query, (bid_submission_post_id,))
    bid_submission_post = cursor.fetchone()

    conn.close()

    if bid_submission_post:
        return GetBidSubmissionPost (
                bid_submission_post_id=bid_submission_post[0],
                bid_submission_id=bid_submission_post[1],
                title=bid_submission_post[2],
                comment=bid_submission_post[3],
                status=bid_submission_post[4],
                posted_by=bid_submission_post[5],
                posted_on=bid_submission_post[6],
                user_name=bid_submission_post[7],
                email=bid_submission_post[8],
                first_name=bid_submission_post[9],
                middle_name=bid_submission_post[10],
                last_name=bid_submission_post[11],
                user_role=bid_submission_post[12],
                role_level=bid_submission_post[13],
                user_profile_photo=bid_submission_post[14],
                team_role=bid_submission_post[15],
                designation_title=bid_submission_post[16]    
            )
    
    else:
        return None


