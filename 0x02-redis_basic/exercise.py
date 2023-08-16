#!/usr/bin/env python3
""" Caching data with the us of Redis: Store,Retrieve,and Display """

import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def call_history(method: Callable) -> Callable:
    """ Store the history of inputs and outputs for a particular function """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ Wrapped function """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


def count_calls(method: Callable) -> Callable:
    """ Count how many times methods of the Cache class are called """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ Wrapped function """
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


class Cache:
    """ Caching class """
    def __init__(self):
        """ Constructor - initialize the Redis client instance and flush the DB """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store the input data in Redis using a random key and return the key """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ Retrieve data from Redis and optionally convert it using a function """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ Automatically parametrize Cache.get to return a string """
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """ Automatically parametrize Cache.get to return an integer """
        data = self._redis.get(key)
        try:
            data = int(data.decode("utf-8"))
        except Exception:
            data = 0
        return data


def replay(method: Callable):
    """ Display the history of calls for a particular function """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"
    redis_instance = method.__self__._redis
    count = redis_instance.get(key).decode("utf-8")
    print(f"{key} was called {count} times:")
    input_list = redis_instance.lrange(inputs, 0, -1)
    output_list = redis_instance.lrange(outputs, 0, -1)
    redis_zipped = list(zip(input_list, output_list))
    for a, b in redis_zipped:
        attr, data = a.decode("utf-8"), b.decode("utf-8")
        print(f"{key}(*{attr}) -> {data}")
