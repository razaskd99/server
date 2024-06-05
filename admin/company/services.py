from typing import Optional, List
from fastapi import HTTPException
from db.connection import get_db_connection
from admin.company.schemas import CompanyCreate, Company
from datetime import datetime


def create_company(company_data: CompanyCreate) -> Company:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO company (
        tenant_id,
        company_name, 
        phone, 
        email, 
        address, 
        industry, 
        website,
        company_type,
        company_logo, 
        created_date, 
        updated_date 
        
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        company_data.tenant_id,
        company_data.company_name,
        company_data.phone,
        company_data.email,
        company_data.address,
        company_data.industry,
        company_data.website,
        company_data.company_type,
        company_data.company_logo,
        company_data.created_date,
        company_data.updated_date,
    )

    cursor.execute(query, values)
    new_company = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_company:
        return Company(company_id=new_company[0], **company_data.dict())
    else:
        raise HTTPException(status_code=404, detail="Company creation failed")


def get_companies(tenant_id: int) -> List[Company]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM company WHERE tenant_id = %s;"
    cursor.execute(query,(tenant_id,))
    companies = cursor.fetchall()

    conn.close()
    
    return [
        Company (
            company_id=row[0],
            tenant_id =row[1],
            company_name=row[2],
            phone=row[3],
            email=row[4],
            address=row[5],
            industry=row[6],
            website=row[7],
            company_type=row[8],
            company_logo=row[9],
            created_date=row[10],   
            updated_date=row[11]   
        )
        for row in companies
    ]

def get_company_by_id(company_id: int) -> Optional[Company]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM company WHERE company_id = %s;"
    cursor.execute(query, (company_id,))
    company = cursor.fetchone()

    conn.close()

    if company:
        return Company(
            company_id=company[0],
            tenant_id =company[1],
            company_name=company[2],
            phone=company[3],
            email=company[4],
            address=company[5],
            industry=company[6],
            website=company[7],
            company_type=company[8],
            company_logo=company[9],
            created_date=company[10],
            updated_date=company[11],
             
        )
    else:
        return None


def update_company(company_id: int, company_data: CompanyCreate) -> Optional[Company]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE company SET 
        company_name = %s,
        phone = %s,
        email = %s,
        address = %s,
        industry = %s,
        website = %s,
        company_type = %s,
        company_logo = %s,
        created_date = %s,
        updated_date = %s
    WHERE company_id = %s RETURNING *;
    """

    values = (
        company_data.company_name,
        company_data.phone,
        company_data.email,
        company_data.address,
        company_data.industry,
        company_data.website,
        company_data.company_type,
        company_data.company_logo,
        company_data.created_date,
        company_data.updated_date,
        company_id,
    )

    cursor.execute(query, values)
    updated_company = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_company:
        return Company(
            company_id=updated_company[0],
            tenant_id = updated_company[1],
            company_name  = updated_company[2],
            phone = updated_company[3],
            email = updated_company[4],
            address = updated_company[5],
            industry = updated_company[6],
            website = updated_company[7],
            company_type = updated_company[8],
            company_logo  = updated_company[9],
            created_date = updated_company[10],
            updated_date = updated_company[11]
        )
    else:
        raise HTTPException(status_code=404, detail="Company update failed")


def delete_company(company_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM company WHERE company_id = %s RETURNING company_id;"
    cursor.execute(query, (company_id,))
           
    
    deleted_company = cursor.fetchone()
    

    conn.commit()
    conn.close()
                
        
    if deleted_company:
        return True
    else:
        return False


def get_company_by_name(company_name: str) -> Optional[Company]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM company WHERE lower(company_name) = %s;"
    cursor.execute(query, (company_name.lower(),))
    company = cursor.fetchone()
    conn.close()

    if company:
        return Company(
            company_id=company[0],
            tenant_id = company[1],
            company_name  = company[2],
            phone = company[3],
            email = company[4],
            address = company[5],
            industry = company[6],
            website = company[7],
            company_type = company[8],
            company_logo  = company[9],
            created_date = company[10],
            updated_date = company[11]
             
        )
    else:
        return None
    

def delete_all_company_record(company_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()  

    query = "SELECT delete_company_disable_FK(%s);"
    cursor.execute(query, (company_id,))
           
    
    deleted_company = cursor.fetchone()
    

    conn.commit()
    conn.close()
                
        
    if deleted_company:
        return True
    else:
        return False

