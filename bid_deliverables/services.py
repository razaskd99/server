from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from bid_deliverables.schemas import BidDeliverablesCreate, BidDeliverables


def create_bid_deliverables(bid_deliverables_data: BidDeliverablesCreate) -> BidDeliverables:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO bid_deliverables (
        rfx_id,
        title,
        description,
        template,
        template_type,
        created_by,
        created_on
    ) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_deliverables_data.rfx_id,
        bid_deliverables_data.title,
        bid_deliverables_data.description,
        bid_deliverables_data.template,
        bid_deliverables_data.template_type,
        bid_deliverables_data.created_by,
        bid_deliverables_data.created_on          
    )

    cursor.execute(query, values)
    new_bid_deliverables = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_bid_deliverables:
        return BidDeliverables(
            bid_deliverables_id=new_bid_deliverables[0],
            rfx_id=new_bid_deliverables[1],
            title=new_bid_deliverables[2],
            description=new_bid_deliverables[3],
            template=new_bid_deliverables[4],
            template_type=new_bid_deliverables[5],
            created_by=new_bid_deliverables[6],
            created_on=new_bid_deliverables[7],
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Deliverables creation failed")


def get_all_bid_deliverables(rfx_id: int) -> List[BidDeliverables]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bid_deliverables WHERE rfx_id = %s
        ORDER BY created_on DESC;
        """

    cursor.execute(query,(rfx_id,))
    bid_deliverables = cursor.fetchall()

    conn.close()
    if bid_deliverables:
        return [
            BidDeliverables(
                bid_deliverables_id=row[0],
                rfx_id=row[1],
                title=row[2],
                description=row[3],
                template=row[4],
                template_type=row[5],
                created_by=row[6],
                created_on=row[7]
            )
            for row in bid_deliverables
        ]
    else:
        None


def update_bid_deliverables(bid_deliverables_id: int, bid_deliverables_data: BidDeliverablesCreate) -> Optional[BidDeliverables]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_deliverables SET 
        title = %s,
        description = %s,
        template = %s,
        template_type = %s
    WHERE bid_deliverables_id = %s RETURNING *;
    """

    values = (
        bid_deliverables_data.title,
        bid_deliverables_data.description,
        bid_deliverables_data.template,
        bid_deliverables_data.template_type,
        bid_deliverables_id
    )

    cursor.execute(query, values)
    updated_bid_deliverables = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_deliverables:
        return BidDeliverables(
            bid_deliverables_id=updated_bid_deliverables[0],
            rfx_id=updated_bid_deliverables[1],
            title=updated_bid_deliverables[2],
            description=updated_bid_deliverables[3],
            template=updated_bid_deliverables[4],
            template_type=updated_bid_deliverables[5],
            created_by=updated_bid_deliverables[6],
            created_on=updated_bid_deliverables[7]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Deliverables update failed")


def delete_bid_deliverables(bid_deliverables_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "DELETE FROM bid_deliverables WHERE bid_deliverables_id = %s RETURNING bid_deliverables_id;"
    cursor.execute(query, (bid_deliverables_id,))
    deleted_bid_deliverables = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_bid_deliverables:
        return True
    else:
        return False


def get_bid_deliverables_by_id(bid_deliverables_id: int) -> Optional[BidDeliverables]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM bid_deliverables WHERE bid_deliverables_id = %s
        ORDER BY created_on DESC;
        """
        
    cursor.execute(query, (bid_deliverables_id,))
    bid_deliverables = cursor.fetchone()

    conn.close()

    if bid_deliverables:
        return BidDeliverables (
                bid_deliverables_id=bid_deliverables[0],
                rfx_id=bid_deliverables[1],
                title=bid_deliverables[2],
                description=bid_deliverables[3],
                template=bid_deliverables[4],
                template_type=bid_deliverables[5],
                created_by=bid_deliverables[6],
                created_on=bid_deliverables[7]
            )
    
    else:
        return None


