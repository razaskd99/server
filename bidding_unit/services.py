from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from bidding_unit.schemas import BiddingUnit, BiddingUnitCreate


def create_bidding_unit(item_form_data: BiddingUnitCreate) -> BiddingUnit:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO bidding_unit (
        tenant_id,
        title,
        active,
        created_at
    ) VALUES (%s, %s, %s, %s) RETURNING *;
    """

    values = (
        item_form_data.tenant_id,
        item_form_data.title,
        item_form_data.active,
        item_form_data.created_at
    )

    cursor.execute(query, values)
    new_item = cursor.fetchone()

   
    conn.commit()
    conn.close()

    if new_item:
        return BiddingUnit(
            bidding_unit_id=new_item[0],
            tenant_id=new_item[1],
            title=new_item[2],
            active=new_item[3],
            created_at=new_item[4]
        )
    else:
        raise HTTPException(status_code=404, detail="Bidding Unit creation failed")


def get_all_bidding_unit(tenant_id: int,  searchTerm: str, offset: int, limit: int) :
    conn = get_db_connection()
    cursor = conn.cursor()

    if searchTerm:
        searchTerm = '%' + searchTerm.lower() + '%'
        query = """
            SELECT * FROM bidding_unit             
            WHERE tenant_id = %s AND lower(title) LIKE %s
            ORDER BY created_at DESC
            OFFSET %s LIMIT %s;
            """
        cursor.execute(query,(tenant_id, searchTerm, offset, limit))
        query_all_items = cursor.fetchall()
    else:
        searchTerm = '%' + searchTerm.lower() + '%'
        query = """
            SELECT * FROM bidding_unit             
            WHERE tenant_id = %s
            ORDER BY created_at DESC
            OFFSET %s LIMIT %s;
            """
        cursor.execute(query,(tenant_id, offset, limit))
        query_all_items = cursor.fetchall()

    # Query to get total count without offset and limit
    query_total_count = "SELECT COUNT(*) FROM bidding_unit WHERE tenant_id = %s;"
    cursor.execute(query_total_count, (tenant_id, ))
    total_count = cursor.fetchone()    
    conn.close()
    
    if query_all_items:
        return {
            "data":[
                BiddingUnit(
                    bidding_unit_id=row[0],
                    tenant_id=row[1],
                    title=row[2],
                    active=row[3],
                    created_at=row[4]
                )
                for row in query_all_items
            ],
            "total_count": total_count
        }
    else:
        None


def update_bidding_unit(bidding_unit_id: int,  item_form_data: BiddingUnitCreate) -> Optional[BiddingUnit]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bidding_unit SET 
        title = %s,
        active = %s
    WHERE bidding_unit_id = %s RETURNING *;
    """

    values = (
        item_form_data.title,
        item_form_data.active,
        bidding_unit_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return BiddingUnit(
            bidding_unit_id=updated_itemm[0],
            tenant_id=updated_itemm[1],
            title=updated_itemm[2],
            active=updated_itemm[3],
            created_at=updated_itemm[4]
        )
    else:
        raise HTTPException(status_code=404, detail="Bidding Unit update failed")


def delete_bidding_unit(bidding_unit_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM bidding_unit WHERE bidding_unit_id = %s RETURNING bidding_unit_id;"
    cursor.execute(query, (bidding_unit_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False
    
def delete_all_bidding_unit(tenant_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM bidding_unit WHERE tenant_id = %s RETURNING bidding_unit_id;"
    cursor.execute(query, (tenant_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False


def get_bidding_unit_by_id(bidding_unit_id: int) -> Optional[BiddingUnit]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bidding_unit WHERE bidding_unit_id = %s;"

    cursor.execute(query, (bidding_unit_id,))
    get_all_items = cursor.fetchone()

    conn.close()

    if get_all_items:
        return BiddingUnit (
                bidding_unit_id=get_all_items[0],
                tenant_id=get_all_items[1],
                title=get_all_items[2],
                active=get_all_items[3],
                created_at=get_all_items[4]
            )
    else:
        return None


