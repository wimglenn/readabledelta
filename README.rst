Installation
------------

``pip install readabledelta``


Usage examples
--------------

The ``readabledelta`` is just a more human-friendly printable version of ``timedelta``.  The public interface is equivalent to timedelta, only printing behaviour has been modified.

It's easy to confuse hours/minutes with minutes/seconds in the default formatting of timedeltas

>>> lunchtime = datetime(year=2015, month=5, day=27, hour=12)
>>> right_now = datetime(year=2015, month=5, day=27, hour=13, minute=5)
>>> 'Lunch was {} ago'.format(delta)
'Lunch was 1:05:00 ago'
>>> 'Lunch was {} ago'.format(readabledelta(delta))
'Lunch was 1 hour and 5 minutes ago'

For negative timedeltas, the default representation is more machine-friendly than human-friendly: "an hour and five minutes" back is easier for people to understand than the weird but technically-correct "negative one day plus 22 hours and 55 minutes"

>>> '{}'.format(lunchtime - right_now)
'-1 day, 22:55:00'
>>> '{}'.format(readabledelta(lunchtime - right_now))
'-1 hour and 5 minutes'

A readabledelta *is a* timedelta, compares as you'd expect, and is simple enough not to misbehave.

>>> issubclass(readabledelta, timedelta)
True
>>> isinstance(readabledelta(), timedelta)
True
>>> readabledelta() == timedelta()
True

This means you can safely add or subtract them to ``datetime`` instances, there will be no unpleasant surprises with arithmetic.
