import json

import redis.asyncio as redis

from app.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


async def save_authorization_code(code: str, user_id: str, client_id: str):
    payload = {"user_id": user_id, "client_id": client_id}

    await redis_client.set(f"auth_code:{code}", json.dumps(payload), ex=300)


async def get_and_delete_authorization_code(code: str) -> dict | None:
    key = f"auth_code:{code}"

    data = await redis_client.get(key)

    if data:
        await redis_client.delete(key)
        return json.loads(data)

    return None
