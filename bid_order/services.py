from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import BidOrderCreate, BidOrder, BidOrderUpdate, BidOrderAcknowledgementUpdate

# Create a Bid Order
def create_bid_order(bid_order_data: BidOrderCreate) -> BidOrder:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_order (
        rfx_id, assign_to, acknowledged_by, acknowledgement_document, bid_order_num,
        title, currency, order_value, description, issued_date, delivery_date,
        acknowledgement_deadline, acknowledgement_comment, acknowledgement_date, acknowledged_on,
        acknowledged, order_complete
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) RETURNING *;
    """

    values = (
        bid_order_data.rfx_id, bid_order_data.assign_to, bid_order_data.acknowledged_by,
        bid_order_data.acknowledgement_document, bid_order_data.bid_order_num,
        bid_order_data.title, bid_order_data.currency, bid_order_data.order_value,
        bid_order_data.description, bid_order_data.issued_date, bid_order_data.delivery_date,
        bid_order_data.acknowledgement_deadline, bid_order_data.acknowledgement_comment,
        bid_order_data.acknowledgement_date, bid_order_data.acknowledged_on,
        bid_order_data.acknowledged, bid_order_data.order_complete
    )

    cursor.execute(query, values)
    new_bid_order = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_bid_order:
        return BidOrder(
            bid_order_id=new_bid_order[0],
            rfx_id=new_bid_order[1],
            assign_to=new_bid_order[2],
            acknowledged_by=new_bid_order[3],
            acknowledgement_document=new_bid_order[4],
            bid_order_num=new_bid_order[5],
            title=new_bid_order[6],
            currency=new_bid_order[7],
            order_value=new_bid_order[8],
            description=new_bid_order[9],
            issued_date=new_bid_order[10],
            delivery_date=new_bid_order[11],
            acknowledgement_deadline=new_bid_order[12],
            acknowledgement_comment=new_bid_order[13],
            acknowledgement_date=new_bid_order[14],
            acknowledged_on=new_bid_order[15],
            acknowledged=new_bid_order[16],
            order_complete=new_bid_order[17]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Order creation failed")

# Get  Bid Orders by id
def get_bid_orders_by_id(bid_order_id: int) -> Optional[BidOrder]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_order WHERE bid_order_id =%s ;"
    cursor.execute(query, (bid_order_id,))
    bid_orders = cursor.fetchone()

    conn.close()

    return BidOrder(
            bid_order_id=bid_orders[0],
            rfx_id=bid_orders[1],
            assign_to=bid_orders[2],
            acknowledged_by=bid_orders[3],
            acknowledgement_document=bid_orders[4],
            bid_order_num=bid_orders[5],
            title=bid_orders[6],
            currency=bid_orders[7],
            order_value=bid_orders[8],
            description=bid_orders[9],
            issued_date=bid_orders[10],
            delivery_date=bid_orders[11],
            acknowledgement_deadline=bid_orders[12],
            acknowledgement_comment=bid_orders[13],
            acknowledgement_date=bid_orders[14],
            acknowledged_on=bid_orders[15],
            acknowledged=bid_orders[16],
            order_complete=bid_orders[17]
        )
     

# Update Bid Order by ID
def update_bid_order(bid_order_id: int, new_data: BidOrderUpdate) -> Optional[BidOrder]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_order SET 
    assign_to = %s, bid_order_num = %s, title = %s, currency = %s,
    order_value = %s, description = %s, issued_date = %s, delivery_date = %s,
    order_complete = %s
    WHERE bid_order_id = %s RETURNING *;
    """

    values = (
        new_data.assign_to,
        new_data.bid_order_num,
        new_data.title,
        new_data.currency,
        new_data.order_value,
        new_data.description,
        new_data.issued_date,
        new_data.delivery_date, 
        new_data.order_complete,
        bid_order_id
    )

    cursor.execute(query, values)
    updated_bid_order = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_order:
        return BidOrder(
            bid_order_id=updated_bid_order[0],
            rfx_id=updated_bid_order[1],
            assign_to=updated_bid_order[2],
            acknowledged_by=updated_bid_order[3],
            acknowledgement_document=updated_bid_order[4],
            bid_order_num=updated_bid_order[5],
            title=updated_bid_order[6],
            currency=updated_bid_order[7],
            order_value=updated_bid_order[8],
            description=updated_bid_order[9],
            issued_date=updated_bid_order[10],
            delivery_date=updated_bid_order[11],
            acknowledgement_deadline=updated_bid_order[12],
            acknowledgement_comment=updated_bid_order[13],
            acknowledgement_date=updated_bid_order[14],
            acknowledged_on=updated_bid_order[15],
            acknowledged=updated_bid_order[16],
            order_complete=updated_bid_order[17]
        )
    else:
        return None
    

# Update Bid Order Acknowledgement by ID
def update_bid_order_acknowledgement(bid_order_id: int, new_data: BidOrderAcknowledgementUpdate) -> Optional[BidOrder]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_order SET 
    acknowledged_by = %s, acknowledgement_document = %s, acknowledgement_comment = %s, acknowledgement_date = %s,
    acknowledged_on = %s, acknowledged = %s
    WHERE bid_order_id = %s RETURNING *;
    """

    values = (
        new_data.acknowledged_by,
        new_data.acknowledgement_document,
        new_data.acknowledgement_comment,
        new_data.acknowledgement_date,
        new_data.acknowledged_on,
        new_data.acknowledged,
        bid_order_id
    )

    cursor.execute(query, values)
    updated_bid_order = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_order:
        return BidOrder(
            bid_order_id=updated_bid_order[0],
            rfx_id=updated_bid_order[1],
            assign_to=updated_bid_order[2],
            acknowledged_by=updated_bid_order[3],
            acknowledgement_document=updated_bid_order[4],
            bid_order_num=updated_bid_order[5],
            title=updated_bid_order[6],
            currency=updated_bid_order[7],
            order_value=updated_bid_order[8],
            description=updated_bid_order[9],
            issued_date=updated_bid_order[10],
            delivery_date=updated_bid_order[11],
            acknowledgement_deadline=updated_bid_order[12],
            acknowledgement_comment=updated_bid_order[13],
            acknowledgement_date=updated_bid_order[14],
            acknowledged_on=updated_bid_order[15],
            acknowledged=updated_bid_order[16],
            order_complete=updated_bid_order[17]
        )
    else:
        return None


# Delete Bid Order by ID
def delete_bid_order(bid_order_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM bid_order WHERE bid_order_id = %s RETURNING *;"
    cursor.execute(query, (bid_order_id,))
    deleted_bid_order = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_bid_order:
        return True
    else:
        return False


# Get Bid Order by ID and Title
def get_bid_order_by_title(rfx_id: int, title: str) -> Optional[BidOrder]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_order WHERE rfx_id = %s AND lower(title) = %s;"
    cursor.execute(query, (rfx_id, title.lower()))
    bid_order = cursor.fetchone()

    conn.close()

    return BidOrder(
            bid_order_id=bid_order[0],
            rfx_id=bid_order[1],
            assign_to=bid_order[2],
            acknowledged_by=bid_order[3],
            acknowledgement_document=bid_order[4],
            bid_order_num=bid_order[5],
            title=bid_order[6],
            currency=bid_order[7],
            order_value=bid_order[8],
            description=bid_order[9],
            issued_date=bid_order[10],
            delivery_date=bid_order[11],
            acknowledgement_deadline=bid_order[12],
            acknowledgement_comment=bid_order[13],
            acknowledgement_date=bid_order[14],
            acknowledged_on=bid_order[15],
            acknowledged=bid_order[16],
            order_complete=bid_order[17]
        )
      


# Get all Bid Orders by Rfx ID
def get_all_bid_orders_by_rfx_id(rfx_id: int) -> List[BidOrder]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_order WHERE rfx_id =%s ;"
    cursor.execute(query, (rfx_id,))
    bid_orders = cursor.fetchall()

    conn.close()

    return [
        BidOrder(
            bid_order_id=row[0],
            rfx_id=row[1],
            assign_to=row[2],
            acknowledged_by=row[3],
            acknowledgement_document=row[4],
            bid_order_num=row[5],
            title=row[6],
            currency=row[7],
            order_value=row[8],
            description=row[9],
            issued_date=row[10],
            delivery_date=row[11],
            acknowledgement_deadline=row[12],
            acknowledgement_comment=row[13],
            acknowledgement_date=row[14],
            acknowledged_on=row[15],
            acknowledged=row[16],
            order_complete=row[17]
        )
        for row in bid_orders
    ]


# Get all Bid Orders by Bid Order Number
def get_bid_orders_by_bid_order_num(rfx_id: int, bid_order_num: str) -> Optional[BidOrder]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_order WHERE rfx_id =%s AND bid_order_num = %s ;"
    cursor.execute(query, (rfx_id, bid_order_num))
    bid_orders = cursor.fetchone()

    conn.close()

    return BidOrder(
            bid_order_id=bid_orders[0],
            rfx_id=bid_orders[1],
            assign_to=bid_orders[2],
            acknowledged_by=bid_orders[3],
            acknowledgement_document=bid_orders[4],
            bid_order_num=bid_orders[5],
            title=bid_orders[6],
            currency=bid_orders[7],
            order_value=bid_orders[8],
            description=bid_orders[9],
            issued_date=bid_orders[10],
            delivery_date=bid_orders[11],
            acknowledgement_deadline=bid_orders[12],
            acknowledgement_comment=bid_orders[13],
            acknowledgement_date=bid_orders[14],
            acknowledged_on=bid_orders[15],
            acknowledged=bid_orders[16],
            order_complete=bid_orders[17]
        )
     
