import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config import settings
from app.core.database_con import get_session
from app.repositories.oauth_client import OAuthClientRepository
from app.repositories.user import UserRepository


async def get_user_repo(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


async def get_oauth_client_repo(
    session: AsyncSession = Depends(get_session),
) -> OAuthClientRepository:
    return OAuthClientRepository(session)


oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    token: str = Depends(oauth_scheme),
    user_repo: UserRepository = Depends(get_user_repo),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.PUBLIC_KEY, algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )

    except jwt.InvalidTokenError:
        raise credentials_exception

    user = await user_repo.get_user_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user
