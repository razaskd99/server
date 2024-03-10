from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from phase_stages.schemas import BiddingPhasesCreate, BiddingPhases


def create_bidding_phases(item_form_data: BiddingPhasesCreate) -> BiddingPhases:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO bidding_phases (
        tenant_id,
        default_name,
        new_name,
        type,
        display_order,
        score,
        status,
        required
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        item_form_data.tenant_id,
        item_form_data.default_name,
        item_form_data.new_name,
        item_form_data.type,
        item_form_data.display_order,
        item_form_data.score,
        item_form_data.status,
        item_form_data.required
    )

    cursor.execute(query, values)
    new_item = cursor.fetchone()

    

    conn.commit()
    conn.close()

    if new_item:
        return BiddingPhases(
            bidding_phases_id=new_item[0],
            tenant_id=new_item[1],
            default_name=new_item[2],
            new_name=new_item[3],
            type=new_item[4],
            display_order=new_item[5],
            score=new_item[6],
            status=new_item[7],
            required=new_item[8]
        )
    else:
        raise HTTPException(status_code=404, detail="Bidding Phases Detail creation failed")

def get_all_bidding_phases(tenant_id: int) -> List[BiddingPhases]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bidding_phases WHERE tenant_id = %s 
        ORDER BY display_order;
        """

    cursor.execute(query,(tenant_id, ))
    query_all_items = cursor.fetchall()

    conn.close()
    if query_all_items:
        return [
            BiddingPhases(
            bidding_phases_id=row[0],
            tenant_id=row[1],
            default_name=row[2],
            new_name=row[3],
            type=row[4],
            display_order=row[5],
            score=row[6],
            status=row[7],
            required=row[8]
            )
            for row in query_all_items
        ]
    else:
        None

def update_bidding_phases(bidding_phases_id: int,  item_form_data: BiddingPhasesCreate) -> Optional[BiddingPhases]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bidding_phases SET 
        default_name = %s,
        new_name = %s,
        type = %s,
        display_order = %s,
        score = %s,
        status = %s,
        required = %s
    WHERE bidding_phases_id = %s RETURNING *;
    """

    values = (
        item_form_data.default_name,
        item_form_data.new_name,
        item_form_data.type,
        item_form_data.display_order,
        item_form_data.score,
        item_form_data.status,
        item_form_data.required,
        bidding_phases_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if updated_itemm:
        return BiddingPhases(
            bidding_phases_id=updated_itemm[0],
            tenant_id=updated_itemm[1],
            default_name=updated_itemm[2],
            new_name=updated_itemm[3],
            type=updated_itemm[4],
            display_order=updated_itemm[5],
            score=updated_itemm[6],
            status=updated_itemm[7],
            required=updated_itemm[8]
        )
    else:
        raise HTTPException(status_code=404, detail="Bidding Phases update failed")

def delete_bidding_phases(bid_validity_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM bidding_phases WHERE bidding_phases_id = %s RETURNING bidding_phases_id;"
    cursor.execute(query, (bid_validity_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False
    

def get_bidding_phases_by_id(bidding_phases_id: int) -> Optional[BiddingPhases]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bidding_phases WHERE bidding_phases_id = %s
        ORDER BY display_order; 
        """
    
    cursor.execute(query, (bidding_phases_id,))
    get_all_items = cursor.fetchone()

    conn.close()

    if get_all_items:
        return BiddingPhases(
            bidding_phases_id=get_all_items[0],
            tenant_id=get_all_items[1],
            default_name=get_all_items[2],
            new_name=get_all_items[3],
            type=get_all_items[4],
            display_order=get_all_items[5],
            score=get_all_items[6],
            status=get_all_items[7],
            required=get_all_items[8]
        )
    else:
        return None

def get_biding_phases_by_name(tenant_id: int, default_name : str) -> Optional[BiddingPhases]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bidding_phases WHERE tenant_id = %s AND (lower(default_name) = %s OR lower(new_name) = %s) 
        ORDER BY display_order;
        """
   
    cursor.execute(query, (tenant_id, default_name.lower(), default_name.lower() ))
    get_item = cursor.fetchone()

    conn.close()

    if get_item:
        return BiddingPhases(
            bidding_phases_id=get_item[0],
            tenant_id=get_item[1],
            default_name=get_item[2],
            new_name=get_item[3],
            type=get_item[4],
            display_order=get_item[5],
            score=get_item[6],
            status=get_item[7],
            required=get_item[8]
        )
    else:
        return None


def get_biding_phases_by_type(tenant_id: int, type : str) -> List[BiddingPhases]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bidding_phases WHERE tenant_id = %s AND lower(type) = %s 
        ORDER BY display_order;
        """
    
    cursor.execute(query, (tenant_id, type.lower()))
    get_item = cursor.fetchall()

    conn.close()

    if get_item:
        return [
            BiddingPhases(
            bidding_phases_id=row[0],
            tenant_id=row[1],
            default_name=row[2],
            new_name=row[3],
            type=row[4],
            display_order=row[5],
            score=row[6],
            status=row[7],
            required=row[8]
            )
            for row in get_item
        ]
    else:
        None

def get_biding_phases_by_status(tenant_id: int, status : str) -> List[BiddingPhases]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bidding_phases WHERE tenant_id = %s AND lower(status) = %s 
        ORDER BY display_order;
        """
   
    cursor.execute(query, (tenant_id, status.lower()))
    get_item = cursor.fetchall()

    conn.close()

    if get_item:
        return [
            BiddingPhases(
            bidding_phases_id=row[0],
            tenant_id=row[1],
            default_name=row[2],
            new_name=row[3],
            type=row[4],
            display_order=row[5],
            score=row[6],
            status=row[7],
            required=row[8]
            )
            for row in get_item
        ]
    else:
        None


def get_biding_phases_by_required(tenant_id: int) -> List[BiddingPhases]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bidding_phases WHERE tenant_id = %s AND required = %s 
        ORDER BY display_order;
        """

    cursor.execute(query, (tenant_id, True))
    get_item = cursor.fetchall()

    conn.close()

    if get_item:
        return [
            BiddingPhases(
            bidding_phases_id=row[0],
            tenant_id=row[1],
            default_name=row[2],
            new_name=row[3],
            type=row[4],
            display_order=row[5],
            score=row[6],
            status=row[7],
            required=row[8]
            )
            for row in get_item
        ]
    else:
        None


