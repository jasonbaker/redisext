from datetime import date, timedelta

from redis import Redis

from redisext.counter import DailyRollingCounter
from redisext.shard import ShardedRedis

class TestDailyRollingCounter(object):
    def setup(self):
        self.redis = Redis()
        self.redis.flushdb()
        self.counter = DailyRollingCounter(self.redis, 'foo')

    def teardown(self):
        self.redis.flushdb()
        self.redis.connection.disconnect()

    def test_full(self):
        self.counter.incr()
        actual_value = self.counter.value()
        assert actual_value == 1

    def test_prune(self):
        outdated_date = date.today() - timedelta(days=31)
        hashkey = 'counter@{0}'.format(outdated_date.strftime('%Y%m%d'))
        self.redis.hset('foo', hashkey, 1)
        self.counter.value()
        keyvalue = self.redis.hget('foo', hashkey)
        assert keyvalue is None

class TestDailyRollingCounterSharded(object):
    def setup(self):
        super(TestDailyRollingCounter, self).setup()
        self.redis = ShardedRedis({'a' : self.redis})
