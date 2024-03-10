from typing import Optional, List
from fastapi import HTTPException

from datetime import date, datetime
from db.connection import get_db_connection
from rfx_stage_detail.schemas import RfxStageDetail, RfxStageDetailCreate


def create_rfx_stage_detail(rfx_stage_detail_data: RfxStageDetailCreate) -> RfxStageDetail:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO rfx_stage_detail (
        rfx_id, status, description, created_date, completed, completed_at
    ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        rfx_stage_detail_data.rfx_id,
        rfx_stage_detail_data.status,
        rfx_stage_detail_data.description,
        rfx_stage_detail_data.created_date,
        rfx_stage_detail_data.completed,
        rfx_stage_detail_data.completed_at,
    )

    cursor.execute(query, values)
    new_rfx_stage_detail = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_rfx_stage_detail:
        return RfxStageDetail(
            rfx_stage_detail_id=new_rfx_stage_detail[0],
            rfx_id=new_rfx_stage_detail[1],
            status=new_rfx_stage_detail[2],
            description=new_rfx_stage_detail[3],
            created_date=new_rfx_stage_detail[4],
            completed=new_rfx_stage_detail[5],
            completed_at=new_rfx_stage_detail[6],
        )
    else:
        raise HTTPException(status_code=404, detail="Rfx Stage Detail creation failed")


def get_all_rfx_stage_details() -> List[RfxStageDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM rfx_stage_detail;"
    cursor.execute(query)
    rfx_stage_details = cursor.fetchall()

    conn.close()

    return [
        RfxStageDetail(
            rfx_stage_detail_id=row[0],
            rfx_id=row[1],
            status=row[2],
            description=row[3],
            created_date=row[4],
            completed=row[5],
            completed_at=row[6],
        )
        for row in rfx_stage_details
    ]


def update_rfx_stage_detail(rfx_stage_detail_id: int, rfx_stage_detail_data: RfxStageDetailCreate) -> Optional[RfxStageDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE rfx_stage_detail SET 
        rfx_id = %s,
        status = %s,
        description = %s,
        created_date = %s,
        completed = %s,
        completed_at = %s
    WHERE rfx_stage_detail_id = %s RETURNING *;
    """

    values = (
        rfx_stage_detail_data.rfx_id,
        rfx_stage_detail_data.status,
        rfx_stage_detail_data.description,
        rfx_stage_detail_data.created_date,
        rfx_stage_detail_data.completed,
        rfx_stage_detail_data.completed_at,
        rfx_stage_detail_id
    )

    cursor.execute(query, values)
    updated_rfx_stage_detail = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_rfx_stage_detail:
        return RfxStageDetail(
            rfx_stage_detail_id=updated_rfx_stage_detail[0],
            rfx_id=updated_rfx_stage_detail[1],
            status=updated_rfx_stage_detail[2],
            description=updated_rfx_stage_detail[3],
            created_date=updated_rfx_stage_detail[4],
            completed=updated_rfx_stage_detail[5],
            completed_at=updated_rfx_stage_detail[6],
        )
    else:
        raise HTTPException(status_code=404, detail="Rfx Stage Detail update failed")


def delete_rfx_stage_detail(rfx_stage_detail_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM rfx_stage_detail WHERE rfx_stage_detail_id = %s RETURNING rfx_stage_detail_id;"
    cursor.execute(query, (rfx_stage_detail_id,))
    deleted_rfx_stage_detail = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_rfx_stage_detail:
        return True
    else:
        return False


def get_rfx_stage_detail_by_id(rfx_stage_detail_id: int) -> Optional[RfxStageDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM rfx_stage_detail WHERE rfx_stage_detail_id = %s;"
    cursor.execute(query, (rfx_stage_detail_id,))
    rfx_stage_detail = cursor.fetchone()

    conn.close()

    if rfx_stage_detail:
        return RfxStageDetail(
            rfx_stage_detail_id=rfx_stage_detail[0],
            rfx_id=rfx_stage_detail[1],
            status=rfx_stage_detail[2],
            description=rfx_stage_detail[3],
            created_date=rfx_stage_detail[4],
            completed=rfx_stage_detail[5],
            completed_at=rfx_stage_detail[6],
        )
    else:
        return None


def get_rfx_stage_detail_by_status(status: str) -> Optional[List[RfxStageDetail]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM rfx_stage_detail WHERE status = %s;"
    cursor.execute(query, (status,))
    rfx_stage_details = cursor.fetchall()

    conn.close()

    if rfx_stage_details:
        return [
            RfxStageDetail(
                rfx_stage_detail_id=row[0],
                rfx_id=row[1],
                status=row[2],
                description=row[3],
                created_date=row[4],
                completed=row[5],
                completed_at=row[6],
            )
            for row in rfx_stage_details
        ]
    else:
        return None
