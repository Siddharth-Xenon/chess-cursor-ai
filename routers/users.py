from fastapi import APIRouter, Body, Depends, HTTPException
from models.user import UserCreate, UserDisplay, UserUpdate
from auth.firebase_auth import (
    create_user,
    get_user,
    update_user,
    delete_user,
    verify_id_token,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
auth_scheme = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    try:
        payload = verify_id_token(token)
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/users/", response_description="Add new user", response_model=UserDisplay)
async def create_user_route(user: UserCreate = Body(...)):
    firebase_user = create_user(
        email=user.email, password=user.password, username=user.username
    )
    if firebase_user:
        return UserDisplay(username=user.username, email=user.email)
    raise HTTPException(status_code=400, detail="Error creating user")


@router.get(
    "/users/{uid}", response_description="Get a user", response_model=UserDisplay
)
async def get_user_route(uid: str, current_user: dict = Depends(get_current_user)):
    firebase_user = get_user(uid)
    if firebase_user:
        return UserDisplay(
            id=uid, username=firebase_user.display_name, email=firebase_user.email
        )
    raise HTTPException(status_code=404, detail="User not found")


@router.put(
    "/users/{uid}", response_description="Update a user", response_model=UserDisplay
)
async def update_user_route(
    uid: str,
    user: UserUpdate = Body(...),
    current_user: dict = Depends(get_current_user),
):
    firebase_user = update_user(
        uid=uid, email=user.email, password=None, username=user.username
    )
    if firebase_user:
        return UserDisplay(
            id=uid, username=firebase_user.display_name, email=firebase_user.email
        )
    raise HTTPException(status_code=400, detail="Error updating user")


@router.delete("/users/{uid}", response_description="Delete a user")
async def delete_user_route(uid: str, current_user: dict = Depends(get_current_user)):
    delete_user(uid)
    return {"message": "User successfully deleted"}
