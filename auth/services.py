from db.connection import get_db_connection
from auth.schemas import UserIn, UserOut, GetUsers
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
ACCESS_TOKEN_EXPIRE_MINUTES = 90

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
    INSERT INTO users (tenant_id, team_id, designation_id, company_id, user_name, email, password, first_name,
    middle_name, last_name, user_role, role_level, registration_date, last_login_at, created_at, updated_at, active, verified, password_salt, user_profile_photo)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
    RETURNING user_id, tenant_id, team_id, designation_id, company_id, user_name, email, password, first_name,
    middle_name, last_name, user_role, role_level, registration_date, last_login_at, created_at, updated_at, active, verified, password_salt, user_profile_photo;
    """

    cursor.execute(query, (
        user_data.tenant_id, user_data.team_id, user_data.designation_id, user_data.company_id,
        user_data.user_name, user_data.email, hashed_password, user_data.first_name,
        user_data.middle_name, user_data.last_name, user_data.user_role, user_data.role_level,
        user_data.registration_date, user_data.last_login_at, user_data.created_at, user_data.updated_at,
        user_data.active, user_data.verified, user_data.password_salt, user_data.user_profile_photo
    ))

    user = cursor.fetchone()

    conn.commit()
    conn.close()

    if user:
        # Now, use the returned user data to create a UserOut object
        return UserOut(
            user_id=user[0],
            tenant_id=user[1],
            team_id=user[2],
            designation_id=user[3],
            company_id=user[4],
            user_name=user[5],
            email=user[6],
            first_name=user[8],
            middle_name=user[9],
            last_name=user[10],
            user_role=user[11],
            role_level=user[12],
            registration_date=user[13],
            last_login_at=user[14],
            created_at=user[15],
            updated_at=user[16],
            active=user[17],
            verified=user[18],
            user_profile_photo=user[19]
        )
    else:
        raise HTTPException(status_code=500, detail="User creation failed")
    

def update_user(user_id: int, user_data: UserIn):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(user_data.password)
    
    if user_data.password:
        query = """
            UPDATE users SET 
                team_id = %s, designation_id = %s, company_id = %s, password = %s, first_name = %s, middle_name = %s,
                last_name = %s, user_role = %s, role_level = %s, updated_at = %s, password_salt = %s,
                user_profile_photo = %s      
            WHERE user_id = %s
            RETURNING user_id, tenant_id, team_id, designation_id, company_id, user_name, email, password, first_name,
            middle_name, last_name, user_role, role_level, registration_date, last_login_at, created_at, updated_at, active, verified, password_salt, user_profile_photo;
            """

        cursor.execute(query, (
            user_data.team_id, user_data.designation_id, user_data.company_id, hashed_password, user_data.first_name,
            user_data.middle_name, user_data.last_name, user_data.user_role, user_data.role_level, user_data.updated_at,
            user_data.password_salt, user_data.user_profile_photo,
            user_id
        ))
    else:
        query = """
            UPDATE users SET 
                team_id = %s, designation_id = %s, company_id = %s, first_name = %s, middle_name = %s,
                last_name = %s, user_role = %s, role_level = %s, updated_at = %s, password_salt = %s,
                user_profile_photo = %s      
            WHERE user_id = %s
            RETURNING user_id, tenant_id, team_id, designation_id, company_id, user_name, email, password, first_name,
            middle_name, last_name, user_role, role_level, registration_date, last_login_at, created_at, updated_at, active, verified, password_salt, user_profile_photo;
            """

        cursor.execute(query, (
            user_data.team_id, user_data.designation_id, user_data.company_id, user_data.first_name,
            user_data.middle_name, user_data.last_name, user_data.user_role, user_data.role_level, user_data.updated_at,
            user_data.password_salt, user_data.user_profile_photo,
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
            team_id=user[2],
            designation_id=user[3],
            company_id=user[4],
            user_name=user[5],
            email=user[6],
            first_name=user[8],
            middle_name=user[9],
            last_name=user[10],
            user_role=user[11],
            role_level=user[12],
            registration_date=user[13],
            last_login_at=user[14],
            created_at=user[15],
            updated_at=user[16],
            active=user[17],
            verified=user[18],
            user_profile_photo=user[19]
        )
    else:
        raise HTTPException(status_code=500, detail="User Updation failed")


def authenticate_user(tenant_id: int, email: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT user_id,tenant_id,team_id,designation_id,company_id,user_name,email,password,first_name,middle_name,last_name,user_role,role_level,registration_date,last_login_at,created_at,updated_at,active,verified,user_profile_photo FROM users WHERE email = %s AND tenant_id = %s ;"
    cursor.execute(query, (email, tenant_id))
    user_data = cursor.fetchone()

    conn.close()

    if user_data and verify_password(password, user_data[7]):
        # Fetching all user details from the database
        user_dict = {
            "user_id": user_data[0],
            "tenant_id": user_data[1],
            "team_id": user_data[2],
            "designation_id": user_data[3],
            "company_id": user_data[4],
            "user_name": user_data[5],
            "email": user_data[6],
            "first_name": user_data[8],
            "middle_name": user_data[9],
            "last_name": user_data[10],
            "user_role": user_data[11],
            "role_level": user_data[12],
            "registration_date": user_data[13].isoformat() if user_data[13] else None,
            "last_login_at": user_data[14].isoformat() if user_data[14] else None,
            "created_at": user_data[15].isoformat() if user_data[15] else None,
            "updated_at": user_data[16].isoformat() if user_data[16] else None,
            "active": user_data[17],
            "verified": user_data[18],
            "user_profile_photo": user_data[19]
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

    query = "SELECT user_id,tenant_id,team_id,designation_id,company_id,user_name,email,password,first_name,middle_name,last_name,user_role,role_level,registration_date,last_login_at,created_at,updated_at,active,verified, user_profile_photo FROM users WHERE email = %s;"
    cursor.execute(query, (email, ))
    user_data = cursor.fetchone()

    conn.close()

    if user_data and verify_password(password, user_data[7]):
        # Fetching all user details from the database
        user_dict = {
            "user_id": user_data[0],
            "tenant_id": user_data[1],
            "team_id": user_data[2],
            "designation_id": user_data[3],
            "company_id": user_data[4],
            "user_name": user_data[5],
            "email": user_data[6],
            "first_name": user_data[8],
            "middle_name": user_data[9],
            "last_name": user_data[10],
            "user_role": user_data[11],
            "role_level": user_data[12],
            "registration_date": user_data[13].isoformat() if user_data[13] else None,
            "last_login_at": user_data[14].isoformat() if user_data[14] else None,
            "created_at": user_data[15].isoformat() if user_data[15] else None,
            "updated_at": user_data[16].isoformat() if user_data[16] else None,
            "active": user_data[17],
            "verified": user_data[18],
            "user_profile_photo": user_data[19]
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

def get_all_users( tenant_id: int) -> List[GetUsers]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT u.*,
	        t.team_title, team_role,
	        d.title AS designation_title, d.type AS designation_type,
	        c.company_name
        FROM users u
        LEFT JOIN team t ON t.team_id=u.user_id
        INNER JOIN designation d ON d.designation_id=u.designation_id
        LEFT JOIN company c ON c.company_id=u.company_id
        WHERE u.tenant_id = %s;
        """
    cursor.execute(query, (tenant_id, ))
    user_data = cursor.fetchall()

    conn.close()

    if user_data:
        pass
        
    else:
        user_data=[] 
           
    return [
        GetUsers(
            user_id = row[0],
            tenant_id= row[1],
            team_id = row[2],
            designation_id= row[3],
            company_id= row[4],
            user_name= row[5],
            email= row[6],
            first_name= row[8],
            middle_name= row[9],
            last_name= row[10],
            user_role= row[11],
            role_level= row[12],
            registration_date= row[13],
            last_login_at= row[14],
            created_on= row[15] or datetime(1970, 1, 1),
            created_at= row[16],
            updated_at= row[17],
            active= row[18],
            verified= row[19],
            user_profile_photo= row[21],
            team_title= row[22] or '',
            team_role= row[23] or '',
            designation_title= row[24],
            designation_type= row[25],
            company_name= row[26]
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
    
def get_users_by_id( user_id: int) -> Optional[GetUsers]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT u.*,
	        t.team_title, team_role,
	        d.title AS designation_title, d.type AS designation_type,
	        c.company_name
        FROM users u
        LEFT JOIN team t ON t.team_id=u.user_id
        INNER JOIN designation d ON d.designation_id=u.designation_id
        LEFT JOIN company c ON c.company_id=u.company_id
        WHERE u.user_id = %s;
        """
    cursor.execute(query, (user_id, ))
    user_data = cursor.fetchone()
    
    conn.close()

    if user_data:    
        return GetUsers(
                user_id = user_data[0],
                tenant_id= user_data[1],
                team_id = user_data[2],
                designation_id= user_data[3],
                company_id= user_data[4],
                user_name= user_data[5],
                email= user_data[6],
                first_name= user_data[8],
                middle_name= user_data[9],
                last_name= user_data[10],
                user_role= user_data[11],
                role_level= user_data[12],
                registration_date= user_data[13],
                last_login_at= user_data[14],
                created_on= user_data[15] or datetime(1970, 1, 1),
                created_at= user_data[16],
                updated_at= user_data[17],
                active= user_data[18],
                verified= user_data[19],
                user_profile_photo= user_data[21],
                team_title= user_data[22] or '',
                team_role= user_data[23] or '',
                designation_title= user_data[24],
                designation_type= user_data[25],
                company_name= user_data[26]
            )
       



