from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password, create_access_token
from app.modules.auth import repository
from app.modules.auth.models import User
from app.modules.auth.schemas import UserOut


async def login(db: AsyncSession, email: str, password: str) -> str:
    user = await repository.get_user_by_email(db, email.lower())
    if not user or not user.is_active or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    roles = await repository.get_roles(db, user.id)
    return create_access_token(str(user.id), str(user.society_id), roles)


async def get_user(db: AsyncSession, user: User) -> UserOut:
    roles = await repository.get_roles(db, user.id)
    return UserOut(id=user.id, society_id=user.society_id, name=user.name,
               email=user.email, roles=roles)