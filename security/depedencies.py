from fastapi import Depends, HTTPException, status
from database.models.user import Userdb
from security.jwt import get_current_user


def get_current_admin(
    current_user: Userdb = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user