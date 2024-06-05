from db.connection import get_db_connection
from auth.schemas import UserIn, UserOut, UserUpdateLimited, UserUpdateBio
from fastapi import HTTPException, Depends
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from typing import Optional, Union, List
from datetime import date, datetime

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 9000

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)

def create_user(user_data: UserIn):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(user_data.password)

    query = """
    INSERT INTO users (tenant_id, job_title, company_name, employee_number, user_name, email, password, password_salt, 
        first_name, middle_name, last_name, user_role, contact_number, profile_image, manager, functional_group, 
        time_zone, work_location, work_hours_start, work_hours_end, active, verified, registration_date, 
        last_login_at, updated_at, created_at, city, state, currency_code, security_code, address, bio, tags)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
    RETURNING user_id, tenant_id, job_title, company_name, employee_number, user_name, email,  
        first_name, middle_name, last_name, user_role, contact_number, profile_image, manager, functional_group, 
        time_zone, work_location, work_hours_start, work_hours_end, active, verified, registration_date, 
        last_login_at, updated_at, created_at, city, state, currency_code, address, bio, tags;
    """

    cursor.execute(query, (
        user_data.tenant_id, user_data.job_title, user_data.company_name, user_data.employee_number,
        user_data.user_name, user_data.email, hashed_password, user_data.password_salt, user_data.first_name,
        user_data.middle_name, user_data.last_name, user_data.user_role, user_data.contact_number,
        user_data.profile_image, user_data.manager, user_data.functional_group, user_data.time_zone,
        user_data.work_location, user_data.work_hours_start, user_data.work_hours_end, user_data.active, 
        user_data.verified, user_data.registration_date, user_data.last_login_at, user_data.updated_at, user_data.created_at, 
        user_data.city, user_data.state, user_data.currency_code, user_data.security_code, user_data.address, '', ''        
    ))

    user = cursor.fetchone()
    conn.commit()
    conn.close()

    if user:
        return UserOut(
            user_id=user[0],
            tenant_id=user[1],
            job_title=user[2],
            company_name=user[3],
            employee_number=user[4],
            user_name=user[5],
            email=user[6],
            first_name=user[7],
            middle_name=user[8],
            last_name=user[9],
            user_role=user[10],
            contact_number=user[11],
            profile_image=user[12],
            manager=user[13],
            functional_group=user[14],
            time_zone=user[15],
            work_location=user[16],
            work_hours_start=user[17],
            work_hours_end=user[18],            
            active=user[19],
            verified=user[20],
            registration_date=user[21],
            last_login_at=user[22],
            updated_at=user[23],
            created_at=user[24],
            # optional fields
            city=user[25],
            state=user[26],
            currency_code=user[27],
            address=user[28],
            bio=user[29],
            tags=user[30]            
        )
    else:
        raise HTTPException(status_code=500, detail="User creation failed")
    

def update_user(user_id: int, user_data: UserIn):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if user_data.password:
        hashed_password = hash_password(user_data.password)
        query = """
            UPDATE users SET 
                job_title = %s, company_name = %s, employee_number = %s, user_name = %s, email = %s, 
                password = %s, password_salt = %s, first_name = %s, middle_name = %s, last_name = %s, user_role = %s, 
                contact_number = %s, profile_image = %s, manager = %s, functional_group = %s, time_zone = %s, 
                work_location = %s, work_hours_start = %s, work_hours_end = %s, active = %s,  
                updated_at = %s, city = %s, state = %s, currency_code = %s, security_code = %s, address = %s     
            WHERE user_id = %s
            RETURNING user_id, tenant_id, job_title, company_name, employee_number, user_name, email,  
                first_name, middle_name, last_name, user_role, contact_number, profile_image, manager, functional_group, 
                time_zone, work_location, work_hours_start, work_hours_end, active, verified, registration_date, 
                last_login_at, updated_at, created_at, city, state, currency_code, address, bio, tags;
            """

        cursor.execute(query, (
            user_data.job_title, user_data.company_name, user_data.employee_number, user_data.user_name, user_data.email,  
            hashed_password, user_data.password_salt, user_data.first_name, user_data.middle_name, user_data.last_name, 
            user_data.user_role, user_data.contact_number, user_data.profile_image, user_data.manager,
            user_data.functional_group, user_data.time_zone, user_data.work_location,  user_data.work_hours_start,
            user_data.work_hours_end, user_data.active, user_data.updated_at,  user_data.city,
            user_data.state, user_data.currency_code, user_data.security_code, user_data.address,
            user_id
        ))
    else:
        query = """
            UPDATE users SET 
                job_title = %s, company_name = %s, employee_number = %s, user_name = %s, email = %s, 
                first_name = %s, middle_name = %s, last_name = %s, user_role = %s, 
                contact_number = %s, profile_image = %s, manager = %s, functional_group = %s, time_zone = %s, 
                work_location = %s, work_hours_start = %s, work_hours_end = %s, active = %s,  
                updated_at = %s, city = %s, state = %s, currency_code = %s, security_code = %s, address = %s    
            WHERE user_id = %s
            RETURNING user_id, tenant_id, job_title, company_name, employee_number, user_name, email,  
                first_name, middle_name, last_name, user_role, contact_number, profile_image, manager, functional_group, 
                time_zone, work_location, work_hours_start, work_hours_end, active, verified, registration_date, 
                last_login_at, updated_at, created_at, city, state, currency_code, address, bio, tags;
            """

        cursor.execute(query, (
            user_data.job_title, user_data.company_name, user_data.employee_number, user_data.user_name, user_data.email,  
            user_data.first_name, user_data.middle_name, user_data.last_name, 
            user_data.user_role, user_data.contact_number, user_data.profile_image, user_data.manager,
            user_data.functional_group, user_data.time_zone, user_data.work_location,  user_data.work_hours_start,
            user_data.work_hours_end, user_data.active, user_data.updated_at,  user_data.city,
            user_data.state, user_data.currency_code, user_data.security_code, user_data.address,
            user_id
        ))
    user = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if user:
        # Now, use the returned user data to create a UserOut object
        return UserOut(
            user_id=user[0],
            tenant_id=user[1],
            job_title=user[2],
            company_name=user[3],
            employee_number=user[4],
            user_name=user[5],
            email=user[6],
            first_name=user[7],
            middle_name=user[8],
            last_name=user[9],
            user_role=user[10],
            contact_number=user[11],
            profile_image=user[12],
            manager=user[13],
            functional_group=user[14],
            time_zone=user[15],
            work_location=user[16],
            work_hours_start=user[17],
            work_hours_end=user[18],            
            active=user[19],
            verified=user[20],
            registration_date=user[21],
            last_login_at=user[22],
            updated_at=user[23],
            created_at=user[24],
            # optional fields
            city=user[25],
            state=user[26],
            currency_code=user[27],
            address=user[28],
            bio=user[29],
            tags=user[30]
        )
    else:
        raise HTTPException(status_code=500, detail="User Updation failed")


def update_user_limited(user_id: int, user_data: UserUpdateLimited):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if user_data.password:
        hashed_password = hash_password(user_data.password)
        query = """
            UPDATE users SET                 
                password = %s, contact_number = %s, profile_image = %s, time_zone = %s, 
                work_location = %s, work_hours_start = %s, work_hours_end = %s, job_title = %s   
            WHERE user_id = %s
            RETURNING user_id, tenant_id, job_title, company_name, employee_number, user_name, email,  
                first_name, middle_name, last_name, user_role, contact_number, profile_image, manager, functional_group, 
                time_zone, work_location, work_hours_start, work_hours_end, active, verified, registration_date, 
                last_login_at, updated_at, created_at, city, state, currency_code, address, bio, tags;
            """

        cursor.execute(query, (
            hashed_password, user_data.contact_number, user_data.profile_image, user_data.time_zone, 
            user_data.work_location, user_data.work_hours_start, user_data.work_hours_end, user_data.job_title, 
            user_id
        ))
    else:
        query = """
            UPDATE users SET 
                contact_number = %s, profile_image = %s, time_zone = %s, 
                work_location = %s, work_hours_start = %s, work_hours_end = %s, job_title = %s   
            WHERE user_id = %s
            RETURNING user_id, tenant_id, job_title, company_name, employee_number, user_name, email,  
                first_name, middle_name, last_name, user_role, contact_number, profile_image, manager, functional_group, 
                time_zone, work_location, work_hours_start, work_hours_end, active, verified, registration_date, 
                last_login_at, updated_at, created_at, city, state, currency_code, address, bio, tags;
            """

        cursor.execute(query, (
            user_data.contact_number, user_data.profile_image, user_data.time_zone, 
            user_data.work_location, user_data.work_hours_start, user_data.work_hours_end, user_data.job_title,
            user_id
        ))
    user = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if user:
        # Now, use the returned user data to create a UserOut object
        return UserOut(
            user_id=user[0],
            tenant_id=user[1],
            job_title=user[2],
            company_name=user[3],
            employee_number=user[4],
            user_name=user[5],
            email=user[6],
            first_name=user[7],
            middle_name=user[8],
            last_name=user[9],
            user_role=user[10],
            contact_number=user[11],
            profile_image=user[12],
            manager=user[13],
            functional_group=user[14],
            time_zone=user[15],
            work_location=user[16],
            work_hours_start=user[17],
            work_hours_end=user[18],            
            active=user[19],
            verified=user[20],
            registration_date=user[21],
            last_login_at=user[22],
            updated_at=user[23],
            created_at=user[24],
            # optional fields
            city=user[25],
            state=user[26],
            currency_code=user[27],
            address=user[28],
            bio=user[29],
            tags=user[30]
        )
    else:
        raise HTTPException(status_code=500, detail="User Updation failed")

def update_user_bio(user_id: int, user_data: UserUpdateLimited):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        UPDATE users SET 
            bio = %s
        WHERE user_id = %s
        RETURNING user_id, tenant_id, job_title, company_name, employee_number, user_name, email,  
            first_name, middle_name, last_name, user_role, contact_number, profile_image, manager, functional_group, 
            time_zone, work_location, work_hours_start, work_hours_end, active, verified, registration_date, 
            last_login_at, updated_at, created_at, city, state, currency_code, address, bio, tags;
        """

    cursor.execute(query, (user_data.bio, user_id))
    user = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if user:
        # Now, use the returned user data to create a UserOut object
        return UserOut(
            user_id=user[0],
            tenant_id=user[1],
            job_title=user[2],
            company_name=user[3],
            employee_number=user[4],
            user_name=user[5],
            email=user[6],
            first_name=user[7],
            middle_name=user[8],
            last_name=user[9],
            user_role=user[10],
            contact_number=user[11],
            profile_image=user[12],
            manager=user[13],
            functional_group=user[14],
            time_zone=user[15],
            work_location=user[16],
            work_hours_start=user[17],
            work_hours_end=user[18],            
            active=user[19],
            verified=user[20],
            registration_date=user[21],
            last_login_at=user[22],
            updated_at=user[23],
            created_at=user[24],
            # optional fields
            city=user[25],
            state=user[26],
            currency_code=user[27],
            address=user[28],
            bio=user[29],
            tags=user[30]
        )
    else:
        raise HTTPException(status_code=500, detail="User Updation failed")

def update_user_tags(user_id: int, user_data: UserUpdateLimited):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        UPDATE users SET 
            tags = %s
        WHERE user_id = %s
        RETURNING user_id, tenant_id, job_title, company_name, employee_number, user_name, email,  
            first_name, middle_name, last_name, user_role, contact_number, profile_image, manager, functional_group, 
            time_zone, work_location, work_hours_start, work_hours_end, active, verified, registration_date, 
            last_login_at, updated_at, created_at, city, state, currency_code, address, bio, tags;
        """

    cursor.execute(query, (user_data.tags, user_id))
    user = cursor.fetchone()
    
    conn.commit()
    conn.close()

    if user:
        # Now, use the returned user data to create a UserOut object
        return UserOut(
            user_id=user[0],
            tenant_id=user[1],
            job_title=user[2],
            company_name=user[3],
            employee_number=user[4],
            user_name=user[5],
            email=user[6],
            first_name=user[7],
            middle_name=user[8],
            last_name=user[9],
            user_role=user[10],
            contact_number=user[11],
            profile_image=user[12],
            manager=user[13],
            functional_group=user[14],
            time_zone=user[15],
            work_location=user[16],
            work_hours_start=user[17],
            work_hours_end=user[18],            
            active=user[19],
            verified=user[20],
            registration_date=user[21],
            last_login_at=user[22],
            updated_at=user[23],
            created_at=user[24],
            # optional fields
            city=user[25],
            state=user[26],
            currency_code=user[27],
            address=user[28],
            bio=user[29],
            tags=user[30]
        )
    else:
        raise HTTPException(status_code=500, detail="User Updation failed")

def authenticate_user(tenant_id: int, email: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """SELECT 
            user_id, tenant_id, job_title, company_name, employee_number, user_name, email,  
            first_name, middle_name, last_name, user_role, contact_number, profile_image, manager, functional_group, 
            time_zone, work_location, work_hours_start, work_hours_end, active, verified, registration_date, 
            last_login_at, updated_at, created_at, city, state, currency_code, address, password
        FROM users WHERE email = %s AND tenant_id = %s ;
        """
    cursor.execute(query, (email, tenant_id))
    user_data = cursor.fetchone()

    conn.close()

    if user_data and verify_password(password, user_data[29]):
        # Fetching all user details from the database
        user_dict = {
            "user_id":  user_data[0],
            "tenant_id":  user_data[1],
            "job_title":  user_data[2],
            "company_name":  user_data[3],
            "employee_number":  user_data[4],
            "user_name":  user_data[5],
            "email":  user_data[6],
            "first_name":  user_data[7],
            "middle_name":  user_data[8],
            "last_name":  user_data[9],
            "user_role":  user_data[10],
            "contact_number":  user_data[11],
            "profile_image":  user_data[12],
            "manager":  user_data[13],
            "functional_group":  user_data[14],
            "time_zone":  user_data[15],
            "work_location":  user_data[16],
            "work_hours_start":  user_data[17],
            "work_hours_end":  user_data[18],            
            "active":  user_data[19],
            "verified":  user_data[20],
            "city":  user_data[25],
            "state":  user_data[26],
            "currency_code":  user_data[27],
            "address":  user_data[28],
            "password": user_data[29]
        }

        # Set the access_token_expires correctly
        access_token_expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        # Include additional fields in the payload
        payload = {
            **user_dict,
            "sub": email,
            "exp": access_token_expires,
        }

        # Create the access token by encoding the payload
        access_token = create_access_token(payload)

        return {
            "email": email,
            "access_token": access_token,
            **user_dict
        }

    return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user2( email: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """SELECT 
            user_id, tenant_id, job_title, company_name, employee_number, user_name, email,  
            first_name, middle_name, last_name, user_role, contact_number, profile_image, manager, functional_group, 
            time_zone, work_location, work_hours_start, work_hours_end, active, verified, registration_date, 
            last_login_at, updated_at, created_at, city, state, currency_code, address, password
        FROM users WHERE email = %s;
        """
    cursor.execute(query, (email, ))
    user_data = cursor.fetchone()

    conn.close()

    if user_data and verify_password(password, user_data[29]):
        # Fetching all user details from the database
        user_dict = {
            "user_id":  user_data[0],
            "tenant_id":  user_data[1],
            "job_title":  user_data[2],
            "company_name":  user_data[3],
            "employee_number":  user_data[4],
            "user_name":  user_data[5],
            "email":  user_data[6],
            "first_name":  user_data[7],
            "middle_name":  user_data[8],
            "last_name":  user_data[9],
            "user_role":  user_data[10],
            "contact_number":  user_data[11],
            "profile_image":  user_data[12],
            "manager":  user_data[13],
            "functional_group":  user_data[14],
            "time_zone":  user_data[15],
            "work_location":  user_data[16],
            "work_hours_start":  user_data[17],
            "work_hours_end":  user_data[18],            
            "active":  user_data[19],
            "verified":  user_data[20],           
            "city":  user_data[25],
            "state":  user_data[26],
            "currency_code":  user_data[27],
            "address":  user_data[28],
            "password":  user_data[29]
        }

        # Set the access_token_expires correctly
        access_token_expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        # Include additional fields in the payload
        payload = {
            **user_dict,
            "sub": email,
            "exp": access_token_expires,
        }

        # Create the access token by encoding the payload
        access_token = create_access_token(payload)

        return {
            "email": email,
            "access_token": access_token,
            **user_dict
        }

    return None

def get_all_users( tenant_id: int, searchTerm: str) -> List[UserOut]:
    conn = get_db_connection()
    cursor = conn.cursor()

    if searchTerm:
        #searchTerm = searchTerm.replace("-", " ")
        searchTerm = '%' + searchTerm.lower() + '%'
        query = """
            SELECT 
                user_id, tenant_id, job_title, company_name, employee_number, user_name, email,  
                first_name, middle_name, last_name, user_role, contact_number, profile_image, manager, functional_group, 
                time_zone, work_location, work_hours_start, work_hours_end, active, verified, registration_date, 
                last_login_at, updated_at, created_at, city, state, currency_code, address, bio, tags
            FROM users WHERE tenant_id = %s AND (CONCAT(lower(first_name),' ', lower(last_name)) LIKE %s OR lower(first_name) LIKE %s OR lower(last_name) LIKE %s)
            ORDER BY created_at DESC;
            """
        cursor.execute(query, (tenant_id, searchTerm, searchTerm, searchTerm))
        user_data = cursor.fetchall()
    else:
        query = """
            SELECT 
                user_id, tenant_id, job_title, company_name, employee_number, user_name, email,  
                first_name, middle_name, last_name, user_role, contact_number, profile_image, manager, functional_group, 
                time_zone, work_location, work_hours_start, work_hours_end, active, verified, registration_date, 
                last_login_at, updated_at, created_at, city, state, currency_code, address, bio, tags
            FROM users WHERE tenant_id = %s
            ORDER BY created_at DESC;
            """
        cursor.execute(query, (tenant_id, ))
        user_data = cursor.fetchall()
        
    conn.close()

    if user_data:
        pass
        
    else:
        user_data=[] 
           
    return [
        UserOut(
            user_id=row[0],
            tenant_id=row[1],
            job_title=row[2],
            company_name=row[3],
            employee_number=row[4],
            user_name=row[5],
            email=row[6],
            first_name=row[7],
            middle_name=row[8],
            last_name=row[9],
            user_role=row[10],
            contact_number=row[11],
            profile_image=row[12],
            manager=row[13],
            functional_group=row[14],
            time_zone=row[15],
            work_location=row[16],
            work_hours_start=row[17],
            work_hours_end=row[18],            
            active=row[19],
            verified=row[20],
            registration_date=row[21],
            last_login_at=row[22],
            updated_at=row[23],
            created_at=row[24],
            # optional fields
            city=row[25],
            state=row[26],
            currency_code=row[27],
            address=row[28],
            bio=row[29],
            tags=row[30]
            
        )
        for row in user_data
    ]


def delete_user(user_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "DELETE FROM users WHERE user_id = %s RETURNING user_id;"

    cursor.execute(query, (user_id,))

    deleted_user = cursor.fetchone()

    conn.commit()
    conn.close()
    
    if deleted_user:
        return True
    else:
        return False

def delete_all_users(tenant_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()  
    
    query = "DELETE FROM users WHERE tenant_id = %s AND user_role != %s RETURNING user_id;"

    cursor.execute(query, (tenant_id, "super admin"))

    deleted_user = cursor.fetchone()

    conn.commit()
    conn.close()
    
    if deleted_user:
        return True
    else:
        return False
    
def get_users_by_id( user_id: int) -> Optional[UserOut]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
	        user_id, tenant_id, job_title, company_name, employee_number, user_name, email,  
            first_name, middle_name, last_name, user_role, contact_number, profile_image, manager, functional_group, 
            time_zone, work_location, work_hours_start, work_hours_end, active, verified, registration_date, 
            last_login_at, updated_at, created_at, city, state, currency_code, address, bio, tags
        FROM users WHERE user_id = %s;
        """
    cursor.execute(query, (user_id, ))
    user = cursor.fetchone()
    
    conn.close()

    if user:    
        return UserOut(
                user_id=user[0],
                tenant_id=user[1],
                job_title=user[2],
                company_name=user[3],
                employee_number=user[4],
                user_name=user[5],
                email=user[6],
                first_name=user[7],
                middle_name=user[8],
                last_name=user[9],
                user_role=user[10],
                contact_number=user[11],
                profile_image=user[12],
                manager=user[13],
                functional_group=user[14],
                time_zone=user[15],
                work_location=user[16],
                work_hours_start=user[17],
                work_hours_end=user[18],            
                active=user[19],
                verified=user[20],
                registration_date=user[21],
                last_login_at=user[22],
                updated_at=user[23],
                created_at=user[24],
                # optional fields
                city=user[25],
                state=user[26],
                currency_code=user[27],
                address=user[28],
                bio=user[29],
                tags=user[30]
            )
       



