from fastapi import FastAPI

from app.api.routers import oauth_clients, users

app = FastAPI(
    title="Identity Provider API",
    description="Secure IdP built with FastAPI and RSA-signed JWTs",
    version="1.0.0",
)

app.include_router(users.router)
app.include_router(oauth_clients.router)


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "Ok", "message": "Identity Provider is operational"}
