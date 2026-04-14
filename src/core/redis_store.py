import time

import redis

from src.core.config import Config

pool = redis.ConnectionPool(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    decode_responses=True
)


class RedisStore:
    def __init__(self):
        self.client = redis.Redis(connection_pool=pool)

    def add_jti_to_blocklist(self, jti: str, expires_in: int):
        print("jti_data", expires_in)
        now = int(time.time())
        ttl = expires_in - now
        if ttl > 0:
            self.client.setex(
                name=f"blocklist:{jti}",
                time=ttl,
                value="true"
            )
            print(f"JTI {jti} đã được đưa vào blocklist trong {ttl} giây.")
        else:
            print("Token đã hết hạn, không cần đưa vào blocklist.")

    def get_blocklist(self) -> list[str]:
        keys = self.client.keys("blocklist:*")
        blocklisted_jtis = []
        for key in keys:
            jti = key.replace("blocklist:", "")
            blocklisted_jtis.append(jti)
        return blocklisted_jtis

    def token_in_blocklist(self, jti: str) -> bool:
        key = f"blocklist:{jti}"
        is_exist = self.client.exists(key)
        return bool(is_exist)


redis_store = RedisStore()
