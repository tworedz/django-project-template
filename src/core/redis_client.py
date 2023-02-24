from datetime import timedelta
import pickle
from typing import Any
from typing import Union

from django.conf import settings
import redis


class BaseRedisClient:
    prefix = None

    def __init__(self):
        pool = redis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
        )
        self.__redis = redis.Redis(connection_pool=pool)

    def get(self, key: Union[int, str]) -> Any:
        _key = self.generate_key(key)
        value = self.__redis.get(name=_key)
        return pickle.loads(value)

    def set(  # noqa: A003
        self,
        key: Union[int, str],
        value: Any,
        ttl: int = settings.CACHE_EXPIRATION_SECONDS,
    ) -> None:
        _key = self.generate_key(key)
        pickled_value = pickle.dumps(value)
        self.__redis.set(name=_key, value=pickled_value, ex=timedelta(seconds=ttl))

    def generate_key(self, key: Union[int, str]) -> str:
        if not self.prefix:
            raise AssertionError("Prefix must be set !")
        return f"{self.prefix}.{key}"

    @classmethod
    def factory(cls):
        return cls()
