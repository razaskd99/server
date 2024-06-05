from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import OpportunityCreate, Opportunity, OpportunityGet, OpportunityGetMax
from datetime import date, datetime


def create_opportunity(opportunity_data: OpportunityCreate) -> Optional[Opportunity]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO opportunity (
        tenant_id, 
        account_id, 
        opp_number, 
        opp_title, 
        customer_id, 
        enduser_id, 
        enduser_project, 
        opp_value, 
        opp_currency, 
        opp_sale_stage, 
        opp_pursuit_progress, 
        opp_business_line, 
        opp_commited_sales_budget, 
        opp_industry, 
        opp_owner_id, 
        region, 
        bidding_unit, 
        project_type, 
        opp_type, 
        description, 
        status, 
        expected_award_date, 
        expected_rfx_date, 
        close_date, 
        updated_at, 
        created_at, 
        data 
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        opportunity_data.tenant_id,
        opportunity_data.account_id, 
        opportunity_data.opp_number, 
        opportunity_data.opp_title, 
        opportunity_data.customer_id, 
        opportunity_data.enduser_id, 
        opportunity_data.enduser_project, 
        opportunity_data.opp_value, 
        opportunity_data.opp_currency, 
        opportunity_data.opp_sale_stage, 
        opportunity_data.opp_pursuit_progress, 
        opportunity_data.opp_business_line, 
        opportunity_data.opp_commited_sales_budget, 
        opportunity_data.opp_industry, 
        opportunity_data.opp_owner_id, 
        opportunity_data.region, 
        opportunity_data.bidding_unit, 
        opportunity_data.project_type, 
        opportunity_data.opp_type, 
        opportunity_data.description,
        opportunity_data.status, 
        opportunity_data.expected_award_date, 
        opportunity_data.expected_rfx_date, 
        opportunity_data.close_date, 
        opportunity_data.updated_at, 
        opportunity_data.created_at, 
        opportunity_data.data 
    )

    cursor.execute(query, values)
    new_opportunity = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if new_opportunity:
        return Opportunity(
            opportunity_id=new_opportunity[0],
            tenant_id=new_opportunity[1],
            account_id=new_opportunity[2],
            opp_number=new_opportunity[3],
            opp_title=new_opportunity[4],
            customer_id=new_opportunity[5],
            enduser_id=new_opportunity[6],
            enduser_project=new_opportunity[7],
            opp_value=new_opportunity[8],
            opp_currency=new_opportunity[9],
            opp_sale_stage=new_opportunity[10],
            opp_pursuit_progress=new_opportunity[11],
            opp_business_line=new_opportunity[12],
            opp_commited_sales_budget=new_opportunity[13],
            opp_industry=new_opportunity[14],
            opp_owner_id=new_opportunity[15],
            region=new_opportunity[16],
            bidding_unit=new_opportunity[17],
            project_type=new_opportunity[18],
            opp_type=new_opportunity[19],
            description=new_opportunity[20],
            status=new_opportunity[21],
            expected_award_date=new_opportunity[22],
            expected_rfx_date=new_opportunity[23],
            close_date=new_opportunity[24],
            updated_at=new_opportunity[25],
            created_at=new_opportunity[26],
            data=new_opportunity[27]            
        )
    else:
        raise HTTPException(status_code=404, detail="Opportunity creation failed")


def get_all_opportunities(tenant_id: int, searchTerm: str, offset: int, limit: int) :
    conn = get_db_connection()
    cursor = conn.cursor()
    print(searchTerm)
    if searchTerm:
        searchTerm = '%' + searchTerm.lower() + '%'
        query = """
            SELECT o.*, a.account_name AS enduser_name, aa.account_name AS customer_name, CONCAT(u.first_name, ' ', u.last_name) AS owner_name
                FROM opportunity o
                LEFT JOIN account a ON a.account_id=o.enduser_id 
                LEFT JOIN account aa ON aa.account_id=o.customer_id 
                LEFT JOIN users u ON u.user_id=o.opp_owner_id 
            WHERE o.tenant_id = %s AND lower(o.opp_title) LIKE %s
            ORDER BY o.created_at DESC
            OFFSET %s LIMIT %s;
            """
        cursor.execute(query, (tenant_id, searchTerm, offset, limit))
        opportunities = cursor.fetchall()
    else:
        query = """ 
            SELECT o.*, a.account_name AS enduser_name, aa.account_name AS customer_name, CONCAT(u.first_name, ' ', u.last_name) AS owner_name
                FROM opportunity o
                LEFT JOIN account a ON a.account_id=o.enduser_id 
                LEFT JOIN account aa ON aa.account_id=o.customer_id 
                LEFT JOIN users u ON u.user_id=o.opp_owner_id 
            WHERE o.tenant_id = %s 
            ORDER BY o.created_at DESC
            OFFSET %s LIMIT %s;
            """
        cursor.execute(query, (tenant_id, offset, limit))
        opportunities = cursor.fetchall()
    
    # Query to get total count without offset and limit
    query_total_count = "SELECT COUNT(*) FROM opportunity WHERE tenant_id = %s;"
    cursor.execute(query_total_count, (tenant_id, ))
    total_count = cursor.fetchone()
    conn.close()    
    
    if opportunities:
        return {
            "data": [
                OpportunityGet(
                    opportunity_id=row[0],
                    tenant_id=row[1],
                    account_id=row[2],
                    opp_number=row[3],
                    opp_title=row[4],
                    customer_id=row[5],
                    enduser_id=row[6],
                    enduser_project=row[7],
                    opp_value=row[8],
                    opp_currency=row[9],
                    opp_sale_stage=row[10],
                    opp_pursuit_progress=row[11],
                    opp_business_line=row[12],
                    opp_commited_sales_budget=row[13],
                    opp_industry=row[14],
                    opp_owner_id=row[15],
                    region=row[16],
                    bidding_unit=row[17],
                    project_type=row[18],
                    opp_type=row[19],
                    description=row[20],
                    status=row[21],
                    expected_award_date=row[22],
                    expected_rfx_date=row[23],
                    close_date=row[24],
                    updated_at=row[25],
                    created_at=row[26],
                    data=row[27],
                    enduser_name=row[28],
                    customer_name=row[29], 
                    owner_name=row[30]           
                )
                for row in opportunities
            ],
            "total_count": total_count
        }
    else:
        None


def update_opportunity(opportunity_id: int, opportunity_data: OpportunityCreate) -> Optional[Opportunity]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE opportunity SET
        account_id = %s, 
        opp_number = %s, 
        opp_title = %s, 
        customer_id = %s, 
        enduser_id = %s, 
        enduser_project = %s, 
        opp_value = %s, 
        opp_currency = %s, 
        opp_sale_stage = %s, 
        opp_pursuit_progress = %s, 
        opp_business_line = %s, 
        opp_commited_sales_budget = %s, 
        opp_industry = %s, 
        opp_owner_id = %s, 
        region = %s, 
        bidding_unit = %s, 
        project_type = %s, 
        opp_type = %s, 
        description = %s, 
        status = %s, 
        expected_award_date = %s, 
        expected_rfx_date = %s, 
        close_date = %s, 
        updated_at = %s, 
        data = %s
    WHERE opportunity_id = %s RETURNING *;
    """

    values = (
        opportunity_data.account_id, 
        opportunity_data.opp_number, 
        opportunity_data.opp_title, 
        opportunity_data.customer_id, 
        opportunity_data.enduser_id, 
        opportunity_data.enduser_project, 
        opportunity_data.opp_value, 
        opportunity_data.opp_currency, 
        opportunity_data.opp_sale_stage, 
        opportunity_data.opp_pursuit_progress, 
        opportunity_data.opp_business_line, 
        opportunity_data.opp_commited_sales_budget, 
        opportunity_data.opp_industry, 
        opportunity_data.opp_owner_id, 
        opportunity_data.region, 
        opportunity_data.bidding_unit, 
        opportunity_data.project_type, 
        opportunity_data.opp_type, 
        opportunity_data.description,
        opportunity_data.status, 
        opportunity_data.expected_award_date, 
        opportunity_data.expected_rfx_date, 
        opportunity_data.close_date, 
        opportunity_data.updated_at, 
        opportunity_data.data, 
        opportunity_id
    )

    cursor.execute(query, values)
    update_opportunity = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if update_opportunity:
        return Opportunity(
            opportunity_id=update_opportunity[0],
            tenant_id=update_opportunity[1],
            account_id=update_opportunity[2],
            opp_number=update_opportunity[3],
            opp_title=update_opportunity[4],
            customer_id=update_opportunity[5],
            enduser_id=update_opportunity[6],
            enduser_project=update_opportunity[7],
            opp_value=update_opportunity[8],
            opp_currency=update_opportunity[9],
            opp_sale_stage=update_opportunity[10],
            opp_pursuit_progress=update_opportunity[11],
            opp_business_line=update_opportunity[12],
            opp_commited_sales_budget=update_opportunity[13],
            opp_industry=update_opportunity[14],
            opp_owner_id=update_opportunity[15],
            region=update_opportunity[16],
            bidding_unit=update_opportunity[17],
            project_type=update_opportunity[18],
            opp_type=update_opportunity[19],
            description=update_opportunity[20],
            status=update_opportunity[21],
            expected_award_date=update_opportunity[22],
            expected_rfx_date=update_opportunity[23],
            close_date=update_opportunity[24],
            updated_at=update_opportunity[25],
            created_at=update_opportunity[26],
            data=update_opportunity[27]            
        )
    else:
        raise HTTPException(status_code=404, detail="Opportunity update failed")


def delete_opportunity(opportunity_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM opportunity WHERE opportunity_id = %s RETURNING opportunity_id;"
    cursor.execute(query, (opportunity_id,))
    deleted_opportunity = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_opportunity:
        return True
    else:
        return False


def get_opportunity_by_id(opportunity_id: int) -> Optional[OpportunityGet]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT o.*, a.account_name AS enduser_name, aa.account_name AS customer_name, CONCAT(u.first_name, ' ', u.last_name) AS owner_name
            FROM opportunity o
            LEFT JOIN account a ON a.account_id=o.enduser_id 
            LEFT JOIN account aa ON aa.account_id=o.customer_id 
            LEFT JOIN users u ON u.user_id=o.opp_owner_id        
        WHERE o.opportunity_id = %s
        ORDER BY o.created_at DESC;
        """
    cursor.execute(query, (opportunity_id,))
    opportunity = cursor.fetchone()

    conn.close()

    if opportunity:
        return OpportunityGet(
            opportunity_id=opportunity[0],
            tenant_id=opportunity[1],
            account_id=opportunity[2],
            opp_number=opportunity[3],
            opp_title=opportunity[4],
            customer_id=opportunity[5],
            enduser_id=opportunity[6],
            enduser_project=opportunity[7],
            opp_value=opportunity[8],
            opp_currency=opportunity[9],
            opp_sale_stage=opportunity[10],
            opp_pursuit_progress=opportunity[11],
            opp_business_line=opportunity[12],
            opp_commited_sales_budget=opportunity[13],
            opp_industry=opportunity[14],
            opp_owner_id=opportunity[15],
            region=opportunity[16],
            bidding_unit=opportunity[17],
            project_type=opportunity[18],
            opp_type=opportunity[19],
            description=opportunity[20],
            status=opportunity[21],
            expected_award_date=opportunity[22],
            expected_rfx_date=opportunity[23],
            close_date=opportunity[24],
            updated_at=opportunity[25],
            created_at=opportunity[26],
            data=opportunity[27],
            enduser_name=opportunity[28],
            customer_name=opportunity[29],  
            owner_name=opportunity[30] 
        )
            
            
def get_opportunity_by_title(tenant_id: int, title: str) -> Optional[OpportunityGet]:
    title = title.replace("-", " ")

    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
         SELECT o.*, a.account_name AS enduser_name, aa.account_name AS customer_name, CONCAT(u.first_name, ' ', u.last_name) AS owner_name
            FROM opportunity o
            LEFT JOIN account a ON a.account_id=o.enduser_id 
            LEFT JOIN account aa ON aa.account_id=o.customer_id 
            LEFT JOIN users u ON u.user_id=o.opp_owner_id        
        WHERE o.tenant_id = %s AND lower(o.opp_title) = %s
        ORDER BY o.created_at DESC;
        """

    cursor.execute(query, (tenant_id, title.lower(),))
    opportunity = cursor.fetchone()

    conn.close()

    if opportunity:
            return OpportunityGet(
                opportunity_id=opportunity[0],
                tenant_id=opportunity[1],
                account_id=opportunity[2],
                opp_number=opportunity[3],
                opp_title=opportunity[4],
                customer_id=opportunity[5],
                enduser_id=opportunity[6],
                enduser_project=opportunity[7],
                opp_value=opportunity[8],
                opp_currency=opportunity[9],
                opp_sale_stage=opportunity[10],
                opp_pursuit_progress=opportunity[11],
                opp_business_line=opportunity[12],
                opp_commited_sales_budget=opportunity[13],
                opp_industry=opportunity[14],
                opp_owner_id=opportunity[15],
                region=opportunity[16],
                bidding_unit=opportunity[17],
                project_type=opportunity[18],
                opp_type=opportunity[19],
                description=opportunity[20],
                status=opportunity[21],
                expected_award_date=opportunity[22],
                expected_rfx_date=opportunity[23],
                close_date=opportunity[24],
                updated_at=opportunity[25],
                created_at=opportunity[26],
                data=opportunity[27],
                enduser_name=opportunity[28],
                customer_name=opportunity[29],  
                owner_name=opportunity[30]           
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


def get_opportunity_id_max() -> Optional[OpportunityGetMax]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT max(opportunity_id), max(opp_number) from opportunity;
        """

    cursor.execute(query,)
    opportunity = cursor.fetchone()
    
    conn.close()
    
    if opportunity:
        return OpportunityGetMax(
                opportunity_id=opportunity[0],
                opp_number=opportunity[1]
            )
    else:
        None