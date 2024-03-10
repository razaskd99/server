from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from contacts.schemas import ContactsCreate, Contacts, ContactsGet

def create_contacts(item_form_data: ContactsCreate) -> Contacts:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO contacts (
        tenant_id,
        rfx_id,
        contact_user_id,
        conatct_key,
        created_date,
        created_at
    ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        item_form_data.tenant_id,
        item_form_data.rfx_id,
        item_form_data.contact_user_id,
        item_form_data.conatct_key,
        item_form_data.created_date,
        item_form_data.created_at
    )

    cursor.execute(query, values)
    new_item = cursor.fetchone()

    query = """
        SELECT c.*, 
            u.user_name, u.email, u.first_name, u.middle_name, u.last_name,
            u.user_role, u.role_level, u.user_profile_photo
        FROM contacts c
        INNER JOIN users u ON u.user_id=c.contact_user_id              
        WHERE c.contact_id = %s ;
        """

    cursor.execute(query,(new_item[0], ))
    new_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_item:
        return Contacts(
            contact_id=new_item[0],
            tenant_id=new_item[1],
            rfx_id=new_item[2],
            contact_user_id=new_item[3],
            conatct_key=new_item[4],
            created_date=new_item[5],
            created_at=new_item[6],
            user_name=new_item[7],
            email=new_item[8],
            first_name=new_item[9],
            middle_name=new_item[10],
            last_name=new_item[11],
            user_role=new_item[12],
            role_level=new_item[13],
            user_profile_photo=new_item[14]
        )
    else:
        raise HTTPException(status_code=404, detail="Contacts creation failed")


def get_all_contacts(tenant_id: int) -> List[ContactsGet]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT c.*, 
            u.user_name, u.email, u.first_name, u.middle_name, u.last_name,
            u.user_role, u.role_level, u.user_profile_photo,
			t.team_role,
			d.title AS designation_title
            FROM contacts c
            INNER JOIN users u ON u.user_id=c.contact_user_id
			LEFT JOIN team t ON t.team_id = u.team_id
			LEFT JOIN designation d ON d.designation_id = u.designation_id              
        WHERE c.tenant_id = %s ;
        """

    cursor.execute(query,(tenant_id, ))
    query_all_items = cursor.fetchall()

    conn.close()
    if query_all_items:
        return [
            ContactsGet(
                contact_id=row[0],
                tenant_id=row[1],
                rfx_id=row[2],
                contact_user_id=row[3],
                conatct_key=row[4],
                created_date=row[5],
                created_at=row[6],
                user_name=row[7],
                email=row[8],
                first_name=row[9],
                middle_name=row[10],
                last_name=row[11],
                user_role=row[12],
                role_level=row[13],
                user_profile_photo=row[14],
                team_role=row[15],
                designation_title=row[16]
            )
            for row in query_all_items
        ]
    else:
        None

def update_contacts(contact_id: int,  contact_data: ContactsCreate) -> Optional[Contacts]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE contacts SET 
        contact_user_id = %s,
        conatct_key = %s
    WHERE contact_id = %s RETURNING *;
    """

    values = (
        contact_data.contact_user_id,
        contact_data.conatct_key,
        contact_id
    )

    cursor.execute(query, values)
    updated_item = cursor.fetchone()

    query = """
        SELECT c.*, 
            u.user_name, u.email, u.first_name, u.first_name, u.first_name,
            u.user_role, u.role_level, u.user_profile_photo
            FROM contacts c
            INNER JOIN users u ON u.user_id=c.contact_user_id  
        WHERE c.contact_id = %s;
        """
    
    cursor.execute(query, (contact_id,))
    updated_itemm = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if updated_item:
        return Contacts(
            contact_id=updated_itemm[0],
            tenant_id=updated_itemm[1],
            rfx_id=updated_itemm[2],
            contact_user_id=updated_itemm[3],
            conatct_key=updated_itemm[4],
            created_date=updated_itemm[5],
            created_at=updated_itemm[6],
            user_name=updated_itemm[7],
            email=updated_itemm[8],
            first_name=updated_itemm[9],
            middle_name=updated_itemm[10],
            last_name=updated_itemm[11],
            user_role=updated_itemm[12],
            role_level=updated_itemm[13],
            user_profile_photo=updated_itemm[14]
        )
    else:
        raise HTTPException(status_code=404, detail="Contacts update failed")


def delete_contacts(contact_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM contacts WHERE contact_id = %s RETURNING contact_id;"
    cursor.execute(query, (contact_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False
    
def get_contacts_by_id(tenant_id: int, contact_id: int) -> List[ContactsGet]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT c.*, 
            u.user_name, u.email, u.first_name, u.middle_name, u.last_name,
            u.user_role, u.role_level, u.user_profile_photo,
			t.team_role,
			d.title AS designation_title
            FROM contacts c
            INNER JOIN users u ON u.user_id=c.contact_user_id
			LEFT JOIN team t ON t.team_id = u.team_id
			LEFT JOIN designation d ON d.designation_id = u.designation_id  
        WHERE c.tenant_id = %s AND c.contact_id = %s ;
        """

    cursor.execute(query, (tenant_id, contact_id))
    get_all_items = cursor.fetchall()

    conn.close()

    if get_all_items:
        return [
            ContactsGet(
                contact_id=row[0],
                tenant_id=row[1],
                rfx_id=row[2],
                contact_user_id=row[3],
                conatct_key=row[4],
                created_date=row[5],
                created_at=row[6],
                user_name=row[7],
                email=row[8],
                first_name=row[9],
                middle_name=row[10],
                last_name=row[11],
                user_role=row[12],
                role_level=row[13],
                user_profile_photo=row[14],
                team_role=row[15],
                designation_title=row[16]
            )
            for row in get_all_items
        ]
    else:
        None


def get_contacts_by_rfx_id(tenant_id: int, rfx_id: int) -> List[ContactsGet]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT c.*, 
            u.user_name, u.email, u.first_name, u.middle_name, u.last_name,
            u.user_role, u.role_level, u.user_profile_photo,
			t.team_role,
			d.title AS designation_title
            FROM contacts c
            INNER JOIN users u ON u.user_id=c.contact_user_id
			LEFT JOIN team t ON t.team_id = u.team_id
			LEFT JOIN designation d ON d.designation_id = u.designation_id  
        WHERE c.tenant_id = %s AND c.rfx_id = %s ;
        """

    cursor.execute(query, (tenant_id, rfx_id))
    get_all_items = cursor.fetchall()

    conn.close()

    if get_all_items:
        return [
            ContactsGet(
                contact_id=row[0],
                tenant_id=row[1],
                rfx_id=row[2],
                contact_user_id=row[3],
                conatct_key=row[4],
                created_date=row[5],
                created_at=row[6],
                user_name=row[7],
                email=row[8],
                first_name=row[9],
                middle_name=row[10],
                last_name=row[11],
                user_role=row[12],
                role_level=row[13],
                user_profile_photo=row[14],
                team_role=row[15],
                designation_title=row[16]
            )
            for row in get_all_items
        ]
    else:
        None
    
def get_contacts_by_rfx_id_and_key(tenant_id: int,rfx_id: int, conatct_key: str) -> List[ContactsGet]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT c.*, 
            u.user_name, u.email, u.first_name, u.middle_name, u.last_name,
            u.user_role, u.role_level, u.user_profile_photo,
			t.team_role,
			d.title AS designation_title
            FROM contacts c
            INNER JOIN users u ON u.user_id=c.contact_user_id
			LEFT JOIN team t ON t.team_id = u.team_id
			LEFT JOIN designation d ON d.designation_id = u.designation_id 
        WHERE c.tenant_id = %s AND c.rfx_id = %s AND lower(c.conatct_key) = %s ;
        """

    cursor.execute(query, (tenant_id, rfx_id, conatct_key.lower()))
    get_all_items = cursor.fetchall()

    conn.close()

    if get_all_items:
        return [
            ContactsGet(
                contact_id=row[0],
                tenant_id=row[1],
                rfx_id=row[2],
                contact_user_id=row[3],
                conatct_key=row[4],
                created_date=row[5],
                created_at=row[6],
                user_name=row[7],
                email=row[8],
                first_name=row[9],
                middle_name=row[10],
                last_name=row[11],
                user_role=row[12],
                role_level=row[13],
                user_profile_photo=row[14],
                team_role=row[15],
                designation_title=row[16]
            )
            for row in get_all_items
        ]
    else:
        None