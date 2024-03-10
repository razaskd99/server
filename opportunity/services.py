from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import OpportunityCreate, Opportunity
from datetime import date, datetime


def create_opportunity(opportunity_data: OpportunityCreate) -> Optional[Opportunity]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO opportunity (
        tenant_id,
        company_id,
        customer_id,
        title,
        type,
        probability,
        total_value,
        crm_id,
        customer_name,
        end_user_name,
        region,
        industry_code,
        business_unit,
        project_type,
        delivery_duration,
        stage,
        status,
        expected_award_date,
        expected_rfx_date,
        close_date,
        competition,
        gross_profit_percent,
        gross_profit_value,
        description,
        last_updated_at,
        forcasted
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        opportunity_data.tenant_id,
        opportunity_data.company_id,
        opportunity_data.customer_id,
        opportunity_data.title,
        opportunity_data.type,
        opportunity_data.probability,
        opportunity_data.total_value,
        opportunity_data.crm_id,
        opportunity_data.customer_name,
        opportunity_data.end_user_name,
        opportunity_data.region,
        opportunity_data.industry_code,
        opportunity_data.business_unit,
        opportunity_data.project_type,
        opportunity_data.delivery_duration,
        opportunity_data.stage,
        opportunity_data.status,
        opportunity_data.expected_award_date,
        opportunity_data.expected_rfx_date,
        opportunity_data.close_date,
        opportunity_data.competition,
        opportunity_data.gross_profit_percent,
        opportunity_data.gross_profit_value,
        opportunity_data.description,
        opportunity_data.last_updated_at,
        opportunity_data.forcasted
    )

    cursor.execute(query, values)
    new_opportunity = cursor.fetchone()

    query = """
        SELECT o.*, 
            p.company_name, p.email AS company_email, p.company_logo,
            c.customer_name AS ct_customer_name, c.email AS customer_email
            FROM opportunity o
            INNER JOIN company p ON p.company_id=o.company_id
            INNER JOIN customer c ON c.customer_id=o.customer_id
        WHERE o.opportunity_id = %s;
        """
    
    cursor.execute(query, (new_opportunity[0],))
    new_opportunity = cursor.fetchone()

    conn.commit()
    conn.close()

    if new_opportunity:
        return Opportunity(
            opportunity_id=new_opportunity[0],
            tenant_id=new_opportunity[1],
            company_id=new_opportunity[2],
            customer_id=new_opportunity[3],
            title=new_opportunity[4],
            type=new_opportunity[5],
            probability=new_opportunity[6],
            total_value=new_opportunity[7],
            crm_id=new_opportunity[8],
            customer_name=new_opportunity[9],
            end_user_name=new_opportunity[10],
            region=new_opportunity[11],
            industry_code=new_opportunity[12],
            business_unit=new_opportunity[13],
            project_type=new_opportunity[14],
            delivery_duration=new_opportunity[15],
            stage=new_opportunity[16],
            status=new_opportunity[17],
            expected_award_date=new_opportunity[18],
            expected_rfx_date=new_opportunity[19],
            close_date=new_opportunity[20],
            competition=new_opportunity[21],
            gross_profit_percent=new_opportunity[22],
            gross_profit_value=new_opportunity[23],
            description=new_opportunity[24],
            last_updated_at=new_opportunity[25],
            forcasted=new_opportunity[26],
            company_name=new_opportunity[27],
            company_email=new_opportunity[28],
            company_logo=new_opportunity[29],
            ct_customer_name=new_opportunity[30],
            customer_email=new_opportunity[31]
        )
    else:
        raise HTTPException(status_code=404, detail="Opportunity creation failed")


def get_all_opportunities(tenant_id: int) -> List[Opportunity]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT o.*, 
            p.company_name, p.email AS company_email, p.company_logo,
            c.customer_name AS ct_customer_name, c.email AS customer_email
            FROM opportunity o
            INNER JOIN company p ON p.company_id=o.company_id
            INNER JOIN customer c ON c.customer_id=o.customer_id
        WHERE o.tenant_id = %s;
        """

    cursor.execute(query, (tenant_id,))
    opportunities = cursor.fetchall()

    conn.close()

    return [
        Opportunity(
            opportunity_id=row[0],
            tenant_id=row[1],
            company_id=row[2],
            customer_id=row[3],
            title=row[4],
            type=row[5],
            probability=row[6],
            total_value=row[7],
            crm_id=row[8],
            customer_name=row[9],
            end_user_name=row[10],
            region=row[11],
            industry_code=row[12],
            business_unit=row[13],
            project_type=row[14],
            delivery_duration=row[15],
            stage=row[16],
            status=row[17],
            expected_award_date=row[18],
            expected_rfx_date=row[19],
            close_date=row[20],
            competition=row[21],
            gross_profit_percent=row[22],
            gross_profit_value=row[23],
            description=row[24],
            last_updated_at=row[25],
            forcasted=row[26],
            company_name=row[27],
            company_email=row[28],
            company_logo=row[29],
            ct_customer_name=row[30],
            customer_email=row[31]
        )
        for row in opportunities
    ]


def update_opportunity(tenant_id: int, opportunity_id: int, opportunity_data: OpportunityCreate) -> Optional[Opportunity]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE opportunity SET 
        tenant_id = %s,
        company_id = %s,
        customer_id = %s,
        title = %s,
        type = %s,
        probability = %s,
        total_value = %s,
        crm_id = %s,
        customer_name = %s,
        end_user_name = %s,
        region = %s,
        industry_code = %s,
        business_unit = %s,
        project_type = %s,
        delivery_duration = %s,
        stage = %s,
        status = %s,
        expected_award_date = %s,
        expected_rfx_date = %s,
        close_date = %s,
        competition = %s,
        gross_profit_percent = %s,
        gross_profit_value = %s,
        description = %s,
        last_updated_at = %s,
        forcasted = %s
    WHERE tenant_id = %s AND opportunity_id = %s RETURNING *;
    """

    values = (
        opportunity_data.tenant_id,
        opportunity_data.company_id,
        opportunity_data.customer_id,
        opportunity_data.title,
        opportunity_data.type,
        opportunity_data.probability,
        opportunity_data.total_value,
        opportunity_data.crm_id,
        opportunity_data.customer_name,
        opportunity_data.end_user_name,
        opportunity_data.region,
        opportunity_data.industry_code,
        opportunity_data.business_unit,
        opportunity_data.project_type,
        opportunity_data.delivery_duration,
        opportunity_data.stage,
        opportunity_data.status,
        opportunity_data.expected_award_date,
        opportunity_data.expected_rfx_date,
        opportunity_data.close_date,
        opportunity_data.competition,
        opportunity_data.gross_profit_percent,
        opportunity_data.gross_profit_value,
        opportunity_data.description,
        opportunity_data.last_updated_at,
        opportunity_data.forcasted,
        tenant_id,
        opportunity_id
    )

    cursor.execute(query, values)
    updated_opportunity = cursor.fetchone()

    query = """
        SELECT o.*, 
            p.company_name, p.email AS company_email, p.company_logo,
            c.customer_name AS ct_customer_name, c.email AS customer_email
            FROM opportunity o
            INNER JOIN company p ON p.company_id=o.company_id
            INNER JOIN customer c ON c.customer_id=o.customer_id
        WHERE o.tenant_id = %s AND o.opportunity_id = %s;
        """
    cursor.execute(query, (tenant_id, opportunity_id))
    updated_opportunity = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_opportunity:
        return Opportunity(
            opportunity_id=updated_opportunity[0],
            tenant_id=updated_opportunity[1],
            company_id=updated_opportunity[2],
            customer_id=updated_opportunity[3],
            title=updated_opportunity[4],
            type=updated_opportunity[5],
            probability=updated_opportunity[6],
            total_value=updated_opportunity[7],
            crm_id=updated_opportunity[8],
            customer_name=updated_opportunity[9],
            end_user_name=updated_opportunity[10],
            region=updated_opportunity[11],
            industry_code=updated_opportunity[12],
            business_unit=updated_opportunity[13],
            project_type=updated_opportunity[14],
            delivery_duration=updated_opportunity[15],
            stage=updated_opportunity[16],
            status=updated_opportunity[17],
            expected_award_date=updated_opportunity[18],
            expected_rfx_date=updated_opportunity[19],
            close_date=updated_opportunity[20],
            competition=updated_opportunity[21],
            gross_profit_percent=updated_opportunity[22],
            gross_profit_value=updated_opportunity[23],
            description=updated_opportunity[24],
            last_updated_at=updated_opportunity[25],
            forcasted=updated_opportunity[26],
            company_name=updated_opportunity[27],
            company_email=updated_opportunity[28],
            company_logo=updated_opportunity[29],
            ct_customer_name=updated_opportunity[30],
            customer_email=updated_opportunity[31]
        )
    else:
        raise HTTPException(status_code=404, detail="Opportunity update failed")


def delete_opportunity(opportunity_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT delete_opportunity_disable_FK(%s);"
    cursor.execute(query, (opportunity_id,))
    deleted_opportunity = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_opportunity:
        return True
    else:
        return False


def get_opportunity_by_id(tenant_id: int, opportunity_id: int) -> Optional[Opportunity]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT o.*, 
            p.company_name, p.email AS company_email, p.company_logo,
            c.customer_name AS ct_customer_name, c.email AS customer_email
            FROM opportunity o
            INNER JOIN company p ON p.company_id=o.company_id
            INNER JOIN customer c ON c.customer_id=o.customer_id
        WHERE o.tenant_id = %s AND o.opportunity_id = %s;
        """
    cursor.execute(query, (tenant_id, opportunity_id,))
    opportunity = cursor.fetchone()

    conn.close()

    if opportunity:
        return Opportunity(
            opportunity_id=opportunity[0],
            tenant_id=opportunity[1],
            company_id=opportunity[2],
            customer_id=opportunity[3],
            title=opportunity[4],
            type=opportunity[5],
            probability=opportunity[6],
            total_value=opportunity[7],
            crm_id=opportunity[8],
            customer_name=opportunity[9],
            end_user_name=opportunity[10],
            region=opportunity[11],
            industry_code=opportunity[12],
            business_unit=opportunity[13],
            project_type=opportunity[14],
            delivery_duration=opportunity[15],
            stage=opportunity[16],
            status=opportunity[17],
            expected_award_date=opportunity[18],
            expected_rfx_date=opportunity[19],
            close_date=opportunity[20],
            competition=opportunity[21],
            gross_profit_percent=opportunity[22],
            gross_profit_value=opportunity[23],
            description=opportunity[24],
            last_updated_at=opportunity[25],
            forcasted=opportunity[26],
            company_name=opportunity[27],
            company_email=opportunity[28],
            company_logo=opportunity[29],
            ct_customer_name=opportunity[30],
            customer_email=opportunity[31]

        )
            
            
def get_opportunity_by_title(tenant_id: int, title: str) -> Optional[Opportunity]:
    conn = get_db_connection()
    cursor = conn.cursor()

    

    query = """
        SELECT o.*, 
            p.company_name, p.email AS company_email, p.company_logo,
            c.customer_name AS ct_customer_name, c.email AS customer_email
            FROM opportunity o
            INNER JOIN company p ON p.company_id=o.company_id
            INNER JOIN customer c ON c.customer_id=o.customer_id
        WHERE o.tenant_id = %s AND lower(o.title) = %s;
        """

    cursor.execute(query, (tenant_id, title.lower(),))
    opportunity = cursor.fetchone()

    conn.close()

    if opportunity:
            return Opportunity(
            opportunity_id=opportunity[0],
            tenant_id=opportunity[1],
            company_id=opportunity[2],
            customer_id=opportunity[3],
            title=opportunity[4],
            type=opportunity[5],
            probability=opportunity[6],
            total_value=opportunity[7],
            crm_id=opportunity[8],
            customer_name=opportunity[9],
            end_user_name=opportunity[10],
            region=opportunity[11],
            industry_code=opportunity[12],
            business_unit=opportunity[13],
            project_type=opportunity[14],
            delivery_duration=opportunity[15],
            stage=opportunity[16],
            status=opportunity[17],
            expected_award_date=opportunity[18],
            expected_rfx_date=opportunity[19],
            close_date=opportunity[20],
            competition=opportunity[21],
            gross_profit_percent=opportunity[22],
            gross_profit_value=opportunity[23],
            description=opportunity[24],
            last_updated_at=opportunity[25],
            forcasted=opportunity[26],
            company_name=opportunity[27],
            company_email=opportunity[28],
            company_logo=opportunity[29],
            ct_customer_name=opportunity[30],
            customer_email=opportunity[31]
        )
    else:
        raise HTTPException(status_code=404, detail="Opportunity not found")  

def delete_all_opportunity_record(opportunity_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()  

    query = "SELECT delete_opportunity_disable_FK(%s);"
    cursor.execute(query, (opportunity_id,))
           
    
    deleted_company = cursor.fetchone()
    

    conn.commit()
    conn.close()
                
        
    if deleted_company:
        return True
    else:
        return False

          