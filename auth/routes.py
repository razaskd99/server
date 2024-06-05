from fastapi import APIRouter, Depends, HTTPException
from auth.services import get_current_user, create_user, authenticate_user, authenticate_user2, create_access_token, delete_all_users, get_users_by_id
from auth.schemas import UserIn, UserOut, UserUpdateLimited, UserUpdateBio, UserUpdateTags

from fastapi.security import OAuth2PasswordRequestForm
from auth.services import authenticate_user, create_access_token, get_all_users, delete_user, update_user, update_user_limited, update_user_bio, update_user_tags
from pydantic.dataclasses import dataclass
from fastapi import Form
from typing import List
from typing import Optional

router = APIRouter()



@router.post("/signup", response_model=UserOut, tags=["auth"] )
async def signup(user_data: UserIn):
    return create_user(user_data)

@router.post("/login", tags=["auth"])
async def login_user(tenant_id: int, email: str, password: str):
    return authenticate_user(tenant_id, email, password)


@router.post("/token", tags=["auth"])
async def login_for_access_token(tenant_id: Optional[int] = None, form_data: OAuth2PasswordRequestForm = Depends()):

    if tenant_id is None:
            tenant_id = -1

    if tenant_id is not None and tenant_id != -1:
        user = authenticate_user(tenant_id, form_data.username, form_data.password)
        if not user or 'email' not in user:  # Check if 'email' exists in the user data
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = create_access_token(data={"sub": user["email"],"user":user})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        user = authenticate_user2(form_data.username, form_data.password)
        if not user or 'email' not in user:  # Check if 'email' exists in the user data
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = create_access_token(data={"sub": user["email"],"user":user})
        return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/users/tenant/{tenant_id}",response_model=List[UserOut], tags=["Users"], summary="Get all users by tenant id.", description="This method will return users for a given tenant id.")
async def login(tenant_id: int, searchTerm: str, current_user: str = Depends(get_current_user)):
    users_list = get_all_users(tenant_id, searchTerm)
    if not users_list:
        raise HTTPException(status_code=404, detail="Users not found")
    return users_list

@router.put("/auth/users/id/{user_id}", response_model=UserOut, tags=["Users"], summary="Update user details", description="This method will update user details by user ID" )
async def update_user_api(user_id: int, user_data: UserIn,current_user: str = Depends(get_current_user) ):
    return update_user(user_id, user_data)
    
@router.put("/auth/users/limited/id/{user_id}", response_model=UserOut, tags=["Users"], summary="Update limited user details", description="This method will update user limited details by user ID" )
async def update_user_api(user_id: int, user_data: UserUpdateLimited,current_user: str = Depends(get_current_user) ):
    return update_user_limited(user_id, user_data)

@router.put("/auth/users/bio/id/{user_id}", response_model=UserOut, tags=["Users"], summary="Update limited user details", description="This method will update user limited details by user ID" )
async def update_user_bio_api(user_id: int, user_data: UserUpdateBio, current_user: str = Depends(get_current_user) ):
    return update_user_bio(user_id, user_data)

@router.put("/auth/users/tags/id/{user_id}", response_model=UserOut, tags=["Users"], summary="Update limited user details", description="This method will update user limited details by user ID" )
async def update_user_tags_api(user_id: int, user_data: UserUpdateTags, current_user: str = Depends(get_current_user) ):
    return update_user_tags(user_id, user_data)

@router.delete("/auth/users/id/{user_id}", tags=["Users"], summary="Delete user details by ID.", description="This method will delete user by the give user ID.")
async def delete_user_api(user_id: int,current_user: str = Depends(get_current_user)):
    deleted = delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.delete("/auth/users/all/tenant/{tenant_id}",tags=["Users"], summary="Delete all users.", description="This method will delete all users by tenant ID.")
async def delete_all_user_api(tenant_id: int,current_user: str = Depends(get_current_user)):
    deleted = delete_all_users(tenant_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Users deleted successfully"}

@router.get("/auth/users/id/{user_id}",response_model=UserOut, tags=["Users"], summary="Get all users by ID.", description="This method will return users for a given user ID.")
async def get_users_by_id_api(user_id: int,current_user: str = Depends(get_current_user)):
    return get_users_by_id(user_id)