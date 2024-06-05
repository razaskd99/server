from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from rfx_detail.schemas import RfxDetailCreate, RfxDetail, SkipDetailUpdate, SkipFinalUpdate, SkipOrderUpdate, SkipPrelimUpdate


def create_rfx_detail(item_form_data: RfxDetailCreate) -> RfxDetail:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO rfx_detail (
        rfx_id,
        skip_prelim,
        skip_prelim_reason,
        skip_detail,
        skip_detail_reason,
        skip_final,
        skip_final_reason,
        skip_order,
        skip_order_reason,
        skip_rfx_clarif,
        skip_rfx_clarif_reason,
        skip_bid_clarif,
        skip_bid_clarif_reason,
        created_on,
        updated_on
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        item_form_data.rfx_id,
        item_form_data.skip_prelim,
        item_form_data.skip_prelim_reason,
        item_form_data.skip_detail,
        item_form_data.skip_detail_reason,
        item_form_data.skip_final,
        item_form_data.skip_final_reason,
        item_form_data.skip_order,
        item_form_data.skip_order_reason,        
        item_form_data.skip_rfx_clarif,
        item_form_data.skip_rfx_clarif_reason,
        item_form_data.skip_bid_clarif,
        item_form_data.skip_bid_clarif_reason,        
        item_form_data.created_on,
        item_form_data.updated_on
    )

    cursor.execute(query, values)
    new_item = cursor.fetchone()

   
    conn.commit()
    conn.close()

    if new_item:
        return RfxDetail(
            rfx_detail_id=new_item[0],
            rfx_id=new_item[1],
            skip_prelim=new_item[2],
            skip_prelim_reason=new_item[3],
            skip_detail=new_item[4],
            skip_detail_reason=new_item[5],
            skip_final=new_item[6],
            skip_final_reason=new_item[7],
            skip_order=new_item[8],
            skip_order_reason=new_item[9],            
            skip_rfx_clarif=new_item[10],
            skip_rfx_clarif_reason=new_item[11],
            skip_bid_clarif=new_item[12],
            skip_bid_clarif_reason=new_item[13], 
            created_on=new_item[14],
            updated_on=new_item[15]
        )
    else:
        raise HTTPException(status_code=404, detail="RFx Detail creation failed")


def get_rfx_detail(rfx_id: int) -> Optional[RfxDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM rfx_detail              
        WHERE rfx_id = %s;
        """

    cursor.execute(query,(rfx_id, ))
    query_all_items = cursor.fetchone()

    conn.close()
    if query_all_items:
        return RfxDetail(
            rfx_detail_id=query_all_items[0],
            rfx_id=query_all_items[1],
            skip_prelim=query_all_items[2],
            skip_prelim_reason=query_all_items[3],
            skip_detail=query_all_items[4],
            skip_detail_reason=query_all_items[5],
            skip_final=query_all_items[6],
            skip_final_reason=query_all_items[7],
            skip_order=query_all_items[8],
            skip_order_reason=query_all_items[9],            
            skip_rfx_clarif=query_all_items[10],
            skip_rfx_clarif_reason=query_all_items[11],
            skip_bid_clarif=query_all_items[12],
            skip_bid_clarif_reason=query_all_items[13],             
            created_on=query_all_items[14],
            updated_on=query_all_items[15]
        )
    else:
        None


def update_skip_prelim(rfx_id: int,  item_form_data: SkipPrelimUpdate) -> Optional[RfxDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE rfx_detail SET 
        skip_prelim = %s,
        skip_prelim_reason = %s,
        updated_on = %s
    WHERE rfx_id = %s RETURNING *;
    """

    values = (
        item_form_data.skip_prelim,
        item_form_data.skip_prelim_reason,
        item_form_data.updated_on,
        rfx_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return RfxDetail(
            rfx_detail_id=updated_itemm[0],
            rfx_id=updated_itemm[1],
            skip_prelim=updated_itemm[2],
            skip_prelim_reason=updated_itemm[3],
            skip_detail=updated_itemm[4],
            skip_detail_reason=updated_itemm[5],
            skip_final=updated_itemm[6],
            skip_final_reason=updated_itemm[7],
            skip_order=updated_itemm[8],
            skip_order_reason=updated_itemm[9],
            skip_rfx_clarif=updated_itemm[10],
            skip_rfx_clarif_reason=updated_itemm[11],
            skip_bid_clarif=updated_itemm[12],
            skip_bid_clarif_reason=updated_itemm[13], 
            created_on=updated_itemm[14],
            updated_on=updated_itemm[15]
        )
    else:
        raise HTTPException(status_code=404, detail="RFx Detail update failed")


def update_skip_detail(rfx_id: int,  item_form_data: SkipDetailUpdate) -> Optional[RfxDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE rfx_detail SET 
        skip_detail = %s,
        skip_detail_reason = %s,
        updated_on = %s
    WHERE rfx_id = %s RETURNING *;
    """

    values = (
        item_form_data.skip_detail,
        item_form_data.skip_detail_reason,
        item_form_data.updated_on,
        rfx_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return RfxDetail(
            rfx_detail_id=updated_itemm[0],
            rfx_id=updated_itemm[1],
            skip_prelim=updated_itemm[2],
            skip_prelim_reason=updated_itemm[3],
            skip_detail=updated_itemm[4],
            skip_detail_reason=updated_itemm[5],
            skip_final=updated_itemm[6],
            skip_final_reason=updated_itemm[7],
            skip_order=updated_itemm[8],
            skip_order_reason=updated_itemm[9],
            skip_rfx_clarif=updated_itemm[10],
            skip_rfx_clarif_reason=updated_itemm[11],
            skip_bid_clarif=updated_itemm[12],
            skip_bid_clarif_reason=updated_itemm[13], 
            created_on=updated_itemm[14],
            updated_on=updated_itemm[15]
        )
    else:
        raise HTTPException(status_code=404, detail="RFx Detail update failed")
    

def update_skip_final(rfx_id: int,  item_form_data: SkipFinalUpdate) -> Optional[RfxDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE rfx_detail SET 
        skip_final = %s,
        skip_final_reason = %s,
        updated_on = %s
    WHERE rfx_id = %s RETURNING *;
    """

    values = (
        item_form_data.skip_final,
        item_form_data.skip_final_reason,
        item_form_data.updated_on,
        rfx_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return RfxDetail(
            rfx_detail_id=updated_itemm[0],
            rfx_id=updated_itemm[1],
            skip_prelim=updated_itemm[2],
            skip_prelim_reason=updated_itemm[3],
            skip_detail=updated_itemm[4],
            skip_detail_reason=updated_itemm[5],
            skip_final=updated_itemm[6],
            skip_final_reason=updated_itemm[7],
            skip_order=updated_itemm[8],
            skip_order_reason=updated_itemm[9],
            skip_rfx_clarif=updated_itemm[10],
            skip_rfx_clarif_reason=updated_itemm[11],
            skip_bid_clarif=updated_itemm[12],
            skip_bid_clarif_reason=updated_itemm[13], 
            created_on=updated_itemm[14],
            updated_on=updated_itemm[15]
        )
    else:
        raise HTTPException(status_code=404, detail="RFx Detail update failed")


def update_skip_order(rfx_id: int,  item_form_data: SkipOrderUpdate) -> Optional[RfxDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE rfx_detail SET 
        skip_order = %s,
        skip_order_reason = %s,
        updated_on = %s
    WHERE rfx_id = %s RETURNING *;
    """

    values = (
        item_form_data.skip_order,
        item_form_data.skip_order_reason,
        item_form_data.updated_on,
        rfx_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return RfxDetail(
            rfx_detail_id=updated_itemm[0],
            rfx_id=updated_itemm[1],
            skip_prelim=updated_itemm[2],
            skip_prelim_reason=updated_itemm[3],
            skip_detail=updated_itemm[4],
            skip_detail_reason=updated_itemm[5],
            skip_final=updated_itemm[6],
            skip_final_reason=updated_itemm[7],
            skip_order=updated_itemm[8],
            skip_order_reason=updated_itemm[9],
            skip_rfx_clarif=updated_itemm[10],
            skip_rfx_clarif_reason=updated_itemm[11],
            skip_bid_clarif=updated_itemm[12],
            skip_bid_clarif_reason=updated_itemm[13], 
            created_on=updated_itemm[14],
            updated_on=updated_itemm[15]
        )
    else:
        raise HTTPException(status_code=404, detail="RFx Detail update failed")


def update_skip_rfx_clarif(rfx_id: int,  item_form_data: SkipOrderUpdate) -> Optional[RfxDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE rfx_detail SET 
        skip_rfx_clarif = %s,
        skip_rfx_clarif_reason = %s,
        updated_on = %s
    WHERE rfx_id = %s RETURNING *;
    """

    values = (
        item_form_data.skip_rfx_clarif,
        item_form_data.skip_rfx_clarif_reason,
        item_form_data.updated_on,
        rfx_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return RfxDetail(
            rfx_detail_id=updated_itemm[0],
            rfx_id=updated_itemm[1],
            skip_prelim=updated_itemm[2],
            skip_prelim_reason=updated_itemm[3],
            skip_detail=updated_itemm[4],
            skip_detail_reason=updated_itemm[5],
            skip_final=updated_itemm[6],
            skip_final_reason=updated_itemm[7],
            skip_order=updated_itemm[8],
            skip_order_reason=updated_itemm[9],
            skip_rfx_clarif=updated_itemm[10],
            skip_rfx_clarif_reason=updated_itemm[11],
            skip_bid_clarif=updated_itemm[12],
            skip_bid_clarif_reason=updated_itemm[13], 
            created_on=updated_itemm[14],
            updated_on=updated_itemm[15]
        )
    else:
        raise HTTPException(status_code=404, detail="RFx Detail update failed")


def update_skip_bid_clarif(rfx_id: int,  item_form_data: SkipOrderUpdate) -> Optional[RfxDetail]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE rfx_detail SET 
        skip_bid_clarif = %s,
        skip_bid_clarif_reason = %s,
        updated_on = %s
    WHERE rfx_id = %s RETURNING *;
    """

    values = (
        item_form_data.skip_bid_clarif,
        item_form_data.skip_bid_clarif_reason,
        item_form_data.updated_on,
        rfx_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return RfxDetail(
            rfx_detail_id=updated_itemm[0],
            rfx_id=updated_itemm[1],
            skip_prelim=updated_itemm[2],
            skip_prelim_reason=updated_itemm[3],
            skip_detail=updated_itemm[4],
            skip_detail_reason=updated_itemm[5],
            skip_final=updated_itemm[6],
            skip_final_reason=updated_itemm[7],
            skip_order=updated_itemm[8],
            skip_order_reason=updated_itemm[9],
            skip_rfx_clarif=updated_itemm[10],
            skip_rfx_clarif_reason=updated_itemm[11],
            skip_bid_clarif=updated_itemm[12],
            skip_bid_clarif_reason=updated_itemm[13], 
            created_on=updated_itemm[14],
            updated_on=updated_itemm[15]
        )
    else:
        raise HTTPException(status_code=404, detail="RFx Detail update failed")
    


def delete_rfx_detail(rfx_detail_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM rfx_detail WHERE rfx_detail_id = %s RETURNING rfx_detail_id;"
    cursor.execute(query, (rfx_detail_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False
    
