from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database_con import get_session
from app.repositories.oauth_client import OAuthClientRepository
from app.repositories.user import UserRepository


async def get_user_repo(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


async def get_oauth_client_repo(
    session: AsyncSession = Depends(get_session),
) -> OAuthClientRepository:
    return OAuthClientRepository(session)
