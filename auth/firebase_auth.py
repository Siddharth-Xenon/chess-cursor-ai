import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, status

# Initialize Firebase Admin SDK
# Note: You need to download your Firebase Admin SDK JSON file and replace 'path/to/your/firebase-sdk.json' with its path
cred = credentials.Certificate(
    "keys\chess-tutor-520-firebase-adminsdk-byee5-e23511e61b.json"
)
firebase_admin.initialize_app(cred)


def create_user(email: str, password: str, username: str):
    """
    Create a new user with email and password
    """
    try:
        user = auth.create_user(email=email, password=password, display_name=username)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating user: {e}"
        )


def verify_id_token(token: str):
    """
    Verify the ID token from the client
    """
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}"
        )


def get_user(uid: str):
    """
    Get a user by UID
    """
    try:
        user = auth.get_user(uid)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found: {e}"
        )


def update_user(
    uid: str, email: str = None, password: str = None, username: str = None
):
    """
    Update user details
    """
    try:
        user = auth.update_user(
            uid, email=email, password=password, display_name=username
        )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating user: {e}"
        )


def delete_user(uid: str):
    """
    Delete a user by UID
    """
    try:
        auth.delete_user(uid)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error deleting user: {e}"
        )
