import redis.asyncio as redis

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

async def redis_store_refresh_token(user_id: str, token: str):
    key = f"refresh:{user_id}"
    await redis_client.set(key, token, ex=60 * 60 * 24 * 7)  # 7 days

async def redis_verify_refresh_token(user_id: str, token: str) -> bool:
    key = f"refresh:{user_id}"
    stored = await redis_client.get(key)
    return stored and stored.decode() == token

async def redis_retrieve_refresh_token(user_id: str):
    key = f"refresh:{user_id}"
    stored_token = await redis_client.get(key)
    return stored_token


