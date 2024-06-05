from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from account_type_entries.schemas import AccountTypeEntries, AccountTypeEntriesCreate, AccountTypeEntriesGet


def create_account_type_entries(item_form_data: AccountTypeEntriesCreate) -> AccountTypeEntries:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO account_type_entries (
        tenant_id,
        account_id,
        account_type_id
    ) VALUES (%s, %s, %s) RETURNING *;
    """

    values = (
        item_form_data.tenant_id,
        item_form_data.account_id,
        item_form_data.account_type_id
    )

    cursor.execute(query, values)
    new_item = cursor.fetchone()

   
    conn.commit()
    conn.close()

    if new_item:
        return AccountTypeEntries(
            account_type_entries_id=new_item[0],
            tenant_id=new_item[1],
            account_id=new_item[2],
            account_type_id=new_item[3]
        )
    else:
        raise HTTPException(status_code=404, detail="Account Type Entries Detail creation failed")


def get_all_account_type_entries(account_id: int) -> List[AccountTypeEntriesGet]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT e.*, t.type_name
            FROM account_type_entries e
            LEFT JOIN account_type t ON t.account_type_id = e.account_type_id             
        WHERE e.account_id = %s;
        """

    cursor.execute(query,(account_id, ))
    query_all_items = cursor.fetchall()

    conn.close()
    if query_all_items:
        return [
            AccountTypeEntriesGet(
                account_type_entries_id=row[0],
                tenant_id=row[1],
                account_id=row[2],
                account_type_id=row[3],
                type_name=row[4]
            )
            for row in query_all_items
        ]
    else:
        None





def delete_account_type_entries(account_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM account_type_entries WHERE account_id = %s RETURNING account_id;"
    cursor.execute(query, (account_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False





def get_account_type_entries_by_id(account_type_entries_id: int) -> Optional[AccountTypeEntriesGet]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT e.*, t.type_name
            FROM account_type_entries e
            LEFT JOIN account_type t ON t.account_type_id = e.account_type_id              
        WHERE e.account_type_entries_id = %s;
        """

    cursor.execute(query, (account_type_entries_id,))
    get_all_items = cursor.fetchone()

    conn.close()

    if get_all_items:
        return AccountTypeEntriesGet (
                account_type_entries_id=get_all_items[0],
                tenant_id=get_all_items[1],
                account_id=get_all_items[2],
                account_type_id=get_all_items[3],
                type_name=get_all_items[4]
            )
    else:
        return None


