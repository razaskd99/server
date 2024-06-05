from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from auth.services import   authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from admin.control_panel.routes import router as control_panel_router

 

# from admin.designation.routers import router as designation_router
# from admin.company.routers import router as company_router
# from admin.team.routers import router as team_router
# from admin.customer.routers import router as customer_router

from auth.routes import router as auth_router 
from mailer.routes import router as mailer_router

from contacts_team.routes import router as contacts_team_router
from persona.routes import router as persona_router
from functional_group.routes import router as functional_group_router

from account.routes import router as account_router
from account_type.routes import router as account_type_router
from account_type_entries.routes import router as account_type_entries_router

from opportunity.routes import router as opportunity_router
from opportunity_sales_stages.routes import router as opportunity_sales_stages_router
from sales_pursuit_progress.routes import router as sales_pursuit_progress_router
from business_line.routes import router as business_line_router
from opp_committed_for_sales_budget.routes import router as opp_committed_for_sales_budget_router
from bidding_unit.routes import router as bidding_unit_router
from project_type.routes import router as project_type_router
from opportunity_type.routes import router as opportunity_type_router



from docvalt.routes import router as docvalt_router

from bid_validity.routes import router as bid_validity_router
from rfx_type.routes import router as rfx_type_router
from rfx_content_submission.routes import router as rfx_content_submission_router
from rfx_submission_mode.routes import router as rfx_submission_mode_router
from rfx_stage.routes import router as rfx_stage_router


from rfx.routes import router as rfx_router

from rfx_detail.routes import router as rfx_detail_router


#from rfx_phase_stage.routes import router as rfx_phase_stage_router
#from rfx_phase_stage_detail.routes import router as rfx_phase_stage_detail_stage_router

#from bid_stage.routes import router as bid_stage_router
#from bid_stage_detail.routes import router as bid_stage_detail_stage_router

from rfx_clarification.routes import router as rfx_clarification_router
from rfx_clarification_post.routes import router as rfx_clarification_post_router
from rfx_clarification_meta.routes import router as rfx_clarification_meta_router
from bid_documents.routes import router as bid_documents_router


from bid_documents_post.routes import router as bid_documents_post_router
from bid_documents_meta.routes import router as bid_documents_meta_router
from bid_clarification.routes import router as bid_clarification_router
from bid_clarification_post.routes import router as bid_clarification_post_router

from bid_clarification_meta.routes import router as bid_clarification_meta_router
from bid_clarification_revision.routes import router as bid_clarification_revision_router
from bid_clarification_revision_line.routes import router as bid_clarification_revision_line_router
from bid_clarification_revision_meta.routes import router as bid_clarification_revision_meta_router
from bid_order.routes import router as bid_order_router
from bid_order_post.routes import router as bid_order_post_router
from bid_order_meta.routes import router as bid_order_meta_router
from contacts.routes import router as contacts_router
from phase_stages.routes import router as phase_stages_router
from phase_stages_detail.routes import router as phase_stages_detail_router


from bid_review.routes import router as bid_review_router
from bid_review_contacts.routes import router as bid_review_contacts_router
from bid_review_post.routes import router as bid_review_post_router
from bid_review_templates.routes import router as bid_review_templates_router
from bid_submission.routes import router as bid_submission_router
from bid_submission_acknowledgement.routes import router as bid_submission_acknowledgement_router
from bid_submission_post.routes import router as bid_submission_post_router

from review_templates.routes import router as review_templates_router

from bid_deliverables.routes import router as bid_deliverables_router
from bid_kickoff_meeting.routes import router as bid_kickoff_meeting_router

from bid_team.routes import router as bidteam_router


from fastapi.responses import RedirectResponse
from core.config import settings
from uploads.routes import router as uploads_router

from admin.users_templates.routers import router as users_template_routers
import os


app = FastAPI(
    debug=True,
    title=settings.PROJECT_NAME, 
    version=settings.PROJECT_VERSION,
    summary="The APIs designed for BIDSFORCE, an innovative bid management platform. These APIs cover authentication, CRUD operations, and management functionalities, aiming to streamline bid planning, workflow automation, and resource allocation.",
    description="A comprehensive set of APIs catering to BIDSFORCE, revolutionizing bid management practices. Spanning authentication with OAuth2 and JWT tokenization, CRUD operations for designations, companies, teams, customers, and DocValt, these APIs ensure secure, efficient, and organized bid processes. They encompass Opportunity and RFX management, bid lifecycle handling, resource allocation, and administrative control through a Control Panel. With detailed endpoint information and usage instructions, these APIs aim to enhance collaboration and deliver an intuitive user experience within the BIDSFORCE platform.",
    root_path_in_servers=True,
    include_in_schema=True,
    separate_input_output_schemas=True,
    )


origins = [
    "https://bidsforce-client-phi.vercel.app",
    "http://localhost:3000",
        "http://127.0.0.1:3000",

    
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def check_server():
    return {"message": os.environ}

app.include_router(auth_router, prefix="/auth")
app.include_router(mailer_router, prefix="/mailer")


app.include_router(contacts_team_router, prefix="/contacts_team")
app.include_router(persona_router, prefix="/persona")
app.include_router(functional_group_router, prefix="/functional_group")

# app.include_router(designation_router, prefix="/designation")
# app.include_router(company_router, prefix="/company")
# app.include_router(team_router, prefix="/team")
# app.include_router(customer_router, prefix="/customer")

app.include_router(account_router, prefix="/account")
app.include_router(account_type_router, prefix="/account_type")
app.include_router(account_type_entries_router, prefix="/account_type_entries")

app.include_router(opportunity_router, prefix="/opportunity")
app.include_router(opportunity_sales_stages_router, prefix="/opportunity_sales_stages")
app.include_router(sales_pursuit_progress_router, prefix="/sales_pursuit_progress")
app.include_router(business_line_router, prefix="/business_line")
app.include_router(opp_committed_for_sales_budget_router, prefix="/opp_committed_for_sales_budget")
app.include_router(bidding_unit_router, prefix="/bidding_unit")
app.include_router(project_type_router, prefix="/project_type")
app.include_router(opportunity_type_router, prefix="/opportunity_type")


app.include_router(docvalt_router, prefix="/docvalt")


app.include_router(bid_validity_router, prefix="/bid_validity")
app.include_router(rfx_type_router, prefix="/rfx_type")
app.include_router(rfx_content_submission_router, prefix="/rfx_content_submission")
app.include_router(rfx_submission_mode_router, prefix="/rfx_submission_mode")
app.include_router(rfx_stage_router, prefix="/rfx_stage")

app.include_router(rfx_router, prefix="/rfx")
app.include_router(rfx_detail_router, prefix="/rfx_detail")


#app.include_router(rfx_phase_stage_router, prefix="/rfx_phase_stage")
#app.include_router(rfx_phase_stage_detail_stage_router, prefix="/rfx_phase_stage_detail_stage")

#app.include_router(bid_stage_router, prefix="/bid_stage")
#app.include_router(bid_stage_detail_stage_router, prefix="/bid_stage_detail_stage")

app.include_router(rfx_clarification_router, prefix="/rfx_clarification")
app.include_router(rfx_clarification_post_router, prefix="/rfx_clarification_post")
app.include_router(rfx_clarification_meta_router, prefix="/rfx_clarification_meta")
app.include_router(bid_documents_router, prefix="/bid_documents")
app.include_router(bid_documents_post_router, prefix="/bid_documents_post")
app.include_router(bid_documents_meta_router, prefix="/bid_documents_meta")
app.include_router(bid_clarification_router, prefix="/bid_clarification")
app.include_router(bid_clarification_post_router, prefix="/bid_clarification_post")
app.include_router(bid_clarification_meta_router, prefix="/bid_clarification_meta")
app.include_router(bid_clarification_revision_router, prefix="/bid_clarification_revision")
app.include_router(bid_clarification_revision_line_router, prefix="/bid_clarification_revision_line")
app.include_router(bid_clarification_revision_meta_router, prefix="/bid_clarification_revision_meta")
app.include_router(bid_order_router, prefix="/bid_order")
app.include_router(bid_order_post_router, prefix="/bid_order_post")
app.include_router(bid_order_meta_router, prefix="/bid_order_meta")
app.include_router(contacts_router, prefix="/contacts")
app.include_router(phase_stages_router, prefix="/phase_stage")
app.include_router(phase_stages_detail_router, prefix="/phase_stages_detail")


app.include_router(bid_review_router, prefix="/bid_review")
app.include_router(bid_review_contacts_router, prefix="/bid_review_contacts")
app.include_router(bid_review_post_router, prefix="/bid_review_post")
app.include_router(bid_review_templates_router, prefix="/bid_review_templates")
app.include_router(bid_submission_router, prefix="/bid_submissions")
app.include_router(bid_submission_acknowledgement_router, prefix="/bid_submission_acknowledgement")
app.include_router(bid_submission_post_router, prefix="/bid_submission_posts")

app.include_router(review_templates_router, prefix="/review_template")

app.include_router(bid_deliverables_router, prefix="/bid_deliverables")
app.include_router(bid_kickoff_meeting_router, prefix="/bid_kickoff_meeting")
app.include_router(bidteam_router, prefix="/bid_teams")



app.include_router(control_panel_router, prefix="/admin/control-panel") 
app.include_router(uploads_router, prefix="/uploads")

app.include_router(users_template_routers, prefix="/templates")

