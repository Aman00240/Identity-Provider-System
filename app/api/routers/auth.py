import secrets
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_oauth_client_repo, get_user_repo
from app.core.cache import save_authorization_code
from app.core.security import create_access_token, verify_password
from app.repositories.oauth_client import OAuthClientRepository
from app.repositories.user import UserRepository

router = APIRouter(prefix="/auth", tags=["Authentication"])
templates = Jinja2Templates(directory="app/templates")


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepository = Depends(get_user_repo),
):
    user = await user_repo.get_user_by_email(form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    jwt_payload = {"sub": str(user.id), "aud": "test_client_id"}

    token = create_access_token(data=jwt_payload)

    return {"access_token": token, "token_type": "bearer"}


@router.get("/authorize", response_class=HTMLResponse)
async def authorize_user(
    request: Request,
    response_type: str = Query(..., pattern="^code$"),
    client_id: str = Query(...),
    redirect_uri: str = Query(...),
    state: str = Query(None),
    client_repo: OAuthClientRepository = Depends(get_oauth_client_repo),
):
    client = await client_repo.get_client_by_id(client_id)

    if not client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid client_id"
        )

    if redirect_uri not in client.redirect_uris:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid redirect_uri"
        )

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "state": state,
        },
    )


@router.post("/login")
async def process_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    client_id: str = Form(...),
    redirect_uri: str = Form(...),
    state: str = Form(None),
    user_repo: UserRepository = Depends(get_user_repo),
):
    user = await user_repo.get_user_by_email(email)

    if not user:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "state": state,
                "error": "Invalid Email or Password",
            },
        )

    if not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "state": state,
                "error": "Invalid Email or Password",
            },
        )

    auth_code = secrets.token_urlsafe(32)

    await save_authorization_code(
        code=auth_code, user_id=str(user.id), client_id=client_id
    )

    query_params = {"code": auth_code}
    if state:
        query_params["state"] = state

    final_redirect_url = f"{redirect_uri}?{urlencode(query_params)}"

    return RedirectResponse(url=final_redirect_url, status_code=status.HTTP_302_FOUND)
