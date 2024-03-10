from typing import Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from admin.control_panel.schemas import TenantCreate, Tenant
from typing import List
from urllib.parse import quote


def check_valid_tenant(domain_url: str) -> Optional[Tenant]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT * FROM tenant
    WHERE lower(domain_url) = %s 
    """

    cursor.execute(query, (domain_url.lower(),))
    tenant = cursor.fetchone()

    conn.close()

    if tenant:
        return Tenant(
            tenant_id=tenant[0],
            tenant_name=tenant[1],
            tenant_title=tenant[2],
            tenant_logo=tenant[3],
            tenant_description=tenant[4],
            contact_person=tenant[5],
            contact_email=tenant[6],
            contact_phone=tenant[7],
            contact_address=tenant[8],
            subscription_start_date=tenant[9],
            subscription_end_date=tenant[10],
            subscription_type=tenant[11],
            created_on=tenant[12],
            created_at=tenant[13],
            updated_at=tenant[14],
            location_country=tenant[15],
            location_state=tenant[16],
            location_zip=tenant[17],
            domain_url=tenant[18],
            private_key=tenant[19],
            public_key=tenant[20],
            email_verified=True if tenant[21] else False,
            tenant_status=tenant[22],
            tenant_is_active=True if tenant[23] else False
        )
    else:
        return None


def create_tenant(tenant_data: TenantCreate) -> Optional[Tenant]:
    conn = get_db_connection()
    cursor = conn.cursor()

    # Convert tenant_name to URL format
    domain_url = convert_to_url_string(tenant_data.tenant_name)

    query = """
    INSERT INTO tenant (
        tenant_name, 
        tenant_title,
        tenant_logo,
        tenant_description, 
        contact_person, 
        contact_email, 
        contact_phone, 
        contact_address,
        subscription_start_date, 
        subscription_end_date, 
        subscription_type,
        created_on,
        created_at,
        updated_at,
        location_country, 
        location_state, 
        location_zip, 
        domain_url,
        private_key,
        public_key,
        email_verified,
        tenant_status,
        tenant_is_active
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        tenant_data.tenant_name,
        tenant_data.tenant_title,
        tenant_data.tenant_logo,       
        tenant_data.tenant_description,
        tenant_data.contact_person,
        tenant_data.contact_email,
        tenant_data.contact_phone,
        tenant_data.contact_address,
        tenant_data.subscription_start_date,
        tenant_data.subscription_end_date,
        tenant_data.subscription_type,
        tenant_data.created_on,
        tenant_data.created_at,
        tenant_data.updated_at,
        tenant_data.location_country,
        tenant_data.location_state,
        tenant_data.location_zip,
        domain_url,  # Use the converted tenant_name as domain_url
        tenant_data.private_key,
        tenant_data.public_key,
        tenant_data.email_verified,
        tenant_data.tenant_status,
        tenant_data.tenant_is_active
    )

    cursor.execute(query, values)
    new_tenant = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_tenant:
        email_verified = True if new_tenant[21] else False
        tenant_is_active = True if new_tenant[23] else False

        return Tenant(
            tenant_id=new_tenant[0],
            tenant_name=new_tenant[1],
            tenant_title=new_tenant[2],
            tenant_logo=new_tenant[3],
            tenant_description=new_tenant[4],
            contact_person=new_tenant[5],
            contact_email=new_tenant[6],
            contact_phone=new_tenant[7],
            contact_address=new_tenant[8],
            subscription_start_date=new_tenant[9],
            subscription_end_date=new_tenant[10],
            subscription_type=new_tenant[11],
            created_on=new_tenant[12],
            created_at=new_tenant[13],
            updated_at=new_tenant[14],
            location_country=new_tenant[15],
            location_state=new_tenant[16],
            location_zip=new_tenant[17],
            domain_url=new_tenant[18],
            private_key=new_tenant[19],
            public_key=new_tenant[20],
            email_verified=email_verified,
            tenant_status=new_tenant[22],
            tenant_is_active=tenant_is_active
        )
    else:
        raise HTTPException(status_code=404, detail="Tenant creation failed")
    
def get_tenants() -> List[Tenant]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM tenant;"
    cursor.execute(query)
    tenants = cursor.fetchall()

    conn.close()

    return [
        Tenant(
            tenant_id=row[0],
            tenant_name=row[1],
            tenant_title=row[2],
            tenant_logo=row[3],
            tenant_description=row[4],
            contact_person=row[5],
            contact_email=row[6],
            contact_phone=row[7],
            contact_address=row[8],
            subscription_start_date=row[9],
            subscription_end_date=row[10],
            subscription_type=row[11],
            created_on=row[12],
            created_at=row[13],
            updated_at=row[14],
            location_country=row[15],
            location_state=row[16],
            location_zip=row[17],
            domain_url=row[18],
            private_key=row[19],
            public_key=row[20],
            email_verified=True if row[21] else False,
            tenant_status=row[22],
            tenant_is_active=True if row[23] else False
        )
        for row in tenants
    ]
    
    
    
def update_tenant(tenant_id: int, tenant_data: TenantCreate) -> Optional[Tenant]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE tenant SET 
        tenant_name = %s,
        tenant_title = %s,
        tenant_logo = %s,        
        tenant_description = %s,
        contact_person = %s,
        contact_email = %s,
        contact_phone = %s,
        contact_address = %s,
        subscription_start_date = %s,
        subscription_end_date = %s,
        subscription_type = %s,
        created_on = %s,
        created_at = %s,
        updated_at = %s,
        location_country = %s,
        location_state = %s,
        location_zip = %s,
        domain_url = %s,
        private_key = %s,
        public_key = %s,
        email_verified = %s,
        tenant_status = %s,
        tenant_is_active = %s
    WHERE tenant_id = %s RETURNING *;
    """

    values = (
        tenant_data.tenant_name,
        tenant_data.tenant_title,
        tenant_data.tenant_logo,
        tenant_data.tenant_description,
        tenant_data.contact_person,
        tenant_data.contact_email,
        tenant_data.contact_phone,
        tenant_data.contact_address,
        tenant_data.subscription_start_date,
        tenant_data.subscription_end_date,
        tenant_data.subscription_type,
        tenant_data.created_on,
        tenant_data.created_at,
        tenant_data.updated_at,
        tenant_data.location_country,
        tenant_data.location_state,
        tenant_data.location_zip,
        tenant_data.domain_url,
        tenant_data.private_key,
        tenant_data.public_key,
        tenant_data.email_verified,
        tenant_data.tenant_status,
        tenant_data.tenant_is_active,
        tenant_id
    )

    cursor.execute(query, values)
    updated_tenant = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_tenant:
        return Tenant(
            tenant_id=updated_tenant[0],
            tenant_name=updated_tenant[1],
            tenant_title=updated_tenant[2],
            tenant_logo=updated_tenant[3],
            tenant_description=updated_tenant[4],
            contact_person=updated_tenant[5],
            contact_email=updated_tenant[6],
            contact_phone=updated_tenant[7],
            contact_address=updated_tenant[8],
            subscription_start_date=updated_tenant[9],
            subscription_end_date=updated_tenant[10],
            subscription_type=updated_tenant[11],
            created_on=updated_tenant[12],
            created_at=updated_tenant[13],
            updated_at=updated_tenant[14],
            location_country=updated_tenant[15],
            location_state=updated_tenant[16],
            location_zip=updated_tenant[17],
            domain_url=updated_tenant[18],
            private_key=updated_tenant[19],
            public_key=updated_tenant[20],
            email_verified=updated_tenant[21],
            tenant_status=updated_tenant[22],
            tenant_is_active=updated_tenant[23]
        )
    else:
        raise HTTPException(status_code=404, detail="Tenant update failed")

def delete_tenant(tenant_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM tenant WHERE tenant_id = %s RETURNING tenant_id;"
    cursor.execute(query, (tenant_id,))
    deleted_tenant = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_tenant:
        return True
    else:
        return False
    
    
def get_tenant_by_name(tenant_name: str) -> Optional[Tenant]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM tenant WHERE lower(tenant_name) = %s;"
    cursor.execute(query, (tenant_name.lower(),))
    tenant = cursor.fetchone()

    conn.close()

    if tenant:
        return Tenant(
            tenant_id=tenant[0],
            tenant_name=tenant[1],
            tenant_title=tenant[2],
            tenant_logo=tenant[3],
            tenant_description=tenant[4],
            contact_person=tenant[5],
            contact_email=tenant[6],
            contact_phone=tenant[7],
            contact_address=tenant[8],
            subscription_start_date=tenant[9],
            subscription_end_date=tenant[10],
            subscription_type=tenant[11],
            created_on=tenant[12],
            created_at=tenant[13],
            updated_at=tenant[14],
            location_country=tenant[15],
            location_state=tenant[16],
            location_zip=tenant[17],
            domain_url=tenant[18],
            private_key=tenant[19],
            public_key=tenant[20],
            email_verified=True if tenant[21] else False,
            tenant_status=tenant[22],
            tenant_is_active=True if tenant[23] else False
        )
    else:
        return None


def get_tenant_by_id(tenant_id: int) -> Optional[Tenant]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM tenant WHERE tenant_id = %s;"
    cursor.execute(query, (tenant_id,))
    tenant = cursor.fetchone()

    conn.close()

    if tenant:
        return Tenant(
            tenant_id=tenant[0],
            tenant_name=tenant[1],
            tenant_title=tenant[2],
            tenant_logo=tenant[3],
            tenant_description=tenant[4],
            contact_person=tenant[5],
            contact_email=tenant[6],
            contact_phone=tenant[7],
            contact_address=tenant[8],
            subscription_start_date=tenant[9],
            subscription_end_date=tenant[10],
            subscription_type=tenant[11],
            created_on=tenant[12],
            created_at=tenant[13],
            updated_at=tenant[14],
            location_country=tenant[15],
            location_state=tenant[16],
            location_zip=tenant[17],
            domain_url=tenant[18],
            private_key=tenant[19],
            public_key=tenant[20],
            email_verified=True if tenant[21] else False,
            tenant_status=tenant[22],
            tenant_is_active=True if tenant[23] else False
        )
    else:
        return None


def get_tenant_by_status(tenant_status: str) -> Optional[Tenant]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM tenant WHERE lower(tenant_status) = %s;"
    cursor.execute(query, (tenant_status.lower(),))
    tenant = cursor.fetchone()

    conn.close()

    if tenant:
        return Tenant(
            tenant_id=tenant[0],
            tenant_name=tenant[1],
            tenant_title=tenant[2],
            tenant_logo=tenant[3],
            tenant_description=tenant[4],
            contact_person=tenant[5],
            contact_email=tenant[6],
            contact_phone=tenant[7],
            contact_address=tenant[8],
            subscription_start_date=tenant[9],
            subscription_end_date=tenant[10],
            subscription_type=tenant[11],
            created_on=tenant[12],
            created_at=tenant[13],
            updated_at=tenant[14],
            location_country=tenant[15],
            location_state=tenant[16],
            location_zip=tenant[17],
            domain_url=tenant[18],
            private_key=tenant[19],
            public_key=tenant[20],
            email_verified=True if tenant[21] else False,
            tenant_status=tenant[22],
            tenant_is_active=True if tenant[23] else False
        )
    else:
        return None


def is_tenant_verified_by_name(tenant_name: str) -> bool:
    tenant = get_tenant_by_name(tenant_name)
    if tenant:
        return bool(tenant.email_verified)
    return False


def is_tenant_active_by_name(tenant_name: str) -> bool:
    tenant = get_tenant_by_name(tenant_name)
    if tenant:
        return bool(tenant.tenant_is_active)
    return False


def convert_to_url_string(input_string):
    # Trim leading and trailing spaces
    input_string = input_string.strip()

    # Replace spaces with dashes (-)
    modified_string = input_string.replace(' ', '-')

    # Remove underscores (_)
    modified_string = modified_string.replace('_', '')

    # Remove special characters
    special_characters = '#$%&*+/:;<=>?@\\^`{|}~'
    modified_string = ''.join(char for char in modified_string if char not in special_characters)

    # Convert the modified string to lowercase
    modified_string = modified_string.lower()

    # Encode the modified string
    url_string = quote(modified_string)
    return url_string