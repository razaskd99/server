from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from rfx_stage.schemas import RfxStageCreate, RfxStage


def create_rfx_stage(rfx_stage_data: RfxStageCreate) -> RfxStage:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO rfx_stage (
        tenant_id,
        rfx_id,
        default_name,
        new_name,
        stage_order,
        required
    ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        rfx_stage_data.tenant_id,
        rfx_stage_data.rfx_id,
        rfx_stage_data.default_name,
        rfx_stage_data.new_name,
        rfx_stage_data.stage_order,
        rfx_stage_data.required     
    )

    cursor.execute(query, values)
    new_rfx_stage = cursor.fetchone()


    query = """
    INSERT INTO rfx_stage_detail (
        rfx_stage_id,
        status,
        description,
        created_date,
        completed,
        completed_at
    ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        new_rfx_stage[0],
        rfx_stage_data.status,
        rfx_stage_data.description,
        rfx_stage_data.created_date,
        rfx_stage_data.completed,
        rfx_stage_data.completed_at
    )
    
    cursor.execute(query, values)
    new_rfx_stage_detail = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_rfx_stage:
        return RfxStage(
            rfx_stage_id=new_rfx_stage[0],
            tenant_id=new_rfx_stage[1],
            rfx_id=new_rfx_stage[2],
            default_name=new_rfx_stage[3],
            new_name=new_rfx_stage[4],
            stage_order=new_rfx_stage[5],
            required=new_rfx_stage[6],
            # stage detail
            status=new_rfx_stage_detail[2],
            description=new_rfx_stage_detail[3],
            created_date=new_rfx_stage_detail[4],
            completed=new_rfx_stage_detail[5],
            completed_at=new_rfx_stage_detail[6]
        )
    else:
        raise HTTPException(status_code=404, detail="Rfx Stage Detail creation failed")


def get_all_rfx_stages(tenant_id: int, rfx_id: int) -> List[RfxStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT a.*,
            b.status, b.description, b.created_date, b.completed, b.completed_at
            FROM rfx_stage a
            INNER JOIN rfx_stage_detail b ON a.rfx_stage_id=b.rfx_stage_id                
        WHERE a.tenant_id = %s AND rfx_id = %s
        ORDER BY a.stage_order ;
        """

    cursor.execute(query,(tenant_id, rfx_id))
    rfx_stages = cursor.fetchall()

    conn.close()
    if rfx_stages:
        return [
            RfxStage(
                rfx_stage_id=row[0],
                tenant_id=row[1],
                rfx_id=row[2],
                default_name=row[3],
                new_name=row[4],
                stage_order=row[5],
                required=row[6],
                status=row[7],
                description=row[8],
                created_date=row[9],
                completed=row[10],
                completed_at=row[11]
            )
            for row in rfx_stages
        ]
    else:
        None


def update_rfx_stage(tenant_id: int, rfx_stage_id: int, rfx_stage_data: RfxStageCreate) -> Optional[RfxStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE rfx_stage SET 
        default_name = %s,
        new_name = %s,
        stage_order = %s,
        required = %s
    WHERE rfx_stage_id = %s AND tenant_id = %s RETURNING *;
    """

    values = (
        rfx_stage_data.default_name,
        rfx_stage_data.new_name,
        rfx_stage_data.stage_order,
        rfx_stage_data.required,
        rfx_stage_id,
        tenant_id
    )

    cursor.execute(query, values)
    updated_rfx_stage = cursor.fetchone()

    query = """
    UPDATE rfx_stage_detail SET 
        status = %s,
        description = %s,
        created_date = %s,
        completed = %s,
        completed_at = %s
    WHERE rfx_stage_id = %s RETURNING *;
    """

    values = (
        rfx_stage_data.status,
        rfx_stage_data.description,
        rfx_stage_data.created_date,
        rfx_stage_data.completed,
        rfx_stage_data.completed_at,
        rfx_stage_id
    )
    cursor.execute(query, values)
    updated_rfx_stage_details = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_rfx_stage:
        return RfxStage(
            rfx_stage_id=updated_rfx_stage[0],
            tenant_id=updated_rfx_stage[1],
            rfx_id=updated_rfx_stage[2],
            default_name=updated_rfx_stage[3],
            new_name=updated_rfx_stage[4],
            stage_order=updated_rfx_stage[5],
            required=updated_rfx_stage[6],
            # stage details
            status=updated_rfx_stage_details[2],
            description=updated_rfx_stage_details[3],
            created_date=updated_rfx_stage_details[4],
            completed=updated_rfx_stage_details[5],
            completed_at=updated_rfx_stage_details[6]
        )
    else:
        raise HTTPException(status_code=404, detail="Rfx Stage update failed")


def delete_rfx_stage(rfx_stage_id: int, tenant_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "DELETE FROM rfx_stage_detail WHERE rfx_stage_id = %s RETURNING rfx_stage_id;"
        cursor.execute(query, (rfx_stage_id,))
        deleted_rfx_stage_detail = cursor.fetchone()
    except:
        None

    query = "DELETE FROM rfx_stage WHERE rfx_stage_id = %s AND tenant_id = %s RETURNING rfx_stage_id;"
    cursor.execute(query, (rfx_stage_id, tenant_id,))
    deleted_rfx_stage = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_rfx_stage:
        return True
    else:
        return False


def get_rfx_stage_by_id(rfx_stage_id: int) -> Optional[RfxStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT a.*,
            b.status, b.description, b.created_date, b.completed, b.completed_at
            FROM rfx_stage a
            INNER JOIN rfx_stage_detail b ON a.rfx_stage_id=b.rfx_stage_id                
        WHERE a.rfx_stage_id = %s
        ORDER BY a.stage_order;
        """
    cursor.execute(query, (rfx_stage_id,))
    rfx_stage = cursor.fetchone()

    conn.close()

    if rfx_stage:
        return RfxStage (
                rfx_stage_id=rfx_stage[0],
                tenant_id=rfx_stage[1],
                rfx_id=rfx_stage[2],
                default_name=rfx_stage[3],
                new_name=rfx_stage[4],
                stage_order=rfx_stage[5],
                required=rfx_stage[6],
                status=rfx_stage[7],
                description=rfx_stage[8],
                created_date=rfx_stage[9],
                completed=rfx_stage[10],
                completed_at=rfx_stage[11]
            )
    
    else:
        return None


def get_rfx_stage_by_name(tenant_id: int, rfx_id: int, default_name : str) -> Optional[RfxStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT a.*,
            b.status, b.description, b.created_date, b.completed, b.completed_at
            FROM rfx_stage a
            INNER JOIN rfx_stage_detail b ON a.rfx_stage_id=b.rfx_stage_id                
        WHERE a.tenant_id = %s AND a.rfx_id = %s AND (lower(a.default_name) = %s OR lower(a.new_name) = %s)
        ORDER BY a.stage_order;
        """
    cursor.execute(query, (tenant_id, rfx_id, default_name.lower(), default_name.lower()))
    rfx_stage = cursor.fetchone()

    conn.close()

    if rfx_stage:
        return RfxStage(
                rfx_stage_id=rfx_stage[0],
                tenant_id=rfx_stage[1],
                rfx_id=rfx_stage[2],
                default_name=rfx_stage[3],
                new_name=rfx_stage[4],
                stage_order=rfx_stage[5],
                required=rfx_stage[6],
                status=rfx_stage[7],
                description=rfx_stage[8],
                created_date=rfx_stage[9],
                completed=rfx_stage[10],
                completed_at=rfx_stage[11]
            )
    else:
        return None
    

def get_rfx_stage_by_status(tenant_id: int, rfx_id: int, status : str) -> List[RfxStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT a.*,
            b.status, b.description, b.created_date, b.completed, b.completed_at
            FROM rfx_stage a
            INNER JOIN rfx_stage_detail b ON a.rfx_stage_id=b.rfx_stage_id                
        WHERE a.tenant_id = %s AND rfx_id = %s AND lower(b.status) = %s
        ORDER BY a.stage_order;
        """
    cursor.execute(query, (tenant_id, rfx_id, status.lower(),))
    rfx_stage_records = cursor.fetchall()

    conn.close()

    if rfx_stage_records:
        return [
            RfxStage (
                rfx_stage_id=row[0],
                tenant_id=row[1],
                rfx_id=row[2],
                default_name=row[3],
                new_name=row[4],
                stage_order=row[5],
                required=row[6],
                status=row[7],
                description=row[8],
                created_date=row[9],
                completed=row[10],
                completed_at=row[11]
            )
            for row in rfx_stage_records
        ]
    else:
        return None
