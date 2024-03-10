from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from bid_validity.schemas import BidValidityCreate, BidValidity


def create_bid_validity(item_form_data: BidValidityCreate) -> BidValidity:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO bid_validity (
        tenant_id,
        title,
        is_active,
        alias
    ) VALUES (%s, %s, %s, %s) RETURNING *;
    """

    values = (
        item_form_data.tenant_id,
        item_form_data.title,
        item_form_data.is_active,
        item_form_data.alias
    )

    cursor.execute(query, values)
    new_item = cursor.fetchone()

   
    conn.commit()
    conn.close()

    if new_item:
        return BidValidity(
            bid_validity_id=new_item[0],
            tenant_id=new_item[1],
            title=new_item[2],
            is_active=new_item[3],
            alias=new_item[4]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Validity Detail creation failed")


def get_all_bid_validity(tenant_id: int) -> List[BidValidity]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bid_validity              
        WHERE tenant_id = %s ;
        """

    cursor.execute(query,(tenant_id, ))
    query_all_items = cursor.fetchall()

    conn.close()
    if query_all_items:
        return [
            BidValidity(
                bid_validity_id=row[0],
                tenant_id=row[1],
                title=row[2],
                is_active=row[3],
                alias=row[4]
            )
            for row in query_all_items
        ]
    else:
        None


def update_bid_validity(bid_validity_id: int,  item_form_data: BidValidityCreate) -> Optional[BidValidity]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_validity SET 
        title = %s,
        is_active = %s,
        alias = %s
    WHERE bid_validity_id = %s RETURNING *;
    """

    values = (
        item_form_data.title,
        item_form_data.is_active,
        item_form_data.alias,
        bid_validity_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return BidValidity(
            bid_validity_id=updated_itemm[0],
            tenant_id=updated_itemm[1],
            title=updated_itemm[2],
            is_active=updated_itemm[3],
            alias=updated_itemm[4]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Validity update failed")


def delete_bid_validity(bid_validity_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM bid_validity WHERE bid_validity_id = %s RETURNING bid_validity_id;"
    cursor.execute(query, (bid_validity_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False
    
def delete_all_bid_validity(tenant_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM bid_validity WHERE tenant_id = %s RETURNING bid_validity_id;"
    cursor.execute(query, (tenant_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False


def get_bid_validity_by_id(bid_validity_id: int) -> Optional[BidValidity]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_validity WHERE bid_validity_id = %s ;"

    cursor.execute(query, (bid_validity_id,))
    get_all_items = cursor.fetchone()

    conn.close()

    if get_all_items:
        return BidValidity (
                bid_validity_id=get_all_items[0],
                tenant_id=get_all_items[1],
                title=get_all_items[2],
                is_active=get_all_items[3],
                alias=get_all_items[4]
            )
    else:
        return None


def get_bid_validity_by_name(title : str, tenant_id: int) -> Optional[BidValidity]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_validity WHERE lower(title) = %s AND tenant_id = %s RETURNING *;"

    cursor.execute(query, (title.lower(), tenant_id))
    get_item = cursor.fetchone()

    conn.close()

    if get_item:
        return BidValidity(
                bid_validity_id=get_item[0],
                tenant_id=get_item[1],
                rfx_id=get_item[2],
                title=get_item[3],
                is_active=get_item[4]
            )
    else:
        return None
    

def get_all_active_bid_validity( tenant_id: int) -> List[BidValidity]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_validity WHERE is_active = %s AND tenant_id = %s;"

    cursor.execute(query, (True, tenant_id,))
    all_records = cursor.fetchall()

    conn.close()
    if all_records:
        return [
            BidValidity (
                bid_validity_id=row[0],
                tenant_id=row[1],
                title=row[2],
                is_active=row[3],
                alias=row[4]
            )
            for row in all_records
        ]
    else:
        return None
    

def get_all_bid_validity_by_alias( tenant_id: int, alias: str) -> Optional[BidValidity]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_validity WHERE tenant_id = %s AND alias = %s;"

    cursor.execute(query, (tenant_id, alias,))
    all_records = cursor.fetchall()

    conn.close()
    if all_records:
        return [
            BidValidity (
                bid_validity_id=row[0],
                tenant_id=row[1],
                title=row[2],
                is_active=row[3],
                alias=row[4]
            )
            for row in all_records
        ]
    else:
        return None
