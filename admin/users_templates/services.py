from typing import Optional, List
from fastapi import HTTPException
from db.connection import get_db_connection
from .schemas import TemplateCreate, Template
import psycopg2
from psycopg2 import errors as psycopg_errors
import json


def create_template(template_data: TemplateCreate, tenant_id: int) :
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO templates (
        name,
        content,
        tenant_id,
        template_category
    ) VALUES (%s, %s, %s, %s) RETURNING *;
    """

    values = (
        template_data.name,
        template_data.content,
        tenant_id,
        template_data.template_category,
    )

    try:
        cursor.execute(query, values)
        new_template = cursor.fetchone()
        conn.commit()
        conn.close()

        if new_template:
            
            return {"msg": "Template Created Sucessfully",
             "code": 201}

        else:
            custom_message = "Template name already exists"
            custom_code = 400
            error_response = {"msg": custom_message, "code": custom_code}
            return json.dumps(error_response)

    except psycopg_errors.UniqueViolation as e:
        # Catch psycopg2 UniqueViolation error
        custom_message = "Template name already exists"
        custom_code = 409
        error_response = {"msg": custom_message, "code": custom_code}
        return json.dumps(error_response)

    except psycopg2.Error as e:
        # Handle other psycopg2 errors
        error_message = f"Database error: {e}"
        error_code = 500
        error_response = {"msg": error_message, "code": error_code}
        return json.dumps(error_response)

    except Exception as e:
        # Handle any other unexpected errors
        error_message = f"Unexpected error: {e}"
        error_code = 500
        error_response = {"msg": error_message, "code": error_code}
        return json.dumps(error_response)



def get_all_templates(tenant_id: int) -> List[Template]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, name,  tenant_id, template_category FROM templates WHERE tenant_id = %s;
        """
    cursor.execute(query,(tenant_id,))
    templates = cursor.fetchall()
    
    conn.close()

    return [
        Template(
            id=row[0],
            name=row[1],
            content="",
            tenant_id=row[2],
            template_category=row[3],
        )
        for row in templates
    ]

def get_template_by_id(template_id: int, tenant_id: int) -> Optional[Template]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, name, content, tenant_id, template_category FROM templates WHERE id = %s AND tenant_id = %s;
        """
    cursor.execute(query, (template_id, tenant_id))
    template = cursor.fetchone()

    conn.close()

    if template:
        return Template(
            id=template[0],
            name=template[1],
            content=template[2],
            tenant_id=template[3],
            template_category=template[4],
        )
    else:
        return None

def delete_template(template_id: int, tenant_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM templates WHERE id = %s AND tenant_id = %s RETURNING id ;"
    cursor.execute(query, (template_id, tenant_id))
    deleted_template = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_template:
        return True
    else:
        return False

def get_template_content_by_name(template_name: str,tenent_id: int) -> Optional[str]:
    # Convert tenant_id to int
    
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT content FROM templates WHERE name = %s AND tenant_id = %s; 
        """

    cursor.execute(query, (template_name,tenent_id,))
    template = cursor.fetchone()

    conn.close()


    if template:

        return template[0]
    else:
        return None
    

def update_template_content_by_name(template_name: str, tenant_id: int, new_content):
    # Convert tenant_id to int
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        UPDATE templates SET content = %s WHERE name = %s AND tenant_id = %s RETURNING content;
    """

    cursor.execute(query, (new_content, template_name, tenant_id))
    updated_content = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_content:
        return updated_content[0]
    else:
        return None


def delete_template_by_name(template_name: str, tenant_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        DELETE FROM templates WHERE name = %s AND tenant_id = %s
        """

    cursor.execute(query, (template_name, tenant_id,))
    rows_deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return rows_deleted > 0
