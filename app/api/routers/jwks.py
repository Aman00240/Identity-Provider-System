import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from fastapi import APIRouter, HTTPException

from app.config import settings

router = APIRouter(tags=["Public Keys"])


def int_to_base64url(value: int) -> str:
    value_hex = format(value, "x")

    if len(value_hex) % 2 == 1:
        value_hex = "0" + value_hex

    value_bytes = bytes.fromhex(value_hex)

    return base64.urlsafe_b64encode(value_bytes).rstrip(b"=").decode("utf-8")


@router.get("/.well-known/jwks.json")
async def get_jwks():

    public_key = serialization.load_pem_public_key(settings.PUBLIC_KEY.encode("utf-8"))

    if not isinstance(public_key, RSAPublicKey):
        raise HTTPException(
            status_code=500, detail="Configured public key is not an RSA key"
        )

    public_numbers = public_key.public_numbers()

    jwk = {
        "kty": "RSA",
        "use": "sig",
        "alg": settings.ALGORITHM,
        "kid": "idp-key-1",
        "n": int_to_base64url(public_numbers.n),
        "e": int_to_base64url(public_numbers.e),
    }

    return {"keys": [jwk]}
