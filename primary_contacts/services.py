from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
import re
from primary_contacts.schemas import PrimaryContactsCreate, PrimaryContacts, PrimaryContactsGet


def create_primary_contacts(item_form_data: PrimaryContactsCreate) -> PrimaryContacts:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO primary_contacts (
        tenant_id,
        first_name, 
        last_name,
        job_title, 
        manager, 
        function_group, 
        contact_number, 
        time_zone, 
        email, 
        working_hours, 
        work_location, 
        profile_image, 
        created_at
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        item_form_data.tenant_id, 
        item_form_data.first_name, 
        item_form_data.last_name,
        item_form_data.job_title, 
        item_form_data.manager, 
        item_form_data.function_group, 
        item_form_data.contact_number, 
        item_form_data.time_zone, 
        item_form_data.email, 
        item_form_data.working_hours, 
        item_form_data.work_location, 
        item_form_data.profile_image, 
        item_form_data.created_at
    )

    cursor.execute(query, values)
    new_item = cursor.fetchone()

   
    conn.commit()
    conn.close()

    if new_item:
        return PrimaryContacts(
            primary_contacts_id=new_item[0],
            tenant_id=new_item[1],
            first_name=new_item[2],
            last_name=new_item[3],
            job_title=new_item[4],
            manager=new_item[5],
            function_group=new_item[6],
            contact_number=new_item[7],
            time_zone=new_item[8],
            email=new_item[9],
            working_hours=new_item[10],
            work_location=new_item[11],
            profile_image=new_item[12],
            created_at=new_item[13]
        )
    else:
        raise HTTPException(status_code=404, detail="Primary Contacts Detail creation failed")


def get_all_primary_contacts(tenant_id: int) :
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM primary_contacts WHERE tenant_id = %s
        ORDER BY created_at DESC;
        """

    cursor.execute(query,(tenant_id, ))
    query_all_items = cursor.fetchall()

    conn.close()
    return [
        PrimaryContactsGet(
            primary_contacts_id=row[0],
            tenant_id=row[1],
            first_name=row[2],
            last_name=row[3],
            job_title=row[4],
            manager=row[5],
            function_group=row[6],
            contact_number=row[7],            
            time_zone=row[8],
            email=row[9],
            working_hours=row[10],
            work_location=row[11],
            profile_image=row[12],
            created_at=row[13],
        )
        for row in query_all_items
    ]


def update_primary_contacts(primary_contacts_id: int,  item_form_data: PrimaryContactsCreate) -> Optional[PrimaryContactsGet]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE primary_contacts SET 
        first_name = %s, 
        last_name = %s, 
        job_title = %s,
        manager = %s, 
        function_group = %s, 
        contact_number = %s, 
        time_zone = %s, 
        email = %s, 
        working_hours = %s, 
        work_location = %s, 
        profile_image = %s       
    WHERE primary_contacts_id = %s RETURNING *;
    """

    values = (
        item_form_data.first_name, 
        item_form_data.last_name,
        item_form_data.job_title,  
        item_form_data.manager, 
        item_form_data.function_group, 
        item_form_data.contact_number, 
        item_form_data.time_zone, 
        item_form_data.email, 
        item_form_data.working_hours, 
        item_form_data.work_location, 
        item_form_data.profile_image, 
        primary_contacts_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return PrimaryContacts(
            primary_contacts_id=updated_itemm[0],
            tenant_id=updated_itemm[1],
            first_name=updated_itemm[2],
            last_name=updated_itemm[3],
            job_title=updated_itemm[4],
            manager=updated_itemm[5],
            function_group=updated_itemm[6],
            contact_number=updated_itemm[7],
            time_zone=updated_itemm[8],
            email=updated_itemm[9],
            working_hours=updated_itemm[10],
            work_location=updated_itemm[11],
            profile_image=updated_itemm[12],
            created_at=updated_itemm[13]
        )
    else:
        raise HTTPException(status_code=404, detail="Primary Contacts update failed")


def delete_primary_contacts(primary_contacts_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM primary_contacts WHERE primary_contacts_id = %s RETURNING primary_contacts_id;"
    cursor.execute(query, (primary_contacts_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False

def delete_all_primary_contacts(tenant_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM primary_contacts WHERE tenant_id = %s RETURNING primary_contacts_id;"
    cursor.execute(query, (tenant_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False


def get_primary_contacts_by_id(primary_contacts_id: int) :
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM primary_contacts WHERE primary_contacts_id = %s
        ORDER BY created_at DESC;
        """

    cursor.execute(query, (primary_contacts_id,))
    get_item = cursor.fetchone()

    conn.close()

    if get_item:
        return  PrimaryContactsGet(
            primary_contacts_id=get_item[0],
            tenant_id=get_item[1],
            first_name=get_item[2],
            last_name=get_item[3],
            job_title=get_item[4],
            manager=get_item[5],
            function_group=get_item[6],
            contact_number=get_item[7],            
            time_zone=get_item[8],
            email=get_item[9],
            working_hours=get_item[10],
            work_location=get_item[11],
            profile_image=get_item[12],
            created_at=get_item[13],
        )                    


def get_primary_contacts_by_manager(tenant_id: int, manager : str) :
    conn = get_db_connection()
    cursor = conn.cursor()
    
    manager = re.sub(r'-', ' ', manager)

    query = """
        SELECT * FROM primary_contacts WHERE tenant_id = %s AND lower(manager) = %s
        ORDER BY created_at DESC;
        """

    cursor.execute(query, (tenant_id, manager.lower()))
    get_item = cursor.fetchall()

    conn.close()

    if get_item:
        return [
            PrimaryContactsGet(
            primary_contacts_id=row[0],
            tenant_id=row[1],
            first_name=row[2],
            last_name=row[3],
            job_title=row[4],
            manager=row[5],
            function_group=row[6],
            contact_number=row[7],            
            time_zone=row[8],
            email=row[9],
            working_hours=row[10],
            work_location=row[11],
            profile_image=row[12],
            created_at=row[13],
        )
            for row in get_item
        ]
