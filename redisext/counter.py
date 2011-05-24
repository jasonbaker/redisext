from datetime import date, datetime

class DailyRollingCounter(object):
    """
    Create a counter that will count something over a rolling 30-day period.
    """
    def __init__(self, redis, key, days=30):
        self.days = days
        self.key = key
        self.redis = redis

    def incr(self, by=1):
        hashkey = 'counter@{0}'.format(date.today().strftime('%Y%m%d'))
        self.redis.hincrby(self.key, hashkey, by)
        self.redis.expire(self.key, self.days*24*60*60)

    def _date_from_key(self, key):
        strdate = key.partition('@')[2]
        return datetime.strptime(strdate, '%Y%m%d').date()

    def value(self):
        """
        Get the current value of the counter.  Note that this will prune old
        records.
        """
        hashdata = self.redis.hgetall(self.key)
        timekeys = [(key, int(count)) for (key, count)
                    in hashdata.iteritems() if key.startswith('counter@')]
        unused_keys = []
        total_count = 0
        for key, count in timekeys:
            keydate = self._date_from_key(key)
            days_old = (date.today() - keydate).days
            if days_old <= self.days:
                total_count += count
            else:
                unused_keys.append(key)

        # prune old keys
        pipe = self.redis.pipeline()
        for hashkey in unused_keys:
            pipe.hdel(self.key, hashkey)
        pipe.execute()
        return total_count
