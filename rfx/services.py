from typing import List, Optional
from datetime import date, datetime
from .schemas import Rfx, RfxCreate, RfxGet, RfxGetSingleRec, RfxUpdateAcknowledgement 
from .schemas import RfxUpdateRfxNumber, RfxUpdateBidNumber, RfxUpdateBidAssignTo
from db.connection import get_db_connection

# Function to create an RFX
def create_rfx(rfx_data: RfxCreate) -> Optional[RfxGetSingleRec]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO rfx(
        tenant_id, opportunity_id, initiator_id, rfx_bid_assignto, rfx_title, rfx_number, 
        under_existing_agreement, status, previous_rfx_ref_num, revision_of_previous_rfx, agreement_ref_num, 
        issued_date, due_date, crm_id, bid_number, request_for_bid, submission_instructions, visit_worksite, 
        visit_worksite_instructions, tech_clarification_deadline, com_clarification_deadline, 
        expected_award_date, enduser_id, enduser_type, rfx_type_id, bid_validity_id,rfx_content_submission_id,
        rfx_submission_mode_id, rfx_stage_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *;
        """

    cursor.execute(query, (
        rfx_data.tenant_id, rfx_data.opportunity_id, rfx_data.initiator_id, rfx_data.rfx_bid_assignto, rfx_data.rfx_title,
        rfx_data.rfx_number, rfx_data.under_existing_agreement, rfx_data.status,
        rfx_data.previous_rfx_ref_num, rfx_data.revision_of_previous_rfx, rfx_data.agreement_ref_num, rfx_data.issued_date,
        rfx_data.due_date, rfx_data.crm_id, rfx_data.bid_number, rfx_data.request_for_bid,
        rfx_data.submission_instructions, rfx_data.visit_worksite, rfx_data.visit_worksite_instructions, 
        rfx_data.tech_clarification_deadline, rfx_data.com_clarification_deadline,
        rfx_data.expected_award_date, rfx_data.enduser_id, rfx_data.enduser_type,
        rfx_data.rfx_type_id, rfx_data.bid_validity_id, rfx_data.rfx_content_submission_id, 
        rfx_data.rfx_submission_mode_id, rfx_data.rfx_stage_id)
    )

    rfx = cursor.fetchone()
    
    if rfx:
        query = """
        INSERT INTO rfx_acknowledgement(
        rfx_id, acknowledged_by, acknowledgement_date, acknowledgement_comment, acknowledged, 
        acknowledgement_document, acknowledgement_submitted_on)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING *;
        """
        
        cursor.execute(query, (
            rfx[0], rfx_data.acknowledged_by, rfx_data.acknowledgement_date, rfx_data.acknowledgement_comment, 
            rfx_data.acknowledged, rfx_data.acknowledgement_document, rfx_data.acknowledgement_submitted_on)
        )    
        
        ack = cursor.fetchone()
        
           
    conn.commit()
    conn.close()
   
    if rfx:
        return RfxGetSingleRec(
            rfx_id=rfx[0],            
            tenant_id=rfx[1],
            opportunity_id=rfx[2],
            initiator_id=rfx[3],
            rfx_bid_assignto=rfx[4],
            rfx_title=rfx[5],
            rfx_number=rfx[6],
            under_existing_agreement=rfx[7],
            status=rfx[8],
            previous_rfx_ref_num=rfx[9],
            revision_of_previous_rfx=rfx[10],
            agreement_ref_num=rfx[11],
            issued_date=rfx[12],
            due_date=rfx[13],
            crm_id=rfx[14],
            bid_number=rfx[15],
            request_for_bid=rfx[16],
            submission_instructions=rfx[17],
            visit_worksite=rfx[18],
            visit_worksite_instructions=rfx[19],
            tech_clarification_deadline=rfx[20],
            com_clarification_deadline=rfx[21],
            expected_award_date=rfx[22],
            enduser_id=rfx[23],
            enduser_type=rfx[24],
            rfx_type_id= rfx[25],
            bid_validity_id= rfx[26],
            rfx_content_submission_id= rfx[27],
            rfx_submission_mode_id= rfx[28],
            rfx_stage_id= rfx[28],
            # rfx acknowledgement
            acknowledged_by=ack[2],
            acknowledgement_date=ack[3],
            acknowledgement_comment=ack[4],
            acknowledged=ack[5],
            acknowledgement_document=ack[6],
            acknowledgement_submitted_on=ack[7]                        
        ) 
        
    else:
        return None 



# Function to retrieve all RFXs
def get_all_rfx(tenant_id: int) -> List[Rfx]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT r.*,
            o.title AS opportunity_title, o.type AS opportunity_type, o.probability, o.total_value, 
            o.end_user_name, o.region, o.industry_code, o.business_unit, o.project_type, 
            o.delivery_duration, r5.title AS opportunity_stage, o.status AS opportunity_status,  
            o.expected_rfx_date, o.close_date, o.competition, o.gross_profit_percent, o.gross_profit_value, 
            o.description AS opportunity_description, 
            o.last_updated_at AS opportunity_last_updated_at, o.forcasted, 
            c.customer_id, c.customer_name, c.email AS customer_email, c.phone AS customer_phone, 
            c.address AS customer_address, 
            p.company_id, p.company_name, p.email AS company_email, 
            p.phone AS company_phone, p.website AS company_website, p.company_logo,
            a.acknowledged_by, a.acknowledgement_date, a.acknowledgement_comment, a.acknowledged, 
            a.acknowledgement_document, a.acknowledgement_submitted_on,
            u.first_name AS initiator_first_name, u.middle_name AS initiator_middle_name, 
            u.last_name AS initiator_last_name,	u.email AS initiator_email, u.user_role AS initiator_role, 
		    u.role_level AS initiator_role_level, u.team_id AS initiator_team_id,
            r1.title AS rfx_type, r2.title AS bid_validity, r3.title AS submission_content,
            r4.title AS submission_mode, r5.title AS rfx_stage_title
        FROM rfx r
        LEFT JOIN rfx_acknowledgement a ON a.rfx_id = r.rfx_id
        LEFT JOIN opportunity o ON o.opportunity_id = r.opportunity_id
        LEFT JOIN customer c ON c.customer_id = o.customer_id
        LEFT JOIN company p ON p.company_id = o.company_id
        LEFT JOIN users u ON u.user_id=r.initiator_id
        LEFT JOIN rfx_type r1 ON r1.rfx_type_id=r.rfx_type_id
        LEFT JOIN bid_validity r2 ON r2.bid_validity_id=r.bid_validity_id
        LEFT JOIN rfx_content_submission r3 ON r3.rfx_content_submission_id=r.rfx_content_submission_id
        LEFT JOIN rfx_submission_mode r4 ON r4.rfx_submission_mode_id=r.rfx_submission_mode_id
        LEFT JOIN rfx_stage r5 ON r5.rfx_stage_id=r.rfx_stage_id
        WHERE r.tenant_id = %s
        ORDER BY r.rfx_id DESC
        """

    try:
        cursor.execute(query, (tenant_id,))
        rfxs = cursor.fetchall()        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()


    return [
        Rfx(
            rfx_id=row[0],tenant_id=row[1],opportunity_id=row[2],initiator_id=row[3],rfx_bid_assignto=row[4],
            rfx_title=row[5],rfx_number=row[6],under_existing_agreement=row[7],status=row[8],
            previous_rfx_ref_num=row[9],revision_of_previous_rfx=row[10],agreement_ref_num=row[11],
            issued_date=row[12],due_date=row[13],crm_id=row[14],bid_number=row[15],
            request_for_bid=row[16],submission_instructions=row[17],
            visit_worksite=row[18],visit_worksite_instructions=row[19],tech_clarification_deadline=row[20],
            com_clarification_deadline=row[21],expected_award_date=row[22],enduser_id=row[23],enduser_type=row[24],
            # end rfx
            opportunity_title=row[30],opportunity_type=row[31],probability=row[32],total_value=row[33],
            end_user_name=row[34],region=row[35],industry_code=row[36],business_unit=row[37],project_type=row[38],
            delivery_duration=row[39],opportunity_stage=row[40],opportunity_status=row[41],expected_rfx_date=row[42],
            close_date=row[43],competition=row[44],gross_profit_percent=row[45],gross_profit_value=row[46],
            opportunity_description=row[47],opportunity_last_updated_at=row[48],forcasted=row[49],            
            # end opportunity
            customer_id=row[50],customer_name=row[51],customer_email=row[52],customer_phone=row[53],
            customer_address=row[54],
            # end customer
            company_id=row[55],company_name=row[56],company_email=row[57],company_phone=row[58],
            company_website=row[59],company_logo=row[60],
            # end company
            acknowledged_by=row[61],acknowledgement_date=row[62],acknowledgement_comment=row[63],
            acknowledged=row[64],acknowledgement_document=row[65],acknowledgement_submitted_on=row[66],
            # end acknowledgement
            initiator_first_name=row[67],initiator_middle_name=row[68],initiator_last_name=row[69],
            initiator_email=row[70],initiator_role=row[71],initiator_role_level=row[72],initiator_team_id=row[73],
            # end initiator
            rfx_type=row[74] or "",bid_validity=row[75] or "",submission_content=row[76] or "",
            submission_mode=row[77] or "", rfx_stage_title=row[78] or "",            
            # end rfx prerequesites
            rfx_type_id=row[25], bid_validity_id=row[26], rfx_content_submission_id=row[27],
            rfx_submission_mode_id=row[28], rfx_stage_id=row[29]    
            # end rfx prerequesites id   
        )
        for row in rfxs
    ]

 
def update_rfx(rfx_id: int, rfx_data: RfxGet) -> Optional[RfxGetSingleRec]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE rfx SET
        rfx_bid_assignto = %s,
        rfx_title = %s,
        rfx_number = %s,    
        under_existing_agreement = %s,
        status = %s,
        previous_rfx_ref_num = %s,
        revision_of_previous_rfx = %s,
        agreement_ref_num = %s,
        issued_date = %s,
        due_date = %s,
        crm_id = %s,
        bid_number = %s,
        request_for_bid = %s,
        submission_instructions = %s,
        visit_worksite = %s,
        visit_worksite_instructions = %s,
        tech_clarification_deadline = %s,
        com_clarification_deadline = %s,
        expected_award_date = %s,
        enduser_id = %s,
        enduser_type = %s,        
        rfx_type_id = %s,
        bid_validity_id = %s,
        rfx_content_submission_id = %s,
        rfx_submission_mode_id = %s,
        rfx_stage_id = %s        
        WHERE rfx_id = %s
        RETURNING *;
        """

    values = (
        rfx_data.rfx_bid_assignto,
        rfx_data.rfx_title,
        rfx_data.rfx_number,
        rfx_data.under_existing_agreement,
        rfx_data.status,
        rfx_data.previous_rfx_ref_num,
        rfx_data.revision_of_previous_rfx,
        rfx_data.agreement_ref_num,
        rfx_data.issued_date,
        rfx_data.due_date,
        rfx_data.crm_id,
        rfx_data.bid_number,
        rfx_data.request_for_bid,
        rfx_data.submission_instructions,
        rfx_data.visit_worksite,
        rfx_data.visit_worksite_instructions,
        rfx_data.tech_clarification_deadline,
        rfx_data.com_clarification_deadline,
        rfx_data.expected_award_date,
        rfx_data.enduser_id,
        rfx_data.enduser_type,
        rfx_data.rfx_type_id,
        rfx_data.bid_validity_id,
        rfx_data.rfx_content_submission_id,
        rfx_data.rfx_submission_mode_id,
        rfx_data.rfx_stage_id,
        rfx_id        
    )
        
   
    cursor.execute(query, values)
    updated_rfx = cursor.fetchone()
       
    
    if updated_rfx:
        query = """
            UPDATE rfx_acknowledgement SET
            acknowledged_by = %s,
            acknowledgement_date = %s,
            acknowledgement_comment = %s,    
            acknowledged = %s,
            acknowledgement_document = %s,
            acknowledgement_submitted_on = %s
            WHERE rfx_id = %s
            RETURNING *;
            """
            
        values = (
            rfx_data.acknowledged_by,
            rfx_data.acknowledgement_date,
            rfx_data.acknowledgement_comment,
            rfx_data.acknowledged,
            rfx_data.acknowledgement_document,
            rfx_data.acknowledgement_submitted_on,
            rfx_id
        )
    
    cursor.execute(query, values)
    updated_acknowledgement = cursor.fetchone()
                
    print(update_rfx) 
    conn.commit()
    conn.close()
    
    if updated_acknowledgement and update_rfx:
        return RfxGetSingleRec(
            rfx_id=updated_rfx[0],            
            tenant_id=updated_rfx[1],
            opportunity_id=updated_rfx[2],
            initiator_id=updated_rfx[3],
            rfx_bid_assignto=updated_rfx[4],
            rfx_title=updated_rfx[5],
            rfx_number=updated_rfx[6],
            under_existing_agreement=updated_rfx[7],
            status=updated_rfx[8],
            previous_rfx_ref_num=updated_rfx[9],
            revision_of_previous_rfx=updated_rfx[10],
            agreement_ref_num=updated_rfx[11],
            issued_date=updated_rfx[12],
            due_date=updated_rfx[13],
            crm_id=updated_rfx[14],
            bid_number=updated_rfx[15],
            request_for_bid=updated_rfx[16],
            submission_instructions=updated_rfx[17],
            visit_worksite=updated_rfx[18],
            visit_worksite_instructions=updated_rfx[19],
            tech_clarification_deadline=updated_rfx[20],
            com_clarification_deadline=updated_rfx[21],
            expected_award_date=updated_rfx[22],
            enduser_id=updated_rfx[23],
            enduser_type=updated_rfx[24],
            rfx_type_id= updated_rfx[25],
            bid_validity_id= updated_rfx[26],
            rfx_content_submission_id= updated_rfx[27],
            rfx_submission_mode_id= updated_rfx[28],
            rfx_stage_id= updated_rfx[28],
            # rfx acknowledgement
            acknowledged_by=updated_acknowledgement[2],
            acknowledgement_date=updated_acknowledgement[3],
            acknowledgement_comment=updated_acknowledgement[4],
            acknowledged=updated_acknowledgement[5],
            acknowledgement_document=updated_acknowledgement[6],
            acknowledgement_submitted_on=updated_acknowledgement[7]                        
        )
    else:
        return None


def update_rfx_number(rfx_id: int, rfx_data: RfxUpdateRfxNumber) -> Optional[bool]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE rfx SET
            rfx_number = %s    
            WHERE rfx_id = %s
        RETURNING *;
        """
    values = (
        rfx_data.rfx_number,
        rfx_id        
    )        
   
    cursor.execute(query, values)
    updated_rfx = cursor.fetchone()
                
    conn.commit()
    conn.close()
    
    if updated_rfx:
        return True
    else:
        return False


def update_bid_number(rfx_id: int, rfx_data: RfxUpdateBidNumber) -> Optional[bool]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE rfx SET 
            bid_number = %s    
            WHERE rfx_id = %s
        RETURNING *;
        """
    values = (
        rfx_data.bid_number,
        rfx_id        
    )        
   
    cursor.execute(query, values)
    updated_rfx = cursor.fetchone()
                
    conn.commit()
    conn.close()
    
    if updated_rfx:
        return True
    else:
        return False


def update_bid_assignto(rfx_id: int, rfx_data: RfxUpdateBidAssignTo) -> Optional[bool]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE rfx SET
            rfx_bid_assignto = %s    
            WHERE rfx_id = %s
        RETURNING *;
        """
    values = (
        rfx_data.rfx_bid_assignto,
        rfx_id        
    )        
   
    cursor.execute(query, values)
    updated_rfx = cursor.fetchone()
                
    conn.commit()
    conn.close()
    
    if updated_rfx:
        return True
    else:
        return False


def update_rfx_acknowledgement(rfx_id: int, rfx_data: RfxUpdateAcknowledgement) -> Optional[RfxUpdateAcknowledgement]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE rfx_acknowledgement SET
        acknowledged_by = %s,
        acknowledgement_date = %s,
        acknowledgement_comment = %s,    
        acknowledged = %s,
        acknowledgement_document = %s,
        acknowledgement_submitted_on = %s
        WHERE rfx_id = %s
        RETURNING *;
        """
            
    values = (
        rfx_data.acknowledged_by,
        rfx_data.acknowledgement_date,
        rfx_data.acknowledgement_comment,
        rfx_data.acknowledged,
        rfx_data.acknowledgement_document,
        rfx_data.acknowledgement_submitted_on,
        rfx_id
    )
    
    cursor.execute(query, values)
    updated_acknowledgement = cursor.fetchone()
                
  
    conn.commit()
    conn.close()
    
    if updated_acknowledgement and update_rfx:
        return RfxUpdateAcknowledgement(
            # rfx acknowledgement
            rfx_acknowledgement=updated_acknowledgement[0],
            rfx_id=updated_acknowledgement[1],
            acknowledged_by=updated_acknowledgement[2],
            acknowledgement_date=updated_acknowledgement[3],
            acknowledgement_comment=updated_acknowledgement[4],
            acknowledged=updated_acknowledgement[5],
            acknowledgement_document=updated_acknowledgement[6],
            acknowledgement_submitted_on=updated_acknowledgement[7]                        
        )
    else:
        return None
   
    
def delete_rfx(rfx_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM rfx_acknowledgement WHERE rfx_id = %s RETURNING rfx_id;"
    cursor.execute(query, (rfx_id,))
    deleted_acknowledgement = cursor.fetchone()
    
    query = "DELETE FROM rfx WHERE rfx_id = %s RETURNING rfx_id;"
    cursor.execute(query, (rfx_id,))
    deleted_rfx = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_rfx and deleted_acknowledgement:
        return True
    else:
        return False 

# Function to retrieve an RFX by ID
def get_rfx_by_id(rfx_id: int) -> Optional[Rfx]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT r.*,
            o.title AS opportunity_title, o.type AS opportunity_type, o.probability, o.total_value, 
            o.end_user_name, o.region, o.industry_code, o.business_unit, o.project_type, 
            o.delivery_duration, r5.title AS opportunity_stage, o.status AS opportunity_status,  
            o.expected_rfx_date, o.close_date, o.competition, o.gross_profit_percent, o.gross_profit_value, 
            o.description AS opportunity_description, 
            o.last_updated_at AS opportunity_last_updated_at, o.forcasted, 
            c.customer_id, c.customer_name, c.email AS customer_email, c.phone AS customer_phone, 
            c.address AS customer_address, 
            p.company_id, p.company_name, p.email AS company_email, 
            p.phone AS company_phone, p.website AS company_website, p.company_logo,
            a.acknowledged_by, a.acknowledgement_date, a.acknowledgement_comment, a.acknowledged, 
            a.acknowledgement_document, a.acknowledgement_submitted_on,
            u.first_name AS initiator_first_name, u.middle_name AS initiator_middle_name, 
            u.last_name AS initiator_last_name,	u.email AS initiator_email, u.user_role AS initiator_role, 
		    u.role_level AS initiator_role_level, u.team_id AS initiator_team_id,
            r1.title AS rfx_type, r2.title AS bid_validity, r3.title AS submission_content,
            r4.title AS submission_mode, r5.title AS rfx_stage_title
        FROM rfx r
        LEFT JOIN rfx_acknowledgement a ON a.rfx_id = r.rfx_id
        LEFT JOIN opportunity o ON o.opportunity_id = r.opportunity_id
        LEFT JOIN customer c ON c.customer_id = o.customer_id
        LEFT JOIN company p ON p.company_id = o.company_id
        LEFT JOIN users u ON u.user_id=r.initiator_id
        LEFT JOIN rfx_type r1 ON r1.rfx_type_id=r.rfx_type_id
        LEFT JOIN bid_validity r2 ON r2.bid_validity_id=r.bid_validity_id
        LEFT JOIN rfx_content_submission r3 ON r3.rfx_content_submission_id=r.rfx_content_submission_id
        LEFT JOIN rfx_submission_mode r4 ON r4.rfx_submission_mode_id=r.rfx_submission_mode_id
        LEFT JOIN rfx_stage r5 ON r5.rfx_stage_id=r.rfx_stage_id
        WHERE  r.rfx_id = %s
        ORDER BY r.rfx_id DESC;
        """

    cursor.execute(query, (rfx_id,))
    rfx = cursor.fetchone()

    conn.close()

    if rfx:
        return Rfx(
            rfx_id=rfx[0],tenant_id=rfx[1],opportunity_id=rfx[2],initiator_id=rfx[3],rfx_bid_assignto=rfx[4],
            rfx_title=rfx[5],rfx_number=rfx[6],under_existing_agreement=rfx[7],status=rfx[8],
            previous_rfx_ref_num=rfx[9],revision_of_previous_rfx=rfx[10],agreement_ref_num=rfx[11],
            issued_date=rfx[12],due_date=rfx[13],crm_id=rfx[14],bid_number=rfx[15],
            request_for_bid=rfx[16],submission_instructions=rfx[17],
            visit_worksite=rfx[18],visit_worksite_instructions=rfx[19],tech_clarification_deadline=rfx[20],
            com_clarification_deadline=rfx[21],expected_award_date=rfx[22],enduser_id=rfx[23],enduser_type=rfx[24],
            # end rfx
            opportunity_title=rfx[30],opportunity_type=rfx[31],probability=rfx[32],total_value=rfx[33],
            end_user_name=rfx[34],region=rfx[35],industry_code=rfx[36],business_unit=rfx[37],project_type=rfx[38],
            delivery_duration=rfx[39],opportunity_stage=rfx[40],opportunity_status=rfx[41],expected_rfx_date=rfx[42],
            close_date=rfx[43],competition=rfx[44],gross_profit_percent=rfx[45],gross_profit_value=rfx[46],
            opportunity_description=rfx[47],opportunity_last_updated_at=rfx[48],forcasted=rfx[49],            
            # end opportunity
            customer_id=rfx[50],customer_name=rfx[51],customer_email=rfx[52],customer_phone=rfx[53],
            customer_address=rfx[54],
            # end customer
            company_id=rfx[55],company_name=rfx[56],company_email=rfx[57],company_phone=rfx[58],
            company_website=rfx[59],company_logo=rfx[60],
            # end company
            acknowledged_by=rfx[61],acknowledgement_date=rfx[62],acknowledgement_comment=rfx[63],
            acknowledged=rfx[64],acknowledgement_document=rfx[65],acknowledgement_submitted_on=rfx[66],
            # end acknowledgement
            initiator_first_name=rfx[67],initiator_middle_name=rfx[68],initiator_last_name=rfx[69],
            initiator_email=rfx[70],initiator_role=rfx[71],initiator_role_level=rfx[72],initiator_team_id=rfx[73],
            # end initiator
            rfx_type=rfx[74] or "",bid_validity=rfx[75] or "",submission_content=rfx[76] or "",
            submission_mode=rfx[77] or "", rfx_stage_title=rfx[78] or "",            
            # end rfx prerequesites
            rfx_type_id=rfx[25], bid_validity_id=rfx[26], rfx_content_submission_id=rfx[27],
            rfx_submission_mode_id=rfx[28], rfx_stage_id=rfx[29]    
            # end rfx prerequesites id    
        )
    else:
        return None
   
    
def get_rfx_by_initiator_id(tenant_id: int, initiator_id: int) -> List[Rfx]:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = """
        SELECT r.*,
            o.title AS opportunity_title, o.type AS opportunity_type, o.probability, o.total_value, 
            o.end_user_name, o.region, o.industry_code, o.business_unit, o.project_type, 
            o.delivery_duration, r5.title AS opportunity_stage, o.status AS opportunity_status,  
            o.expected_rfx_date, o.close_date, o.competition, o.gross_profit_percent, o.gross_profit_value, 
            o.description AS opportunity_description, 
            o.last_updated_at AS opportunity_last_updated_at, o.forcasted, 
            c.customer_id, c.customer_name, c.email AS customer_email, c.phone AS customer_phone, 
            c.address AS customer_address, 
            p.company_id, p.company_name, p.email AS company_email, 
            p.phone AS company_phone, p.website AS company_website, p.company_logo,
            a.acknowledged_by, a.acknowledgement_date, a.acknowledgement_comment, a.acknowledged, 
            a.acknowledgement_document, a.acknowledgement_submitted_on,
            u.first_name AS initiator_first_name, u.middle_name AS initiator_middle_name, 
            u.last_name AS initiator_last_name,	u.email AS initiator_email, u.user_role AS initiator_role, 
		    u.role_level AS initiator_role_level, u.team_id AS initiator_team_id,
            r1.title AS rfx_type, r2.title AS bid_validity, r3.title AS submission_content,
            r4.title AS submission_mode, r5.title AS rfx_stage_title
        FROM rfx r
        LEFT JOIN rfx_acknowledgement a ON a.rfx_id = r.rfx_id
        LEFT JOIN opportunity o ON o.opportunity_id = r.opportunity_id
        LEFT JOIN customer c ON c.customer_id = o.customer_id
        LEFT JOIN company p ON p.company_id = o.company_id
        LEFT JOIN users u ON u.user_id=r.initiator_id
        LEFT JOIN rfx_type r1 ON r1.rfx_type_id=r.rfx_type_id
        LEFT JOIN bid_validity r2 ON r2.bid_validity_id=r.bid_validity_id
        LEFT JOIN rfx_content_submission r3 ON r3.rfx_content_submission_id=r.rfx_content_submission_id
        LEFT JOIN rfx_submission_mode r4 ON r4.rfx_submission_mode_id=r.rfx_submission_mode_id
        LEFT JOIN rfx_stage r5 ON r5.rfx_stage_id=r.rfx_stage_id
        WHERE r.initiator_id = %s AND r.tenant_id = %s
        ORDER BY r.rfx_id DESC;
        """
    
                
    cursor.execute(query, (initiator_id, tenant_id))
    rfxs = cursor.fetchall()

    conn.close()

    return [
        Rfx(
            rfx_id=row[0],tenant_id=row[1],opportunity_id=row[2],initiator_id=row[3],rfx_bid_assignto=row[4],
            rfx_title=row[5],rfx_number=row[6],under_existing_agreement=row[7],status=row[8],
            previous_rfx_ref_num=row[9],revision_of_previous_rfx=row[10],agreement_ref_num=row[11],
            issued_date=row[12],due_date=row[13],crm_id=row[14],bid_number=row[15],
            request_for_bid=row[16],submission_instructions=row[17],
            visit_worksite=row[18],visit_worksite_instructions=row[19],tech_clarification_deadline=row[20],
            com_clarification_deadline=row[21],expected_award_date=row[22],enduser_id=row[23],enduser_type=row[24],
            # end rfx
            opportunity_title=row[30],opportunity_type=row[31],probability=row[32],total_value=row[33],
            end_user_name=row[34],region=row[35],industry_code=row[36],business_unit=row[37],project_type=row[38],
            delivery_duration=row[39],opportunity_stage=row[40],opportunity_status=row[41],expected_rfx_date=row[42],
            close_date=row[43],competition=row[44],gross_profit_percent=row[45],gross_profit_value=row[46],
            opportunity_description=row[47],opportunity_last_updated_at=row[48],forcasted=row[49],            
            # end opportunity
            customer_id=row[50],customer_name=row[51],customer_email=row[52],customer_phone=row[53],
            customer_address=row[54],
            # end customer
            company_id=row[55],company_name=row[56],company_email=row[57],company_phone=row[58],
            company_website=row[59],company_logo=row[60],
            # end company
            acknowledged_by=row[61],acknowledgement_date=row[62],acknowledgement_comment=row[63],
            acknowledged=row[64],acknowledgement_document=row[65],acknowledgement_submitted_on=row[66],
            # end acknowledgement
            initiator_first_name=row[67],initiator_middle_name=row[68],initiator_last_name=row[69],
            initiator_email=row[70],initiator_role=row[71],initiator_role_level=row[72],initiator_team_id=row[73],
            # end initiator
            rfx_type=row[74] or "",bid_validity=row[75] or "",submission_content=row[76] or "",
            submission_mode=row[77] or "", rfx_stage_title=row[78] or "",            
            # end rfx prerequesites
            rfx_type_id=row[25], bid_validity_id=row[26], rfx_content_submission_id=row[27],
            rfx_submission_mode_id=row[28], rfx_stage_id=row[29]    
            # end rfx prerequesites id  
        )
        for row in rfxs
    ]


# Function to retrieve RFXs by title
def get_rfx_by_rfx_title(tenant_id: int, rfx_title: str) -> Optional[Rfx]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT r.*,
            o.title AS opportunity_title, o.type AS opportunity_type, o.probability, o.total_value, 
            o.end_user_name, o.region, o.industry_code, o.business_unit, o.project_type, 
            o.delivery_duration, r5.title AS opportunity_stage, o.status AS opportunity_status,  
            o.expected_rfx_date, o.close_date, o.competition, o.gross_profit_percent, o.gross_profit_value, 
            o.description AS opportunity_description, 
            o.last_updated_at AS opportunity_last_updated_at, o.forcasted, 
            c.customer_id, c.customer_name, c.email AS customer_email, c.phone AS customer_phone, 
            c.address AS customer_address, 
            p.company_id, p.company_name, p.email AS company_email, 
            p.phone AS company_phone, p.website AS company_website, p.company_logo,
            a.acknowledged_by, a.acknowledgement_date, a.acknowledgement_comment, a.acknowledged, 
            a.acknowledgement_document, a.acknowledgement_submitted_on,
            u.first_name AS initiator_first_name, u.middle_name AS initiator_middle_name, 
            u.last_name AS initiator_last_name,	u.email AS initiator_email, u.user_role AS initiator_role, 
		    u.role_level AS initiator_role_level, u.team_id AS initiator_team_id,
            r1.title AS rfx_type, r2.title AS bid_validity, r3.title AS submission_content,
            r4.title AS submission_mode, r5.title AS rfx_stage_title
        FROM rfx r
        LEFT JOIN rfx_acknowledgement a ON a.rfx_id = r.rfx_id
        LEFT JOIN opportunity o ON o.opportunity_id = r.opportunity_id
        LEFT JOIN customer c ON c.customer_id = o.customer_id
        LEFT JOIN company p ON p.company_id = o.company_id
        LEFT JOIN users u ON u.user_id=r.initiator_id
        LEFT JOIN rfx_type r1 ON r1.rfx_type_id=r.rfx_type_id
        LEFT JOIN bid_validity r2 ON r2.bid_validity_id=r.bid_validity_id
        LEFT JOIN rfx_content_submission r3 ON r3.rfx_content_submission_id=r.rfx_content_submission_id
        LEFT JOIN rfx_submission_mode r4 ON r4.rfx_submission_mode_id=r.rfx_submission_mode_id
        LEFT JOIN rfx_stage r5 ON r5.rfx_stage_id=r.rfx_stage_id
        WHERE lower(r.rfx_title) = %s AND r.tenant_id = %s
        ORDER BY r.rfx_id DESC;
        """

    cursor.execute(query, (rfx_title.lower(), tenant_id,))
    rfx = cursor.fetchone()

    conn.close()

    if rfx:
        return Rfx(            
            rfx_id=rfx[0],tenant_id=rfx[1],opportunity_id=rfx[2],initiator_id=rfx[3],rfx_bid_assignto=rfx[4],
            rfx_title=rfx[5],rfx_number=rfx[6],under_existing_agreement=rfx[7],status=rfx[8],
            previous_rfx_ref_num=rfx[9],revision_of_previous_rfx=rfx[10],agreement_ref_num=rfx[11],
            issued_date=rfx[12],due_date=rfx[13],crm_id=rfx[14],bid_number=rfx[15],
            request_for_bid=rfx[16],submission_instructions=rfx[17],
            visit_worksite=rfx[18],visit_worksite_instructions=rfx[19],tech_clarification_deadline=rfx[20],
            com_clarification_deadline=rfx[21],expected_award_date=rfx[22],enduser_id=rfx[23],enduser_type=rfx[24],
            # end rfx
            opportunity_title=rfx[30],opportunity_type=rfx[31],probability=rfx[32],total_value=rfx[33],
            end_user_name=rfx[34],region=rfx[35],industry_code=rfx[36],business_unit=rfx[37],project_type=rfx[38],
            delivery_duration=rfx[39],opportunity_stage=rfx[40],opportunity_status=rfx[41],expected_rfx_date=rfx[42],
            close_date=rfx[43],competition=rfx[44],gross_profit_percent=rfx[45],gross_profit_value=rfx[46],
            opportunity_description=rfx[47],opportunity_last_updated_at=rfx[48],forcasted=rfx[49],            
            # end opportunity
            customer_id=rfx[50],customer_name=rfx[51],customer_email=rfx[52],customer_phone=rfx[53],
            customer_address=rfx[54],
            # end customer
            company_id=rfx[55],company_name=rfx[56],company_email=rfx[57],company_phone=rfx[58],
            company_website=rfx[59],company_logo=rfx[60],
            # end company
            acknowledged_by=rfx[61],acknowledgement_date=rfx[62],acknowledgement_comment=rfx[63],
            acknowledged=rfx[64],acknowledgement_document=rfx[65],acknowledgement_submitted_on=rfx[66],
            # end acknowledgement
            initiator_first_name=rfx[67],initiator_middle_name=rfx[68],initiator_last_name=rfx[69],
            initiator_email=rfx[70],initiator_role=rfx[71],initiator_role_level=rfx[72],initiator_team_id=rfx[73],
            # end initiator
            rfx_type=rfx[74] or "",bid_validity=rfx[75] or "",submission_content=rfx[76] or "",
            submission_mode=rfx[77] or "", rfx_stage_title=rfx[78] or "",
            # end rfx prerequesites
            rfx_type_id=rfx[25], bid_validity_id=rfx[26], rfx_content_submission_id=rfx[27],
            rfx_submission_mode_id=rfx[28], rfx_stage_id=rfx[29]    
            # end rfx prerequesites id  
        ) 
    else:
        return None


# Function to retrieve RFXs by rfx number
def get_rfx_by_rfx_number(tenant_id: int, rfx_number: str) ->  List[Rfx]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT r.*,
            o.title AS opportunity_title, o.type AS opportunity_type, o.probability, o.total_value, 
            o.end_user_name, o.region, o.industry_code, o.business_unit, o.project_type, 
            o.delivery_duration, r5.title AS opportunity_stage, o.status AS opportunity_status,  
            o.expected_rfx_date, o.close_date, o.competition, o.gross_profit_percent, o.gross_profit_value, 
            o.description AS opportunity_description, 
            o.last_updated_at AS opportunity_last_updated_at, o.forcasted, 
            c.customer_id, c.customer_name, c.email AS customer_email, c.phone AS customer_phone, 
            c.address AS customer_address, 
            p.company_id, p.company_name, p.email AS company_email, 
            p.phone AS company_phone, p.website AS company_website, p.company_logo,
            a.acknowledged_by, a.acknowledgement_date, a.acknowledgement_comment, a.acknowledged, 
            a.acknowledgement_document, a.acknowledgement_submitted_on,
            u.first_name AS initiator_first_name, u.middle_name AS initiator_middle_name, 
            u.last_name AS initiator_last_name,	u.email AS initiator_email, u.user_role AS initiator_role, 
		    u.role_level AS initiator_role_level, u.team_id AS initiator_team_id,
            r1.title AS rfx_type, r2.title AS bid_validity, r3.title AS submission_content,
            r4.title AS submission_mode, r5.title AS rfx_stage_title
        FROM rfx r
        LEFT JOIN rfx_acknowledgement a ON a.rfx_id = r.rfx_id
        LEFT JOIN opportunity o ON o.opportunity_id = r.opportunity_id
        LEFT JOIN customer c ON c.customer_id = o.customer_id
        LEFT JOIN company p ON p.company_id = o.company_id
        LEFT JOIN users u ON u.user_id=r.initiator_id
        LEFT JOIN rfx_type r1 ON r1.rfx_type_id=r.rfx_type_id
        LEFT JOIN bid_validity r2 ON r2.bid_validity_id=r.bid_validity_id
        LEFT JOIN rfx_content_submission r3 ON r3.rfx_content_submission_id=r.rfx_content_submission_id
        LEFT JOIN rfx_submission_mode r4 ON r4.rfx_submission_mode_id=r.rfx_submission_mode_id
        LEFT JOIN rfx_stage r5 ON r5.rfx_stage_id=r.rfx_stage_id
        WHERE lower(r.rfx_number) = %s AND r.tenant_id=%s
        ORDER BY r.rfx_id DESC;
        """
    
    try:
        cursor.execute(query, (rfx_number.lower(), tenant_id,))
        rfxs = cursor.fetchall()        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
            

    return [
            Rfx(
            rfx_id=row[0],tenant_id=row[1],opportunity_id=row[2],initiator_id=row[3],rfx_bid_assignto=row[4],
            rfx_title=row[5],rfx_number=row[6],under_existing_agreement=row[7],status=row[8],
            previous_rfx_ref_num=row[9],revision_of_previous_rfx=row[10],agreement_ref_num=row[11],
            issued_date=row[12],due_date=row[13],crm_id=row[14],bid_number=row[15],
            request_for_bid=row[16],submission_instructions=row[17],
            visit_worksite=row[18],visit_worksite_instructions=row[19],tech_clarification_deadline=row[20],
            com_clarification_deadline=row[21],expected_award_date=row[22],enduser_id=row[23],enduser_type=row[24],
            # end rfx
            opportunity_title=row[30],opportunity_type=row[31],probability=row[32],total_value=row[33],
            end_user_name=row[34],region=row[35],industry_code=row[36],business_unit=row[37],project_type=row[38],
            delivery_duration=row[39],opportunity_stage=row[40],opportunity_status=row[41],expected_rfx_date=row[42],
            close_date=row[43],competition=row[44],gross_profit_percent=row[45],gross_profit_value=row[46],
            opportunity_description=row[47],opportunity_last_updated_at=row[48],forcasted=row[49],            
            # end opportunity
            customer_id=row[50],customer_name=row[51],customer_email=row[52],customer_phone=row[53],
            customer_address=row[54],
            # end customer
            company_id=row[55],company_name=row[56],company_email=row[57],company_phone=row[58],
            company_website=row[59],company_logo=row[60],
            # end company
            acknowledged_by=row[61],acknowledgement_date=row[62],acknowledgement_comment=row[63],
            acknowledged=row[64],acknowledgement_document=row[65],acknowledgement_submitted_on=row[66],
            # end acknowledgement
            initiator_first_name=row[67],initiator_middle_name=row[68],initiator_last_name=row[69],
            initiator_email=row[70],initiator_role=row[71],initiator_role_level=row[72],initiator_team_id=row[73],
            # end initiator
            rfx_type=row[74] or "",bid_validity=row[75] or "",submission_content=row[76] or "",
            submission_mode=row[77] or "", rfx_stage_title=row[78] or "",            
            # end rfx prerequesites
            rfx_type_id=row[25], bid_validity_id=row[26], rfx_content_submission_id=row[27],
            rfx_submission_mode_id=row[28], rfx_stage_id=row[29]    
            # end rfx prerequesites id  
        ) 
        for row in rfxs
    ]
    