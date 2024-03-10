from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from bid_stage.schemas import BidStageCreate, BidStage


def create_bid_stage(bid_stage_data: BidStageCreate) -> BidStage:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO bid_stage (
        tenant_id,
        rfx_id,
        default_name,
        new_name,
        stage_order,
        required
    ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_stage_data.tenant_id,
        bid_stage_data.rfx_id,
        bid_stage_data.default_name,
        bid_stage_data.new_name,
        bid_stage_data.stage_order,
        bid_stage_data.required     
    )

    cursor.execute(query, values)
    new_bid_stage = cursor.fetchone()


    query = """
    INSERT INTO bid_stage_detail (
        bid_stage_id,
        status,
        description,
        created_date,
        completed,
        completed_at
    ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        new_bid_stage[0],
        bid_stage_data.status,
        bid_stage_data.description,
        bid_stage_data.created_date,
        bid_stage_data.completed,
        bid_stage_data.completed_at
    )
    
    cursor.execute(query, values)
    new_bid_stage_detail = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_bid_stage:
        return BidStage(
            bid_stage_id=new_bid_stage[0],
            tenant_id=new_bid_stage[1],
            rfx_id=new_bid_stage[2],
            default_name=new_bid_stage[3],
            new_name=new_bid_stage[4],
            stage_order=new_bid_stage[5],
            required=new_bid_stage[6],
            # bid stage detail
            status=new_bid_stage_detail[2],
            description=new_bid_stage_detail[3],
            created_date=new_bid_stage_detail[4],
            completed=new_bid_stage_detail[5],
            completed_at=new_bid_stage_detail[6]
        )
    else:
        raise HTTPException(status_code=404, detail="bid Stage Detail creation failed")


def get_all_bid_stages(tenant_id: int, rfx_id: int) -> List[BidStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT a.*,
            b.status, b.description, b.created_date, b.completed, b.completed_at
            FROM bid_stage a
            INNER JOIN bid_stage_detail b ON a.bid_stage_id=b.bid_stage_id                
        WHERE a.tenant_id = %s AND a.rfx_id = %s
        ORDER BY a.stage_order;
        """

    cursor.execute(query,(tenant_id, rfx_id))
    bid_stages = cursor.fetchall()

    conn.close()
    if bid_stages:
        return [
            BidStage(
                bid_stage_id=row[0],
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
            for row in bid_stages
        ]
    else:
        None


def update_bid_stage(tenant_id: int, bid_stage_id: int, bid_stage_data: BidStageCreate) -> Optional[BidStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_stage SET 
        default_name = %s,
        new_name = %s,
        stage_order = %s,
        required = %s
    WHERE bid_stage_id = %s AND tenant_id = %s RETURNING *;
    """

    values = (
        bid_stage_data.default_name,
        bid_stage_data.new_name,
        bid_stage_data.stage_order,
        bid_stage_data.required,
        bid_stage_id,
        tenant_id
    )

    cursor.execute(query, values)
    updated_bid_stage = cursor.fetchone()

    query = """
    UPDATE bid_stage_detail SET 
        status = %s,
        description = %s,
        created_date = %s,
        completed = %s,
        completed_at = %s
    WHERE bid_stage_id = %s RETURNING *;
    """

    values = (
        bid_stage_data.status,
        bid_stage_data.description,
        bid_stage_data.created_date,
        bid_stage_data.completed,
        bid_stage_data.completed_at,
        bid_stage_id
    )
    cursor.execute(query, values)
    updated_bid_stage_details = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_stage:
        return BidStage(
            bid_stage_id=updated_bid_stage[0],
            tenant_id=updated_bid_stage[1],
            rfx_id=updated_bid_stage[2],
            default_name=updated_bid_stage[3],
            new_name=updated_bid_stage[4],
            stage_order=updated_bid_stage[5],
            required=updated_bid_stage[6],
            # Bid stage details
            status=updated_bid_stage_details[2],
            description=updated_bid_stage_details[3],
            created_date=updated_bid_stage_details[4],
            completed=updated_bid_stage_details[5],
            completed_at=updated_bid_stage_details[6]
        )
    else:
        raise HTTPException(status_code=404, detail="bid Stage update failed")


def delete_bid_stage(bid_stage_id: int, tenant_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "DELETE FROM bid_stage_detail WHERE bid_stage_id = %s RETURNING bid_stage_id;"
        cursor.execute(query, (bid_stage_id,))
        deleted_bid_stage_detail = cursor.fetchone()
    except:
        None

    query = "DELETE FROM bid_stage WHERE bid_stage_id = %s AND tenant_id = %s RETURNING bid_stage_id;"
    cursor.execute(query, (bid_stage_id, tenant_id,))
    deleted_bid_stage = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_bid_stage:
        return True
    else:
        return False


def get_bid_stage_by_id(bid_stage_id: int) -> Optional[BidStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT a.*,
            b.status, b.description, b.created_date, b.completed, b.completed_at
            FROM bid_stage a
            INNER JOIN bid_stage_detail b ON a.bid_stage_id=b.bid_stage_id                
        WHERE a.bid_stage_id = %s
        ORDER BY a.stage_order;
        """
    cursor.execute(query, (bid_stage_id,))
    bid_stage = cursor.fetchone()

    conn.close()

    if bid_stage:
        return BidStage (
                bid_stage_id=bid_stage[0],
                tenant_id=bid_stage[1],
                rfx_id=bid_stage[2],
                default_name=bid_stage[3],
                new_name=bid_stage[4],
                stage_order=bid_stage[5],
                required=bid_stage[6],
                status=bid_stage[7],
                description=bid_stage[8],
                created_date=bid_stage[9],
                completed=bid_stage[10],
                completed_at=bid_stage[11]
            )
    
    else:
        return None


def get_bid_stage_by_name(tenant_id: int, rfx_id: int, default_name : str) -> Optional[BidStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT a.*,
            b.status, b.description, b.created_date, b.completed, b.completed_at
            FROM bid_stage a
            INNER JOIN bid_stage_detail b ON a.bid_stage_id=b.bid_stage_id                
        WHERE a.tenant_id = %s AND a.rfx_id = %s AND (lower(a.default_name) = %s OR lower(a.new_name) = %s);
        """
    cursor.execute(query, (tenant_id, rfx_id, default_name.lower(), default_name.lower()))
    bid_stage = cursor.fetchone()

    conn.close()

    if bid_stage:
        return BidStage(
                bid_stage_id=bid_stage[0],
                tenant_id=bid_stage[1],
                rfx_id=bid_stage[2],
                default_name=bid_stage[3],
                new_name=bid_stage[4],
                stage_order=bid_stage[5],
                required=bid_stage[6],
                status=bid_stage[7],
                description=bid_stage[8],
                created_date=bid_stage[9],
                completed=bid_stage[10],
                completed_at=bid_stage[11]
            )
    else:
        return None
    

def get_bid_stage_by_status(tenant_id: int, rfx_id: int, status : str) -> List[BidStage]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT a.*,
            b.status, b.description, b.created_date, b.completed, b.completed_at
            FROM bid_stage a
            INNER JOIN bid_stage_detail b ON a.bid_stage_id=b.bid_stage_id                
        WHERE a.tenant_id = %s AND a.rfx_id = %s AND lower(b.status) = %s
        ORDER BY a.stage_order;
        """
    cursor.execute(query, (tenant_id, rfx_id, status.lower(),))
    bid_stage_records = cursor.fetchall()

    conn.close()
    if bid_stage_records:
        return [
            BidStage (
                bid_stage_id=row[0],
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
            for row in bid_stage_records
        ]
    else:
        return None
