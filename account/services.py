from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from account.schemas import AccountCreate, Account, AccountGet, AccountGetMax, AccountUpdate


def create_account(account_data: AccountCreate) -> Account:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO account (
        tenant_id,
        account_name,
        account_type_id,
        account_owner_id,
        street,
        city,
        postal_code,
        country,
        data,
        created_at,
        account_number,
        account_image,
        state
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        account_data.tenant_id,
        account_data.account_name,
        account_data.account_type_id,
        account_data.account_owner_id,
        account_data.street,
        account_data.city,
        account_data.postal_code,
        account_data.country,
        account_data.data,
        account_data.created_at,
        account_data.account_number,
        account_data.account_image,
        account_data.state
    )

    cursor.execute(query, values)
    new_submission = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if new_submission:
        return Account(
            account_id=new_submission[0],
            tenant_id=new_submission[1],
            account_name=new_submission[2],
            account_type_id=new_submission[3],
            account_owner_id=new_submission[4],
            street=new_submission[5],
            city=new_submission[6],
            postal_code=new_submission[7],
            country=new_submission[8],
            data=new_submission[9],
            created_at=new_submission[10],
            account_number=new_submission[11],
            account_image=new_submission[12],
            state=new_submission[13]                                 
                 
        )
    else:
        raise HTTPException(status_code=404, detail="Account creation failed")


def get_all_account(tenant_id: int, searchTerm: str, offset: int, limit: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if searchTerm: 
        searchTerm = '%' + searchTerm.lower() + '%'
        query = """
            SELECT a.*,
                t.type_name, CONCAT(u.first_name, ' ', u.last_name) AS owner_name, u.profile_image, u.job_title,
                (
                    SELECT string_agg(tt.type_name, ', ') AS type_list
                        FROM account_type_entries ee
                        LEFT JOIN account_type tt ON tt.account_type_id = ee.account_type_id              
                    WHERE ee.account_id = a.account_id
                )
                FROM account a 
                LEFT JOIN account_type t ON t.account_type_id = a.account_type_id
                LEFT JOIN users u ON u.user_id = a.account_owner_id
            WHERE a.tenant_id = %s and lower(a.account_name) LIKE %s 
            ORDER BY a.created_at DESC 
            OFFSET %s LIMIT %s;           
            """
        cursor.execute(query,(tenant_id, searchTerm, offset, limit))
        account = cursor.fetchall()
        
        # Query to get total count without offset and limit
        query_total_count = "SELECT COUNT(*) FROM account WHERE tenant_id = %s AND lower(account_name) LIKE %s;"
        cursor.execute(query_total_count, (tenant_id, searchTerm))
        total_count = cursor.fetchone()
    else:
        query = """
            SELECT a.*,
                t.type_name, CONCAT(u.first_name, ' ', u.last_name) AS owner_name, u.profile_image, u.job_title,
                (
                    SELECT string_agg(tt.type_name, ', ') AS type_list
                        FROM account_type_entries ee
                        LEFT JOIN account_type tt ON tt.account_type_id = ee.account_type_id              
                    WHERE ee.account_id = a.account_id
                )
                FROM account a 
                LEFT JOIN account_type t ON t.account_type_id = a.account_type_id
                LEFT JOIN users u ON u.user_id = a.account_owner_id
            WHERE a.tenant_id = %s 
            ORDER BY a.created_at DESC 
            OFFSET %s LIMIT %s;           
            """
        cursor.execute(query,(tenant_id, offset, limit))
        account = cursor.fetchall()
        
    # Query to get total count without offset and limit
    query_total_count = "SELECT COUNT(*) FROM account WHERE tenant_id = %s;"
    cursor.execute(query_total_count, (tenant_id, ))
    total_count = cursor.fetchone()
    
    conn.close()
    
    if account:
        return {
            "data": [
                AccountGet(
                    account_id=row[0],
                    tenant_id=row[1],
                    account_name=row[2],
                    account_type_id=row[3],
                    account_owner_id=row[4],
                    street=row[5],
                    city=row[6],
                    postal_code=row[7],
                    country=row[8],
                    data=row[9],
                    created_at=row[10],
                    account_number=row[11],
                    account_image=row[12],
                    state=row[13],
                    type_name=row[14],
                    owner_name=row[15],
                    profile_image=row[16],
                    job_title=row[17],
                    type_list=row[18]                    
                )
                for row in account
            ],
            "total_count": total_count
        }
    else:
        None
   
        
def update_account(account_id: int, account_data: AccountUpdate) -> Optional[Account]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE account SET 
        account_name = %s,
        account_type_id = %s,
        account_owner_id = %s,
        street = %s,
        city = %s,
        postal_code = %s,
        country = %s,
        data = %s,
        account_image = %s,
        state = %s
    WHERE account_id = %s RETURNING *;
    """
    
    values = (
        account_data.account_name,
        account_data.account_type_id,
        account_data.account_owner_id,
        account_data.street,
        account_data.city,
        account_data.postal_code,
        account_data.country,
        account_data.data,
        account_data.account_image,
        account_data.state,
        account_id
    )

    cursor.execute(query, values)
    account = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if account:
        return Account(
                account_id=account[0],
                tenant_id=account[1],
                account_name=account[2],
                account_type_id=account[3],
                account_owner_id=account[4],
                street=account[5],
                city=account[6],
                postal_code=account[7],
                country=account[8],
                data=account[9],
                created_at=account[10],
                account_number=account[11],
                account_image=account[12],
                state=account[13]
            )      
    else:
        None
 

       
def delete_account(account_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "DELETE FROM account WHERE account_id = %s RETURNING account_id;"
    cursor.execute(query, (account_id,))
    deleted_account = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if deleted_account:
        return True
    else:
        return False


def get_account_by_id(account_id: int) -> Optional[AccountGet]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT a.*,
            t.type_name, CONCAT(u.first_name, ' ', u.last_name) AS owner_name, u.profile_image, u.job_title,
            (
                SELECT string_agg(tt.type_name, ', ') AS type_list
                    FROM account_type_entries ee
                    LEFT JOIN account_type tt ON tt.account_type_id = ee.account_type_id              
                WHERE ee.account_id = a.account_id
            )
            FROM account a 
            LEFT JOIN account_type t ON t.account_type_id = a.account_type_id
            LEFT JOIN users u ON u.user_id = a.account_owner_id
        WHERE a.account_id = %s
        ORDER BY a.created_at DESC; 
        """

    cursor.execute(query,(account_id,))
    account = cursor.fetchone()

    conn.close()
    if account:
        return AccountGet(
                account_id=account[0],
                tenant_id=account[1],
                account_name=account[2],
                account_type_id=account[3],
                account_owner_id=account[4],
                street=account[5],
                city=account[6],
                postal_code=account[7],
                country=account[8],
                data=account[9],
                created_at=account[10],
                account_number=account[11],
                account_image=account[12],
                state=account[13],
                type_name=account[14],
                owner_name=account[15],
                profile_image=account[16],
                job_title=account[17],
                type_list=account[18]
            )
    else:
        None
        
def get_account_id_max() -> Optional[AccountGetMax]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT max(account_id), max(account_number) from account;
        """

    cursor.execute(query)
    account = cursor.fetchone()

    conn.close()
    if account:
        return AccountGetMax(
                account_id=account[0],
                account_number=account[1]
            )
    else:
        None