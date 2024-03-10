from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from bid_kickoff_meeting.schemas import BidKickoffMeetingCreate, BidKickoffMeeting


def create_bid_kickoff_meeting(bid_kickoff_meeting_data: BidKickoffMeetingCreate) -> BidKickoffMeeting:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO bid_kickoff_meeting (
        rfx_id,
        title,
        description,
        template,
        template_type,
        location,
        date,
        start_time,
        end_time,
        created_on
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_kickoff_meeting_data.rfx_id,
        bid_kickoff_meeting_data.title,
        bid_kickoff_meeting_data.description,
        bid_kickoff_meeting_data.template,
        bid_kickoff_meeting_data.template_type,
        bid_kickoff_meeting_data.location,
        bid_kickoff_meeting_data.date,
        bid_kickoff_meeting_data.start_time,
        bid_kickoff_meeting_data.end_time,
        bid_kickoff_meeting_data.created_on          
    )

    cursor.execute(query, values)
    new_bid_kickoff_meeting = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_bid_kickoff_meeting:
        return BidKickoffMeeting(
            bid_kickoff_meeting_id=new_bid_kickoff_meeting[0],
            rfx_id=new_bid_kickoff_meeting[1],
            title=new_bid_kickoff_meeting[2],
            description=new_bid_kickoff_meeting[3],
            template=new_bid_kickoff_meeting[4],
            template_type=new_bid_kickoff_meeting[5],
            location=new_bid_kickoff_meeting[6],
            date=new_bid_kickoff_meeting[7],
            start_time=new_bid_kickoff_meeting[8],
            end_time=new_bid_kickoff_meeting[9],
            created_on=new_bid_kickoff_meeting[10]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Kickoff Meeting creation failed")


def get_all_bid_kickoff_meeting(rfx_id: int) -> List[BidKickoffMeeting]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bid_kickoff_meeting WHERE rfx_id = %s
        ORDER BY created_on DESC;
        """

    cursor.execute(query,(rfx_id,))
    bid_kickoff_meeting = cursor.fetchall()

    conn.close()
    if bid_kickoff_meeting:
        return [
            BidKickoffMeeting(
                bid_kickoff_meeting_id=row[0],
                rfx_id=row[1],
                title=row[2],
                description=row[3],
                template=row[4],
                template_type=row[5],
                location=row[6],
                date=row[7],
                start_time=row[8],
                end_time=row[9],
                created_on=row[10]
            )
            for row in bid_kickoff_meeting
        ]
    else:
        None


def update_bid_kickoff_meeting(bid_kickoff_meeting_id: int, bid_kickoff_meeting_data: BidKickoffMeetingCreate) -> Optional[BidKickoffMeeting]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_kickoff_meeting SET 
        title = %s,
        description = %s,
        template = %s,
        template_type = %s,
        location = %s,
        date = %s,
        start_time = %s,
        end_time = %s
    WHERE bid_kickoff_meeting_id = %s RETURNING *;
    """

    values = (
        bid_kickoff_meeting_data.title,
        bid_kickoff_meeting_data.description,
        bid_kickoff_meeting_data.template,
        bid_kickoff_meeting_data.template_type,
        bid_kickoff_meeting_data.location,
        bid_kickoff_meeting_data.date,
        bid_kickoff_meeting_data.start_time,
        bid_kickoff_meeting_data.end_time,
        bid_kickoff_meeting_id
    )

    cursor.execute(query, values)
    updated_bid_kickoff_meeting = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_kickoff_meeting:
        return BidKickoffMeeting(
            bid_kickoff_meeting_id=updated_bid_kickoff_meeting[0],
            rfx_id=updated_bid_kickoff_meeting[1],
            title=updated_bid_kickoff_meeting[2],
            description=updated_bid_kickoff_meeting[3],
            template=updated_bid_kickoff_meeting[4],
            template_type=updated_bid_kickoff_meeting[5],
            location=updated_bid_kickoff_meeting[6],
            date=updated_bid_kickoff_meeting[7],
            start_time=updated_bid_kickoff_meeting[8],
            end_time=updated_bid_kickoff_meeting[9],
            created_on=updated_bid_kickoff_meeting[10]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Kickoff Meeting update failed")


def delete_bid_kickoff_meeting(bid_kickoff_meeting_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "DELETE FROM bid_kickoff_meeting WHERE bid_kickoff_meeting_id = %s RETURNING bid_kickoff_meeting_id;"
    cursor.execute(query, (bid_kickoff_meeting_id,))
    deleted_bid_kickoff_meeting = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_bid_kickoff_meeting:
        return True
    else:
        return False


def get_bid_kickoff_meeting_by_id(bid_kickoff_meeting_id: int) -> Optional[BidKickoffMeeting]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bid_kickoff_meeting WHERE bid_kickoff_meeting_id = %s
        ORDER BY created_on DESC;
        """
        
    cursor.execute(query, (bid_kickoff_meeting_id,))
    bid_kickoff_meeting = cursor.fetchone()

    conn.close()

    if bid_kickoff_meeting:
        return BidKickoffMeeting (
                bid_kickoff_meeting_id=bid_kickoff_meeting[0],
                rfx_id=bid_kickoff_meeting[1],
                title=bid_kickoff_meeting[2],
                description=bid_kickoff_meeting[3],
                template=bid_kickoff_meeting[4],
                template_type=bid_kickoff_meeting[5],
                location=bid_kickoff_meeting[6],
                date=bid_kickoff_meeting[7],
                start_time=bid_kickoff_meeting[8],
                end_time=bid_kickoff_meeting[9],
                created_on=bid_kickoff_meeting[10]
            )
    
    else:
        return None


