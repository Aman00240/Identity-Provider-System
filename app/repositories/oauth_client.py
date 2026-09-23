from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.oauth_client import OAuthClient


class OAuthClientRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_client(
        self, client_id: str, client_secret: str, redirect_uris: list[str]
    ) -> OAuthClient:
        hashed_secret = get_password_hash(client_secret)

        new_client = OAuthClient(
            client_id=client_id,
            client_secret_hash=hashed_secret,
            redirect_uris=redirect_uris,
        )

        self.session.add(new_client)
        await self.session.commit()
        await self.session.refresh(new_client)

        return new_client

    async def get_client_by_client_id(self, client_id: str) -> OAuthClient | None:
        stmt = select(OAuthClient).where(OAuthClient.client_id == client_id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
