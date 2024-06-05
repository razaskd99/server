from typing import Optional, List
from fastapi import HTTPException
from db.connection import get_db_connection
import re
from .schemas import CustomerCreate, Customer
from datetime import date, datetime

def create_customer(customer_data: CustomerCreate) -> Customer:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO customer (
        tenant_id,
        company_id,
        customer_name,
        email,
        phone,
        address,
        created_at,
        updated_at
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        customer_data.tenant_id,
        customer_data.company_id,
        customer_data.customer_name,
        customer_data.email,
        customer_data.phone,
        customer_data.address,
        customer_data.created_at,
        customer_data.updated_at
    )

    cursor.execute(query, values)
    new_customer = cursor.fetchone()

    query = """
        SELECT c.*, 
            p.company_name, p.phone AS company_phone, p.email AS company_email,
            p.industry  AS company_industry, p.website AS company_website
            FROM customer c
            INNER JOIN company p ON p.company_id=c.company_id            
        WHERE c.customer_id = %s;
        """
    cursor.execute(query,(new_customer[0],))
    new_customer = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_customer:
        return Customer(
            customer_id=new_customer[0],
            tenant_id=new_customer[1],
            company_id=new_customer[2],
            customer_name=new_customer[3],
            email=new_customer[4],
            phone=new_customer[5],
            address=new_customer[6],
            created_at=new_customer[7],
            updated_at=new_customer[8],            
            company_name=new_customer[9],
            company_phone=new_customer[10],
            company_email=new_customer[11],
            company_industry=new_customer[12],
            company_website=new_customer[13]            
        )
    else:
        raise HTTPException(status_code=404, detail="Customer creation failed")


def get_all_customers(tenant_id: int) -> List[Customer]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT c.*, 
            p.company_name, p.phone AS company_phone, p.email AS company_email,
            p.industry  AS company_industry, p.website AS company_website
            FROM customer c
            INNER JOIN company p ON p.company_id=c.company_id
        WHERE c.tenant_id = %s;
        """
    cursor.execute(query,(tenant_id,))
    customers = cursor.fetchall()

    conn.close()

    return [
        Customer(
            customer_id=row[0],
            tenant_id=row[1],
            company_id=row[2],
            customer_name=row[3],
            email=row[4],
            phone=row[5],
            address=row[6],
            created_at=row[7],
            updated_at=row[8],            
            company_name=row[9],
            company_phone=row[10],
            company_email=row[11],
            company_industry=row[12],
            company_website=row[13]                  
        )
        for row in customers
    ]


def get_customer_by_id(customer_id: int) -> Optional[Customer]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT c.*, 
            p.company_name, p.phone AS company_phone, p.email AS company_email,
            p.industry  AS company_industry, p.website AS company_website
            FROM customer c
            INNER JOIN company p ON p.company_id=c.company_id
        WHERE c.customer_id = %s;
        """
    cursor.execute(query, (customer_id,))
    customer = cursor.fetchone()

    conn.close()

    if customer:
        return Customer(
            customer_id=customer[0],
            tenant_id=customer[1],
            company_id=customer[2],
            customer_name=customer[3],
            email=customer[4],
            phone=customer[5],
            address=customer[6],
            created_at=customer[7],
            updated_at=customer[8],            
            company_name=customer[9],
            company_phone=customer[10],
            company_email=customer[11],
            company_industry=customer[12],
            company_website=customer[13]             
        )
    else:
        return None


def get_customer_by_name(tenant_id: int, customer_name: str) -> Optional[Customer]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    customer_name = re.sub(r'-', ' ', customer_name)

    query = """
        SELECT c.*, 
            p.company_name, p.phone AS company_phone, p.email AS company_email,
            p.industry  AS company_industry, p.website AS company_website
            FROM customer c
            INNER JOIN company p ON p.company_id=c.company_id
        WHERE c.tenant_id = %s AND lower(c.customer_name) = %s;
        """
    cursor.execute(query, (tenant_id, customer_name.lower(),))
    customer = cursor.fetchone()

    conn.close()

    if customer:
        return Customer(
            customer_id=customer[0],
            tenant_id=customer[1],
            company_id=customer[2],
            customer_name=customer[3],
            email=customer[4],
            phone=customer[5],
            address=customer[6],
            created_at=customer[7],
            updated_at=customer[8],            
            company_name=customer[9],
            company_phone=customer[10],
            company_email=customer[11],
            company_industry=customer[12],
            company_website=customer[13]   
        )
    else:
        return None


def update_customer(customer_id: int, customer_data: CustomerCreate) -> Optional[Customer]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE customer SET 
        customer_name = %s,
        email = %s,
        phone = %s,
        address = %s,
        updated_ate = %s
    WHERE customer_id = %s RETURNING *;
    """

    values = (
        customer_data.customer_name,
        customer_data.email,
        customer_data.phone,
        customer_data.address,
        customer_data.updated_at,
        customer_id,
    )

    cursor.execute(query, values)
    updated_customer = cursor.fetchone()

    query = """
        SELECT c.*, 
            p.company_name, p.phone AS company_phone, p.email AS company_email,
            p.industry  AS company_industry, p.website AS company_website
            FROM customer c
            INNER JOIN company p ON p.company_id=c.company_id
        WHERE c.customer_id = %s;
        """
    cursor.execute(query,(customer_id,))
    updated_customer = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_customer:
        return Customer(
            customer_id=updated_customer[0],
            tenant_id=updated_customer[1],
            company_id=updated_customer[2],
            customer_name=v[3],
            email=updated_customer[4],
            phone=updated_customer[5],
            address=updated_customer[6],
            created_at=updated_customer[7],
            updated_at=updated_customer[8],            
            company_name=updated_customer[9],
            company_phone=updated_customer[10],
            company_email=updated_customer[11],
            company_industry=updated_customer[12],
            company_website=updated_customer[13]   
        )
    else:
        return None


def delete_customer(customer_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT delete_customer_disable_FK(%s) ;"
    cursor.execute(query, (customer_id,))
    deleted_customer = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_customer:
        return True
    else:
        return False
    
def delete_all_customer_record(customer_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()  

    query = "SELECT delete_customer_disable_FK(%s);"
    cursor.execute(query, (customer_id,))
           
    
    deleted_company = cursor.fetchone()
    

    conn.commit()
    conn.close()
                
        
    if deleted_company:
        return True
    else:
        return False

