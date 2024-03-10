from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from bid_review_contacts.schemas import BidReviewContactsCreate, BidReviewContacts, BidReviewGet


def create_bid_review_contacts(bid_review_contacts_data: BidReviewContactsCreate) -> BidReviewContacts:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_review_contacts (
        bid_review_id,
        user_id,
        review_role,
        has_approved,
        approved_notes
    ) VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_review_contacts_data.bid_review_id,
        bid_review_contacts_data.user_id,
        bid_review_contacts_data.review_role,
        bid_review_contacts_data.has_approved,
        bid_review_contacts_data.approved_notes
    )

    cursor.execute(query, values)
    new_bid_review_contacts = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if new_bid_review_contacts:
        return BidReviewContacts(
            bid_review_contacts_id=new_bid_review_contacts[0],
            bid_review_id=new_bid_review_contacts[1],
            user_id=new_bid_review_contacts[2],
            review_role=new_bid_review_contacts[3],
            has_approved=new_bid_review_contacts[4],
            approved_notes=new_bid_review_contacts[5]            
        )
    else:
        raise HTTPException(status_code=404, detail="Bid review contact Detail creation failed")


def get_all_bid_review_contacts(bid_review_id: int) -> List[BidReviewGet]:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    
    query = """
        SELECT c.*,
            u.first_name, u.middle_name, u.last_name, u.email, u.user_profile_photo
            FROM bid_review_contacts c 
            LEFT JOIN users u ON u.user_id = c.user_id              
        WHERE c.bid_review_id = %s ;
        """

    cursor.execute(query,(bid_review_id,))
    bid_review_contacts = cursor.fetchall()

    conn.close()
    if bid_review_contacts:
        return [
            BidReviewGet(
                bid_review_contacts_id=row[0],
                bid_review_id=row[1],
                user_id=row[2],
                review_role=row[3],
                has_approved=row[4],
                approved_notes=row[5],
                first_name=row[6],
                middle_name=row[7],
                last_name=row[8],
                email=row[9],
                user_profile_photo=row[10]

            )
            for row in bid_review_contacts
        ]
    else:
        None


def update_bid_review_contacts(bid_review_contacts_id: int, bid_review_contacts_data: BidReviewContactsCreate) -> Optional[BidReviewContacts]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_review_contacts SET 
        user_id = %s,
        review_role = %s,
        has_approved = %s,
        approved_notes = %s
    WHERE bid_review_contacts_id = %s RETURNING *;
    """

    values = (
        bid_review_contacts_data.user_id,
        bid_review_contacts_data.review_role,
        bid_review_contacts_data.has_approved,
        bid_review_contacts_data.approved_notes,
        bid_review_contacts_id
    )

    cursor.execute(query, values)
    updated_bid_review_contacts = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_review_contacts:
        return BidReviewContacts(            
            bid_review_contacts_id=updated_bid_review_contacts[0],
            bid_review_id=updated_bid_review_contacts[1],
            user_id=updated_bid_review_contacts[2],
            review_role=updated_bid_review_contacts[3],
            has_approved=updated_bid_review_contacts[4],
            approved_notes=updated_bid_review_contacts[5]    
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Review Contacts update failed")


def delete_bid_review_contacts(bid_review_contacts_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "DELETE FROM bid_review_contacts WHERE bid_review_contacts_id = %s RETURNING bid_review_contacts_id;"
    cursor.execute(query, (bid_review_contacts_id,))
    deleted_bid_review_contacts = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if deleted_bid_review_contacts:
        return True
    else:
        return False


def get_bid_review_contacts_by_id(bid_review_contacts_id: int) -> Optional[BidReviewGet]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT c.*,
            u.first_name, u.middle_name, u.last_name, u.email, u.user_profile_photo
            FROM bid_review_contacts c 
            LEFT JOIN users u ON u.user_id = c.user_id              
        WHERE c.bid_review_contacts_id = %s ;
        """

    cursor.execute(query, (bid_review_contacts_id,))
    bid_review_contacts = cursor.fetchone()

    conn.close()

    if bid_review_contacts:
        return BidReviewGet(
                bid_review_contacts_id=bid_review_contacts[0],
                bid_review_id=bid_review_contacts[1],
                user_id=bid_review_contacts[2],
                review_role=bid_review_contacts[3],
                has_approved=bid_review_contacts[4],
                approved_notes=bid_review_contacts[5],
                first_name=bid_review_contacts[6],
                middle_name=bid_review_contacts[7],
                last_name=bid_review_contacts[8],
                email=bid_review_contacts[9],
                user_profile_photo=bid_review_contacts[10]

            )
    
    else:
        return None


