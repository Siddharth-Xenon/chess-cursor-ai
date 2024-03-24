from fastapi import APIRouter, Body, Depends, HTTPException
from models.user import UserCreate, UserDisplay, UserUpdate
from auth.firebase_auth import (
    create_user,
    get_user,
    update_user,
    delete_user,
    verify_id_token,
    authenticate_user,  # Assuming this is a new function you will add for authentication
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_id_token(token)
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {e}",
        )


@router.post("/token", response_model=UserDisplay)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    firebase_user = authenticate_user(
        email=form_data.username, password=form_data.password
    )
    if firebase_user:
        return {
            "username": firebase_user.display_name,
            "email": firebase_user.email,
            "token": firebase_user.token,
        }
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


@router.post(
    "/users/",
    response_description="Add new user",
    response_model=UserDisplay,
    dependencies=[],
)
async def create_user_route(user: UserCreate = Body(...)):
    firebase_user = create_user(
        email=user.email, password=user.password, username=user.username
    )
    if firebase_user:
        # Authenticate the user immediately after creation
        token = authenticate_user(email=user.email, password=user.password)
        if token:
            return {"username": user.username, "email": user.email, "token": token}
        else:
            raise HTTPException(
                status_code=400, detail="Authentication failed after user creation"
            )
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
