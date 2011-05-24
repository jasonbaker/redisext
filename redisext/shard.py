from __future__ import absolute_import
import hashlib
import sys

class ShardedRedis(object):
    """
    A wrapper around a Redis object that supports sharding.
    """
    def __init__(self, redis_mapping):
        self.redis_mapping = redis_mapping

    def get_redis(self, name):
        h = hashlib.md5().digest()[0]
        h = ord(h)
        index = h % len(self.redis_mapping)
        keys = self.redis_mapping.keys()
        keys.sort()
        key = keys[index]
        return self.redis_mapping[key]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for r in self.redis_mapping.values():
            r.connection.disconnect()

    def __getattr__(self, name):
        def _wrapper(key, *args, **kwargs):
            connection = self.get_redis(key)
            method = getattr(connection, name)
            return method(key, *args, **kwargs)
        return _wrapper
