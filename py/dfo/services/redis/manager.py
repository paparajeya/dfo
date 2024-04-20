# -*- coding: utf-8 -*-
"""
@Author     : Dr Prashant Aparajeya
                Founder & Director @AISimply Ltd
                Computer Vision Scientist
                London, United Kingdom
                
@Copyright  : Copyright 2024 - present
@Project    : Dispersive Flies Optimization (DFO) Algorithm
"""

import logging
import json
import aioredis
import pickle
from functools import wraps
from aioredis.lock import Lock

from core.config import settings

log = logging.getLogger(__name__)


class RedisManager:
    def __init__(self) -> None:
        # Redis Connection
        self.client = self.create_redis_session()
        
    def create_redis_session(self, redis_url: str = settings.REDIS_URL):
        return aioredis.from_url(str(redis_url))

    async def delete(self, cache_key: str):
        if await self.exists(cache_key):
            await self.client.delete(cache_key)
            return True
        return False

    async def exists(self, cache_key: str):
        return await self.client.exists(cache_key)

    async def get(self, cache_key: str, _Class=None):
        try:
            with self.client.lock(f"lock:{cache_key}"):
                if _Class is None or _Class == "str":
                    return await self.client.get(cache_key)
                else:
                    serialized_obj = await self.client.get(cache_key)
                    if serialized_obj:
                        return pickle.loads(serialized_obj)
                    return None
        except Exception as e:
            log.exception(e)
            return None

    async def get_data_with_key_prefix(
        self, prefix: str, data_type: str = "str", _Class=None
    ):
        keys = await self.get_keys_with_prefix(prefix)
        data = {}

        # Get data
        for key in keys:
            if data_type.lower() == "json":
                data[key[len(prefix) :]] = await self.get_json(key)
            else:
                data[key[len(prefix) :]] = await self.get(key, _Class)
                
        # Return data
        return data

    async def get_json(self, cache_key: str):
        try:
            with self.client.lock(f"lock:{cache_key}"):
                # Get the JSON data
                data = await self.get(cache_key)
                return json.loads(data) if data else None
        except Exception as e:
            log.exception(e)
            return None
    
    async def get_key_expiry_time(self, cache_key: str, in_millis: bool=False) -> int:
        if await self.exists(cache_key):
            if in_millis:
                return await self.client.pttl(cache_key)
            return await self.client.ttl(cache_key)
        return 0
        
    def get_lock(self, cache_key: str):
        return self.client.lock(self.lock_key(cache_key))
                
    async def get_keys_with_prefix(self, prefix: str):
        return await self.client.keys(prefix + "*")
    
    def lock_key(self, cache_key: str) -> str:
        return f"lock:{cache_key}"
    
    def release_lock(self, lock: Lock):
        return lock.release()
        
    async def set(self, cache_key: str, value: str, expire: float = settings.REDIS_EXPIRY):
        if isinstance(value, str):
            if expire > 0:
                await self.client.set(cache_key, value, ex=expire)
            else:
                await self.client.set(cache_key, value)
        elif isinstance(value, dict):
            await self.set_json(cache_key, value, expire)
        else:
            serialized_obj = pickle.dumps(value)
            if expire > 0:
                await self.client.set(cache_key, serialized_obj, ex=expire)
            else:
                await self.client.set(cache_key, serialized_obj)
        if expire <= 0:
            await self.client.persist(cache_key)

    async def set_json(
        self, cache_key: str, value: dict, expire: float = settings.REDIS_EXPIRY
    ):
        try:
            with self.client.lock(self.lock_key(cache_key)):
                await self.client.set(cache_key, json.dumps(value, default=str))

                if expire <= 0:
                    await self.client.persist(cache_key)
                else:
                    await self.client.expire(cache_key, expire)
                
        except Exception as e:
            log.exception(e)


redis_manager = RedisManager()


async def redis_cache(function):
    @wraps(function)
    async def wrapper(*args, **kwargs):
        key = kwargs.get("key")
        expire = kwargs.get("expire", settings.REDIS_EXPIRY)
        data_type = kwargs.get("data_type")
        redis_manager: RedisManager = kwargs.get("redis_manager", RedisManager())

        # Check if the result is already in the cache
        if cached_result := await redis_manager.get(key, _Class=data_type):
            return cached_result

        # If the result is not in the cache, execute the function
        result = await function(*args, **kwargs)

        # Store the result in the cache
        await redis_manager.set(key, result, expire)

        return result

    return wrapper


async def redis_json_cache(function):
    @wraps(function)
    async def wrapper(*args, **kwargs):
        key = kwargs.get("key")
        expire = kwargs.get("expire", settings.REDIS_EXPIRY)
        redis_manager: RedisManager = kwargs.get("redis_manager", RedisManager())

        # Check if the result is already in the cache
        if cached_result := await redis_manager.get_json(key):
            return cached_result

        # If the result is not in the cache, execute the function
        result = await function(*args, **kwargs)

        # Store the result in the cache
        await redis_manager.set_json(key, result, expire)

        return result

    return wrapper


async def redis_data_prefix_cache(function):
    @wraps(function)
    async def wrapper(*args, **kwargs):
        prefix = kwargs.get("prefix")
        expire = kwargs.get("expire", settings.REDIS_EXPIRY)
        data_type = kwargs.get("data_type", "json")
        redis_manager: RedisManager = kwargs.get("redis_manager", RedisManager())

        # Check if the result is already in the cache
        if cached_result := await redis_manager.get_data_with_key_prefix(prefix, data_type=data_type):
            return cached_result

        # If the result is not in the cache, execute the function
        result = await function(*args, **kwargs)

        # Store the result in the cache
        for key in result:
            await redis_manager.set_json(f"{prefix}{key}", result[key], expire)

        return result

    return wrapper

async def redis_lock_cache(function):
    @wraps(function)
    async def wrapper(*args, **kwargs):
        lock_key = kwargs.get("lock_key", "default_lock")
        redis_manager: RedisManager = kwargs.get("redis_manager", RedisManager())

        # Get the lock
        with await redis_manager.get_lock(lock_key):
            # execute the function
            result = await function(*args, **kwargs)
            return result

    return wrapper