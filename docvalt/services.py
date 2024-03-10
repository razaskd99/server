from typing import Optional, List
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import DocValtCreate, DocValt
from datetime import date, datetime

def create_docvalt(docvalt_data: DocValtCreate) -> DocValt:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO docvalt (
        tenant_id,
        rfx_id,
        user_id,
        docvalt_key,
        docvalt_dir,
        docvalt_filename,
        docvalt_cloudpath,
        file_type,
        file_size,
        file_moved,
        created_date,
        created_at,
        updated_at
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        docvalt_data.tenant_id,
        docvalt_data.rfx_id,
        docvalt_data.user_id,
        docvalt_data.docvalt_key,
        docvalt_data.docvalt_dir,
        docvalt_data.docvalt_filename,
        docvalt_data.docvalt_cloudpath,
        docvalt_data.file_type,
        docvalt_data.file_size,
        docvalt_data.file_moved,
        docvalt_data.created_date,
        docvalt_data.created_at,
        docvalt_data.updated_at,
    )

    cursor.execute(query, values)
    new_docvalt = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_docvalt:
        return DocValt(
            docvalt_id=new_docvalt[0],
            tenant_id=new_docvalt[1],
            rfx_id=new_docvalt[2],
            user_id=new_docvalt[3],
            docvalt_key=new_docvalt[4],
            docvalt_dir=new_docvalt[5],
            docvalt_filename=new_docvalt[6],
            docvalt_cloudpath=new_docvalt[7],
            file_type=new_docvalt[8],
            file_size=new_docvalt[9],
            file_moved=new_docvalt[10],
            created_date=new_docvalt[11],
            created_at=new_docvalt[12],
            updated_at=new_docvalt[13],
        )
    else:
        raise HTTPException(status_code=404, detail="DocValt creation failed")


def get_all_docvalts(tenant_id: int) -> List[DocValt]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM docvalt WHERE tenant_id = %s;"
    cursor.execute(query,(tenant_id,))
    docvalts = cursor.fetchall()

    conn.close()

    return [
        DocValt(
            docvalt_id=row[0],
            tenant_id=row[1],
            rfx_id=row[2],
            user_id=row[3],
            docvalt_key=row[4],
            docvalt_dir=row[5],
            docvalt_filename=row[6],
            docvalt_cloudpath=row[7],
            file_type=row[8],
            file_size=row[9],
            file_moved=row[10],
            created_date=row[11],
            created_at=row[12],
            updated_at=row[13]
        )
        for row in docvalts
    ]


def get_docvalt_by_id(docvalt_id: int) -> Optional[DocValt]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM docvalt WHERE docvalt_id = %s;"
    cursor.execute(query, (docvalt_id,))
    docvalt = cursor.fetchone()

    conn.close()

    if docvalt:
        return DocValt(
            docvalt_id=docvalt[0],
            tenant_id=docvalt[1],
            rfx_id=docvalt[2],
            user_id=docvalt[3],
            docvalt_key=docvalt[4],
            docvalt_dir=docvalt[5],
            docvalt_filename=docvalt[6],
            docvalt_cloudpath=docvalt[7],
            file_type=docvalt[8],
            file_size=docvalt[9],
            file_moved=docvalt[10],
            created_date=docvalt[11],
            created_at=docvalt[12],
            updated_at=docvalt[13]
        )
    else:
        return None



def update_docvalt(docvalt_id: int, docvalt_data: DocValtCreate) -> Optional[DocValt]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE docvalt SET 
        docvalt_key = %s,
        docvalt_dir = %s,
        docvalt_filename = %s,
        docvalt_cloudpath = %s,
        file_type = %s,
        file_size = %s,
        file_moved = %s,
        created_date = %s,
        created_at = %s,
        updated_at = %s
    WHERE docvalt_id = %s RETURNING *;
    """

    values = (
        docvalt_data.docvalt_key,
        docvalt_data.docvalt_dir,
        docvalt_data.docvalt_filename,
        docvalt_data.docvalt_cloudpath,
        docvalt_data.file_type,
        docvalt_data.file_size,
        docvalt_data.file_moved,
        docvalt_data.created_date,
        docvalt_data.created_at,
        docvalt_data.updated_at,
        docvalt_id,
    )

    cursor.execute(query, values)
    updated_docvalt = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_docvalt:
        return DocValt(
            docvalt_id=updated_docvalt[0],
            tenant_id=updated_docvalt[1],
            rfx_id=updated_docvalt[2],
            user_id=updated_docvalt[3],
            docvalt_key=updated_docvalt[4],
            docvalt_dir=updated_docvalt[5],
            docvalt_filename=updated_docvalt[6],
            docvalt_cloudpath=updated_docvalt[7],
            file_type=updated_docvalt[8],
            file_size=updated_docvalt[9],
            file_moved=True if updated_docvalt[10] else False,
            created_date=updated_docvalt[11],
            created_at=updated_docvalt[12],
            updated_at=updated_docvalt[13]
        )
    else:
        return None


def delete_docvalt(docvalt_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM docvalt WHERE docvalt_id = %s RETURNING docvalt_id;"
    cursor.execute(query, (docvalt_id,))
    deleted_docvalt = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_docvalt:
        return True
    else:
        return False

def get_all_docvalts_by_rfx_id(tenant_id: int, rfx_id: int) -> List[DocValt]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM docvalt WHERE tenant_id = %s AND rfx_id = %s;"
    cursor.execute(query,(tenant_id, rfx_id))
    docvalts = cursor.fetchall()

    conn.close()

    return [
        DocValt(
            docvalt_id=row[0],
            tenant_id=row[1],
            rfx_id=row[2],
            user_id=row[3],
            docvalt_key=row[4],
            docvalt_dir=row[5],
            docvalt_filename=row[6],
            docvalt_cloudpath=row[7],
            file_type=row[8],
            file_size=row[9],
            file_moved=row[10],
            created_date=row[11],
            created_at=row[12],
            updated_at=row[13]
        )
        for row in docvalts
    ]
    
def get_docvalt_by_docvalt_key(tenant_id: int, docvalt_key: str) -> List[DocValt]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM docvalt WHERE tenant_id = %s AND lower(docvalt_key) = %s;"
    cursor.execute(query, (tenant_id, docvalt_key.lower()))
    docvalt = cursor.fetchall()

    conn.close()

    if docvalt:
        return [
            DocValt(
                docvalt_id=row[0],
                tenant_id=row[1],
                rfx_id=row[2],
                user_id=row[3],
                docvalt_key=row[4],
                docvalt_dir=row[5],
                docvalt_filename=row[6],
                docvalt_cloudpath=row[7],
                file_type=row[8],
                file_size=row[9],
                file_moved=True if row[10] else False,
                created_date=row[11],
                created_at=row[12],
                updated_at=row[13]
            )
            for row in docvalt
        ]
    else:
        return None

def get_docvalt_by_user_id(tenant_id: int, user_id: int) -> List[DocValt]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM docvalt WHERE tenant_id = %s AND user_id = %s;"
    cursor.execute(query, (tenant_id, user_id))
    docvalt = cursor.fetchall()

    conn.close()

    if docvalt:
        return [
            DocValt(
                docvalt_id=row[0],
                tenant_id=row[1],
                rfx_id=row[2],
                user_id=row[3],
                docvalt_key=row[4],
                docvalt_dir=row[5],
                docvalt_filename=row[6],
                docvalt_cloudpath=row[7],
                file_type=row[8],
                file_size=row[9],
                file_moved=True if row[10] else False,
                created_date=row[11],
                created_at=row[12],
                updated_at=row[13]
            )
            for row in docvalt
        ]
    else:
        return None
    

def get_docvalt_by_file_name(tenant_id: int, docvalt_filename: str) -> List[DocValt]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM docvalt WHERE tenant_id = %s AND docvalt_filename = %s;"
    cursor.execute(query,(tenant_id, docvalt_filename))
    docvalts = cursor.fetchall()

    conn.close()

    return [
        DocValt(
            docvalt_id=row[0],
            tenant_id=row[1],
            rfx_id=row[2],
            user_id=row[3],
            docvalt_key=row[4],
            docvalt_dir=row[5],
            docvalt_filename=row[6],
            docvalt_cloudpath=row[7],
            file_type=row[8],
            file_size=row[9],
            file_moved=row[10],
            created_date=row[11],
            created_at=row[12],
            updated_at=row[13]
        )
        for row in docvalts
    ]
    

def get_docvalt_by_RfxID_key(rfx_id: int, key: str) -> List[DocValt]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM docvalt WHERE rfx_id = %s AND docvalt_key = %s;"
    cursor.execute(query,(rfx_id, key))
    docvalts = cursor.fetchall()

    conn.close()

    return [
        DocValt(
            docvalt_id=row[0],
            tenant_id=row[1],
            rfx_id=row[2],
            user_id=row[3],
            docvalt_key=row[4],
            docvalt_dir=row[5],
            docvalt_filename=row[6],
            docvalt_cloudpath=row[7],
            file_type=row[8],
            file_size=row[9],
            file_moved=row[10],
            created_date=row[11],
            created_at=row[12],
            updated_at=row[13]
        )
        for row in docvalts
    ]