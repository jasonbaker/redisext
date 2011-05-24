def pipeline(redis, key):
    """
    Get a pipeline for *key*.  Useful if you don't know whether a redis object
    is sharded or non-sharded.
    """
    if getattr(redis, 'get_redis', None):
        redis = redis.get_redis(key)
    return redis.pipeline()
