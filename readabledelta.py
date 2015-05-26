from __future__ import unicode_literals

from datetime import timedelta


def to_human_readable(delta):
    years, days = divmod(delta.days, 365)
    hours, minutes = divmod(delta.seconds, 60*60)
    minutes, seconds = divmod(minutes, 60)
    microseconds = delta.microseconds
    result = ('')
    return result


class readabledelta(timedelta):

    @classmethod
    def from_timedelta(cls, dt):
        return cls(days=dt.days, seconds=dt.seconds, microseconds=dt.microseconds)

    def __str__(self):
        return to_human_readable(self)
