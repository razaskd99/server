from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from phase_stages_detail.schemas import StagesDetailCreate, StagesDetail, GetStagesDetail


def create_stages_phases(item_form_data: StagesDetailCreate) -> GetStagesDetail:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO stages_detail(
        bidding_phases_id,
        rfx_id,
        stage_status,
        stage_score,
        completed,
        created_at,
        updated_at
    ) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        item_form_data.bidding_phases_id,
        item_form_data.rfx_id,
        item_form_data.stage_status,
        item_form_data.stage_score,
        item_form_data.completed,
        item_form_data.created_at,
        item_form_data.updated_at
    )

    cursor.execute(query, values)
    new_item = cursor.fetchone()
    id = new_item[0]
    query = """
        SELECT b.*,
            s.stages_detail_id, s.rfx_id, s.stage_status, s.stage_score, s.completed, s.created_at, s.updated_at 
            FROM bidding_phases b
        LEFT JOIN stages_detail s ON s.bidding_phases_id=b.bidding_phases_id             
        WHERE s.stages_detail_id = %s ;
        """

    cursor.execute(query, (id,))
    new_item = cursor.fetchone()
   
    conn.commit()
    conn.close()

    if new_item:
        return GetStagesDetail(
            bidding_phases_id=new_item[0],
            tenant_id=new_item[1],
            default_name=new_item[2],
            new_name=new_item[3],
            type=new_item[4],
            display_order=new_item[5],
            score=new_item[6],
            status=new_item[7],
            required=new_item[8],
            stages_detail_id=new_item[9],
            rfx_id=new_item[10],
            stage_status=new_item[11],
            stage_score=new_item[12],
            completed=new_item[13],
            created_at=new_item[14],
            updated_at=new_item[15]
            )
    else:
        raise HTTPException(status_code=404, detail="Stages Details creation failed")


def get_all_stages_detail(rfx_id: int) -> List[GetStagesDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*,
            s.stages_detail_id, s.rfx_id, s.stage_status, s.stage_score, s.completed, s.created_at, s.updated_at 
            FROM bidding_phases b
        LEFT JOIN stages_detail s ON s.bidding_phases_id=b.bidding_phases_id             
        WHERE s.rfx_id = %s ;
        """

    cursor.execute(query,(rfx_id, ))
    query_all_items = cursor.fetchall()

    conn.close()
    if query_all_items:
        return [
            GetStagesDetail(
            bidding_phases_id=row[0],
            tenant_id=row[1],
            default_name=row[2],
            new_name=row[3],
            type=row[4],
            display_order=row[5],
            score=row[6],
            status=row[7],
            required=row[8],
            stages_detail_id=row[9],
            rfx_id=row[10],
            stage_status=row[11],
            stage_score=row[12],
            completed=row[13],
            created_at=row[14],
            updated_at=row[15]
            )
            for row in query_all_items
        ]
    else:
        None

def update_stages_detail(stages_detail_id: int , item_form_data: StagesDetailCreate) -> Optional[GetStagesDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE stages_detail SET
        stage_status = %s,
        stage_score = %s,
        completed = %s,
        updated_at = %s
    WHERE stages_detail_id = %s RETURNING *;
    """

    values = (
        item_form_data.stage_status,
        item_form_data.stage_score,
        item_form_data.completed,
        item_form_data.updated_at,
        stages_detail_id
    )
    
    cursor.execute(query, values)
    new_item = cursor.fetchone()

    query = """
        SELECT b.*,
            s.stages_detail_id, s.rfx_id, s.stage_status, s.stage_score, s.completed, s.created_at, s.updated_at 
            FROM bidding_phases b
        LEFT JOIN stages_detail s ON s.bidding_phases_id=b.bidding_phases_id             
        WHERE s.stages_detail_id = %s ;
        """

    cursor.execute(query, (stages_detail_id,))
    new_item = cursor.fetchone()
   
    conn.commit()
    conn.close()

    if new_item:
        return GetStagesDetail(
            bidding_phases_id=new_item[0],
            tenant_id=new_item[1],
            default_name=new_item[2],
            new_name=new_item[3],
            type=new_item[4],
            display_order=new_item[5],
            score=new_item[6],
            status=new_item[7],
            required=new_item[8],
            stages_detail_id=new_item[9],
            rfx_id=new_item[10],
            stage_status=new_item[11],
            stage_score=new_item[12],
            completed=new_item[13],
            created_at=new_item[14],
            updated_at=new_item[15]
            )
    else:
        raise HTTPException(status_code=404, detail="Stages Detail update failed")
    
def delete_stages_detail(stages_detail_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM stages_detail WHERE stages_detail_id = %s RETURNING stages_detail_id;"
    cursor.execute(query, (stages_detail_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False

def get_stages_detail_by_id(stages_detail_id: int) -> Optional[GetStagesDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*,
            s.stages_detail_id, s.rfx_id, s.stage_status, s.stage_score, s.completed, s.created_at, s.updated_at 
            FROM bidding_phases b
        LEFT JOIN stages_detail s ON s.bidding_phases_id=b.bidding_phases_id             
        WHERE s.stages_detail_id = %s;
        """

    cursor.execute(query, (stages_detail_id,))
    get_all_items = cursor.fetchone()

    conn.close()

    if get_all_items:
        return GetStagesDetail(
            bidding_phases_id=get_all_items[0],
            tenant_id=get_all_items[1],
            default_name=get_all_items[2],
            new_name=get_all_items[3],
            type=get_all_items[4],
            display_order=get_all_items[5],
            score=get_all_items[6],
            status=get_all_items[7],
            required=get_all_items[8],
            stages_detail_id=get_all_items[9],
            rfx_id=get_all_items[10],
            stage_status=get_all_items[11],
            stage_score=get_all_items[12],
            completed=get_all_items[13],
            created_at=get_all_items[14],
            updated_at=get_all_items[15]
            )
        
    else:
        return None
    
def get_stages_detail_by_type(rfx_id: int, type: str) -> List[GetStagesDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*,
            s.stages_detail_id, s.rfx_id, s.stage_status, s.stage_score, s.completed, s.created_at, s.updated_at 
            FROM bidding_phases b
        LEFT JOIN stages_detail s ON s.bidding_phases_id=b.bidding_phases_id             
        WHERE s.rfx_id = %s AND lower(b.type) = %s 
        ORDER by b.display_order;
        """
    cursor.execute(query, (rfx_id,type.lower()))
    get_all_items = cursor.fetchall()

    conn.close()

    if get_all_items:
        return [
        GetStagesDetail(
            bidding_phases_id=row[0],
            tenant_id=row[1],
            default_name=row[2],
            new_name=row[3],
            type=row[4],
            display_order=row[5],
            score=row[6],
            status=row[7],
            required=row[8],
            stages_detail_id=row[9],
            rfx_id=row[10],
            stage_status=row[11],
            stage_score=row[12],
            completed=row[13],
            created_at=row[14],
            updated_at=row[15]
            )
            for row in get_all_items
        ]
    else:
        return None
    
def get_stages_detail_by_type_and_status(rfx_id: int, type: str, status: str) -> List[GetStagesDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*,
            s.stages_detail_id, s.rfx_id, s.stage_status, s.stage_score, s.completed, s.created_at, s.updated_at 
            FROM bidding_phases b
        LEFT JOIN stages_detail s ON s.bidding_phases_id=b.bidding_phases_id             
        WHERE s.rfx_id = %s AND lower(b.type) = %s AND lower(b.status) = %s;
        """
    cursor.execute(query, (rfx_id, type.lower(), status.lower()))
    get_all_items = cursor.fetchall()

    conn.close()

    if get_all_items:
        return [
        GetStagesDetail(
            bidding_phases_id=row[0],
            tenant_id=row[1],
            default_name=row[2],
            new_name=row[3],
            type=row[4],
            display_order=row[5],
            score=row[6],
            status=row[7],
            required=row[8],
            stages_detail_id=row[9],
            rfx_id=row[10],
            stage_status=row[11],
            stage_score=row[12],
            completed=row[13],
            created_at=row[14],
            updated_at=row[15]
            )
            for row in get_all_items
        ]
    else:
        return None
    
def get_stages_detail_by_type_and_name(rfx_id: int, type: str, default_name: str) -> Optional[GetStagesDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*,
            s.stages_detail_id, s.rfx_id, s.stage_status, s.stage_score, s.completed, s.created_at, s.updated_at 
            FROM bidding_phases b
        LEFT JOIN stages_detail s ON s.bidding_phases_id=b.bidding_phases_id             
        WHERE s.rfx_id = %s AND lower(b.type) = %s AND (lower(b.default_name) = %s OR lower(b.new_name) = %s) ;
        """
    cursor.execute(query, (rfx_id, type.lower(), default_name.lower(), default_name.lower()))
    get_all_items = cursor.fetchone()

    conn.close()

    if get_all_items:
        return GetStagesDetail(
            bidding_phases_id=get_all_items[0],
            tenant_id=get_all_items[1],
            default_name=get_all_items[2],
            new_name=get_all_items[3],
            type=get_all_items[4],
            display_order=get_all_items[5],
            score=get_all_items[6],
            status=get_all_items[7],
            required=get_all_items[8],
            stages_detail_id=get_all_items[9],
            rfx_id=get_all_items[10],
            stage_status=get_all_items[11],
            stage_score=get_all_items[12],
            completed=get_all_items[13],
            created_at=get_all_items[14],
            updated_at=get_all_items[15]
            )
            
        
    else:
        return None