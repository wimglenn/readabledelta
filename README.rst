Installation
------------

``pip install readabledelta``



Usage examples
--------------

The ``readabledelta`` is just a more human-friendly printable version of ``timedelta``.  The public interface is equivalent to timedelta (with the exception of the ``years`` kwarg in the constructor - see below).  Only printing behaviour has been modified.  

>>> lunchtime = datetime(year=2015, month=5, day=27, hour=12)
>>> right_now = datetime(year=2015, month=5, day=27, hour=13, minute=5)
>>> delta = right_now - lunchtime
>>> print 'We had lunch {} ago'.format(delta)
We had lunch 1:05:00 ago

Oh, what's that mean an hour and five minutes?  Or it's a minute and five seconds?

>>> rdelta = readabledelta.from_timedelta(delta)
>>> print 'We had lunch {} ago'.format(rdelta)
We had lunch 1 hour and 5 minutes ago

There are often contexts where you don't really care about the sign of the delta, only the absolute value.  But if you are not careful to handle the future or past tense correctly, you get this:

>>> print 'Lunchtime and now are {} apart'.format(lunchtime - right_now)
Lunchtime and now are -1 day, 22:55:00 apart

Huh??  Well, it's *technically* correct that lunchtime and now are negative one day plus 22 hours and 55 minutes apart.  But we don't generally think in terms of negative time just as we don't think in terms of negative lengths; 5 minutes in the future and 5 minutes in the past are both just 5 minutes away.

>>> rd = readabledelta.from_timedelta
>>> print 'Lunchtime and now are {} apart'.format(rd(lunchtime - right_now))
Lunchtime and now are 1 hour and 5 minutes apart

A readabledelta *is a* timedelta, compares as you'd expect, and is simple enough not to misbehave.  

>>> issubclass(readabledelta, timedelta)
True
>>> isinstance(rdelta, timedelta)
True
>>> rdelta == delta
True

This means you can safely add or subtract them to ``datetime`` instances. 



Long deltas
-----------

Python doesn't have great support for "long" deltas, the ``years`` kwarg was missing for example.  

>>> readabledelta(years=1, days=2) == timedelta(days=367)
True
>>> print readabledelta(years=1, seconds=126)
1 year, 2 minutes and 6 seconds


And if you're a human being you don't care about displaying microseconds.  

>>> startup_time = datetime(year=2013, month=1, day=1)
>>> now = datetime.utcnow()
>>> print 'The server has been up for {}'.format(now - startup_time)
The server has been up for 876 days, 8:16:35.116488

>>> print 'The server has been up for {}'.format(rd(now - startup_time))
The server has been up for 2 years, 146 days, 8 hours, 16 minutes and 35 seconds
