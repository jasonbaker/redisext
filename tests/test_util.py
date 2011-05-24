from redis import Redis
from redis.client import Pipeline

from redisext.util import pipeline
from redisext.shard import ShardedRedis

class TestPipeline(object):
    def test_with_redis(self):
        r = Redis()
        p = pipeline(r, 'foo')
        assert isinstance(p, Pipeline)

    def test_with_shard(self):
        s = ShardedRedis({'a' : Redis()})
        p = pipeline(s, 'foo')
        assert isinstance(p, Pipeline)
