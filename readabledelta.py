from __future__ import unicode_literals

from datetime import timedelta


def to_human_readable(delta, include_microseconds=False):
    keys = 'years', 'days', 'hours', 'minutes', 'seconds'
    if include_microseconds:
        keys += 'microseconds',

    # timedeltas are normalised to just days, seconds, microseconds in cpython
    data = {}
    data['years'], data['days'] = divmod(delta.days, 365)
    data['hours'], _minutes = divmod(delta.seconds, 60*60)
    data['minutes'], data['seconds'] = divmod(_minutes, 60)
    data['microseconds'] = delta.microseconds

    output = ['{} {}'.format(data[k], k[:-1] if data[k] == 1 else k) for k in keys if data[k] != 0]
    result = ', '.join(output)

    return result


class readabledelta(timedelta):

    @classmethod
    def from_timedelta(cls, dt):
        return cls(days=dt.days, seconds=dt.seconds, microseconds=dt.microseconds)

    def __str__(self):
        return to_human_readable(self)
