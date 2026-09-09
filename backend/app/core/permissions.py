from fastapi import Depends, HTTPException, status

from app.core.auth import get_current_user
from app.models.user import User


def admin_required(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource."
        )

    return current_user