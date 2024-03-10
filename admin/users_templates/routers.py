from fastapi import APIRouter, HTTPException,Response
from typing import List
from . import schemas, services
import json

router = APIRouter()

@router.post("/templates",  tags=["Templates"], summary="Create a Template", description="Create a new template and store its name and content in the PostgreSQL database")
async def add_template(template_data: schemas.TemplateCreate, tenant_id: int):
    return services.create_template(template_data, tenant_id)

@router.get("/templates", response_model=List[schemas.Template], tags=["Templates"], summary="Get All Templates", description="Retrieve all templates for the given tenant from the PostgreSQL database")
async def get_all_templates(tenant_id: int):
    return services.get_all_templates(tenant_id)

@router.get("/templates/{template_id}", response_model=schemas.Template, tags=["Templates"], summary="Get Template by ID", description="Retrieve a template by its ID from the PostgreSQL database")
async def get_template_by_id(template_id: int, tenant_id: int):
    template = services.get_template_by_id(template_id, tenant_id)
    if template is None:
        raise HTTPException(status_code=404, detail=f"Template with id {template_id} not found for tenant {tenant_id}")
    return template

@router.delete("/templates/{template_id}", tags=["Templates"], summary="Delete Template by ID", description="Delete a template by its ID from the PostgreSQL database")
async def delete_template(template_id: int, tenant_id: int):
    deleted = services.delete_template(template_id, tenant_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Template with id {template_id} not found for tenant {tenant_id}")
    return {"message": "Template deleted successfully"}


@router.get("/templates/{template_name}/content/load", tags=["Templates"], summary="Get Template Content by Name", description="Retrieve the content of a template by its name from the PostgreSQL database")
async def get_template_content_by_name(template_name,tenant_id):
    content = services.get_template_content_by_name(template_name,tenant_id)
    if content :
        # Remove the surrounding single quotes
        json_string = content.strip('\'')
        # Convert escaped double quotes back to regular double quotes
        json_string = json_string.replace(r'\"', '"')

        # Load the JSON string to get the JSON object
        json_object = json.loads(json_string)


        return json_object
    else:
        return {}



@router.post("/templates/{template_name}/content/save", tags=["Templates"], summary="Get Template Content by Name", description="Retrieve the content of a template by its name from the PostgreSQL database")
async def post_template_content_by_name(template_name,tenant_id,request_body: dict):
    
    # Convert the dictionary to a JSON-formatted string
    json_string = json.dumps(request_body)

    # Convert double quotes in the JSON string to escaped double quotes
    json_string = json_string.replace('"', r'\"')

    # Construct the final string representation
    final_string = f'\'{json_string}\''

    content = services.update_template_content_by_name(template_name, tenant_id,final_string)
    
    if content:
        json_string = content.strip("'")

        # Use json.loads() to convert the JSON string back into a dictionary
        data_dict = json.loads(json_string)

        return data_dict
    else:
        return None
    

@router.delete("/templates/{template_name}/content/delete", tags=["Templates"], summary="Delete Template by Name", description="Delete a template by its name from the PostgreSQL database")
async def delete_template_by_name(template_name: str, tenant_id: int):
    deleted = services.delete_template_by_name(template_name, tenant_id)
    if deleted:
        return {"message": f"Template '{template_name}' deleted successfully"}
    else:
        return {"message": f"Template '{template_name}' Could not be deleted!"}
