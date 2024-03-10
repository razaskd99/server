from typing import List, Optional
from db.connection import get_db_connection
from .schemas import BidDocumentsMetaCreate, BidDocumentsMeta
from fastapi import HTTPException


def create_bid_document_meta(bid_document_meta_data: BidDocumentsMetaCreate) -> BidDocumentsMeta:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bid_documents_meta (
        rfx_id,
        bid_documents_id,
        bid_documents_post_id,
        meta_key,
        meta_id
    ) VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        bid_document_meta_data.rfx_id,
        bid_document_meta_data.bid_documents_id,
        bid_document_meta_data.bid_documents_post_id,
        bid_document_meta_data.meta_key,
        bid_document_meta_data.meta_id
    )

    cursor.execute(query, values)
    new_bid_document_meta = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_bid_document_meta:
        return BidDocumentsMeta(bid_documents_meta_id=new_bid_document_meta[0], **bid_document_meta_data.dict())
    else:
        raise HTTPException(status_code=404, detail="Bid Document Meta creation failed")


def get_all_bid_document_meta(bid_documents_id: int) -> List[BidDocumentsMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_documents_meta WHERE bid_documents_id = %s;"
    cursor.execute(query, (bid_documents_id,))
    bid_documents_meta = cursor.fetchall()

    conn.close()

    return [
        BidDocumentsMeta(
            bid_documents_meta_id=row[0],
            rfx_id=row[1],
            bid_documents_id=row[2],
            bid_documents_post_id=row[3],
            meta_key=row[4],
            meta_id=row[5]
        )
        for row in bid_documents_meta
    ]


def update_bid_document_meta(
    bid_documents_meta_id: int, bid_document_meta_data: BidDocumentsMetaCreate
) -> Optional[BidDocumentsMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_documents_meta SET
        meta_key = %s,
        meta_id = %s
    WHERE bid_documents_meta_id = %s RETURNING *;
    """

    values = (
        bid_document_meta_data.meta_key,
        bid_document_meta_data.meta_id,
        bid_documents_meta_id
    )

    cursor.execute(query, values)
    updated_bid_document_meta = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_bid_document_meta:
        return BidDocumentsMeta(
            bid_documents_meta_id=updated_bid_document_meta[0],
            rfx_id=updated_bid_document_meta[1],
            bid_documents_id=updated_bid_document_meta[2],
            bid_documents_post_id=updated_bid_document_meta[3],
            meta_key=updated_bid_document_meta[4],
            meta_id=updated_bid_document_meta[5],
        )
    else:
        return None


def delete_bid_document_meta(bid_documents_meta_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM bid_documents_meta WHERE bid_documents_meta_id = %s RETURNING bid_documents_meta_id;"
    cursor.execute(query, (bid_documents_meta_id,))
    deleted_bid_document_meta = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_bid_document_meta:
        return True
    else:
        return False


def get_bid_document_meta_by_id(bid_documents_meta_id: int) -> Optional[BidDocumentsMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_documents_meta WHERE bid_documents_meta_id = %s;"
    cursor.execute(query, (bid_documents_meta_id,))
    bid_document_meta = cursor.fetchone()

    conn.close()

    if bid_document_meta:
        return BidDocumentsMeta(
            bid_documents_meta_id=bid_document_meta[0],
            rfx_id=bid_document_meta[1],
            bid_documents_id=bid_document_meta[2],
            bid_documents_post_id=bid_document_meta[3],
            meta_key=bid_document_meta[4],
            meta_id=bid_document_meta[5]
        )
    else:
        return None


def get_bid_document_meta_by_bid_documents_post_id(bid_documents_post_id: int) -> List[BidDocumentsMeta]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM bid_documents_meta WHERE bid_documents_post_id = %s;"
    cursor.execute(query, (bid_documents_post_id,))
    bid_document_meta = cursor.fetchall()

    conn.close()

    return [
        BidDocumentsMeta(
            bid_documents_meta_id=row[0],
            rfx_id=row[1],
            bid_documents_id=row[2],
            bid_documents_post_id=row[3],
            meta_key=row[4],
            meta_id=row[5]
        )
        for row in bid_document_meta
    ]
