from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import get_oauth_client_repo
from app.repositories.oauth_client import OAuthClientRepository
from app.schemas.oauth_client import OAuthClientCreate, OAuthClientResponse

router = APIRouter(prefix="/clients", tags=["OAuth Clients"])


@router.post(
    "/register", response_model=OAuthClientResponse, status_code=status.HTTP_201_CREATED
)
async def register_client(
    client_in: OAuthClientCreate,
    client_repo: OAuthClientRepository = Depends(get_oauth_client_repo),
):
    try:
        new_client = client_repo.create_client(
            client_id=client_in.client_id,
            client_secret=client_in.client_secret,
            redirect_uris=[str(uri) for uri in client_in.redirect_uris],
        )
        return new_client
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client ID already exists. Please choose a different one",
        )
