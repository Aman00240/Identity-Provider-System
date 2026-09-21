from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database_con import Base


class OAuthClient(Base):
    __tablename__ = "oauth_clients"

    client_id: Mapped[str] = mapped_column(primary_key=True)
    client_secret_hash: Mapped[str]
    redirect_uris: Mapped[list[str]] = mapped_column(JSONB)
