from redisext.shard import ShardedRedis

import mock

connections = {'a' : mock.Mock(),
               'b' : object(),
               'c' : object(),
               'd' : object()}

def test_connection():
    r = ShardedRedis(connections)
    actual_connection = r.get_redis("foo")
    assert actual_connection == connections['a']

def test_getattr():
    r = ShardedRedis(connections)
    r.get('foo')
    assert connections['a'].get.called
