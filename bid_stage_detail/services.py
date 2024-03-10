from typing import Optional, List
from fastapi import HTTPException

from datetime import date, datetime
from db.connection import get_db_connection
from bid_stage_detail.schemas import BidStageDetail, BidStageDetailCreate


def create_bid_stage_detail(bid_stage_detail_data: BidStageDetailCreate) -> BidStageDetail:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_stage_detail (
        rfx_id, status, description, created_date, completed, completed_at
    ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_stage_detail_data.rfx_id,
        bid_stage_detail_data.status,
        bid_stage_detail_data.description,
        bid_stage_detail_data.created_date,
        bid_stage_detail_data.completed,
        bid_stage_detail_data.completed_at,
    )

    cursor.execute(query, values)
    new_bid_stage_detail = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_bid_stage_detail:
        return BidStageDetail(
            bid_stage_detail_id=new_bid_stage_detail[0],
            rfx_id=new_bid_stage_detail[1],
            status=new_bid_stage_detail[2],
            description=new_bid_stage_detail[3],
            created_date=new_bid_stage_detail[4],
            completed=new_bid_stage_detail[5],
            completed_at=new_bid_stage_detail[6],
        )
    else:
        raise HTTPException(status_code=404, detail="Rfx Stage Detail creation failed")


def get_all_bid_stage_details() -> List[BidStageDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_stage_detail;"
    cursor.execute(query)
    bid_stage_details = cursor.fetchall()

    conn.close()

    return [
        BidStageDetail(
            bid_stage_detail_id=row[0],
            rfx_id=row[1],
            status=row[2],
            description=row[3],
            created_date=row[4],
            completed=row[5],
            completed_at=row[6],
        )
        for row in bid_stage_details
    ]


def update_bid_stage_detail(bid_stage_detail_id: int, bid_stage_detail_data: BidStageDetailCreate) -> Optional[BidStageDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_stage_detail SET 
        rfx_id = %s,
        status = %s,
        description = %s,
        created_date = %s,
        completed = %s,
        completed_at = %s
    WHERE bid_stage_detail_id = %s RETURNING *;
    """

    values = (
        bid_stage_detail_data.rfx_id,
        bid_stage_detail_data.status,
        bid_stage_detail_data.description,
        bid_stage_detail_data.created_date,
        bid_stage_detail_data.completed,
        bid_stage_detail_data.completed_at,
        bid_stage_detail_id
    )

    cursor.execute(query, values)
    updated_bid_stage_detail = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_stage_detail:
        return BidStageDetail(
            bid_stage_detail_id=updated_bid_stage_detail[0],
            rfx_id=updated_bid_stage_detail[1],
            status=updated_bid_stage_detail[2],
            description=updated_bid_stage_detail[3],
            created_date=updated_bid_stage_detail[4],
            completed=updated_bid_stage_detail[5],
            completed_at=updated_bid_stage_detail[6],
        )
    else:
        raise HTTPException(status_code=404, detail="Rfx Stage Detail update failed")


def delete_bid_stage_detail(bid_stage_detail_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM bid_stage_detail WHERE bid_stage_detail_id = %s RETURNING bid_stage_detail_id;"
    cursor.execute(query, (bid_stage_detail_id,))
    deleted_bid_stage_detail = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_bid_stage_detail:
        return True
    else:
        return False


def get_bid_stage_detail_by_id(bid_stage_detail_id: int) -> Optional[BidStageDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_stage_detail WHERE bid_stage_detail_id = %s;"
    cursor.execute(query, (bid_stage_detail_id,))
    bid_stage_detail = cursor.fetchone()

    conn.close()

    if bid_stage_detail:
        return BidStageDetail(
            bid_stage_detail_id=bid_stage_detail[0],
            rfx_id=bid_stage_detail[1],
            status=bid_stage_detail[2],
            description=bid_stage_detail[3],
            created_date=bid_stage_detail[4],
            completed=bid_stage_detail[5],
            completed_at=bid_stage_detail[6],
        )
    else:
        return None


def get_bid_stage_detail_by_status(status: str) -> Optional[List[BidStageDetail]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_stage_detail WHERE status = %s;"
    cursor.execute(query, (status,))
    bid_stage_details = cursor.fetchall()

    conn.close()

    if bid_stage_details:
        return [
            BidStageDetail(
                bid_stage_detail_id=row[0],
                rfx_id=row[1],
                status=row[2],
                description=row[3],
                created_date=row[4],
                completed=row[5],
                completed_at=row[6],
            )
            for row in bid_stage_details
        ]
    else:
        return None
