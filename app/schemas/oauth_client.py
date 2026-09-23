from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class OAuthClientCreate(BaseModel):
    client_id: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Client ID must be 3-50 characters and contain only letters, numbers, dashes, or underscores",
    )
    client_secret: str = Field(
        min_length=16,
        max_length=128,
        description="Client secret must be at least 16 characters long",
    )
    redirect_uris: list[HttpUrl] = Field(
        min_length=1,
        description="Must provide at least one valid redirect URI (e.g., https://app.example.com/callback).",
    )


class OAuthClientResponse(BaseModel):
    client_id: str
    redirect_uris: list[str]

    model_config = ConfigDict(from_attributes=True)
