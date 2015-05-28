from __future__ import unicode_literals

from datetime import timedelta

__version__ = '0.0.1'


class readabledelta(timedelta):

    def __new__(cls, *args, **kwargs):
        years = kwargs.pop('years', 0)
        if 'days' in kwargs:
            kwargs['days'] += 365 * years
        elif years:
            arg0 = args[0] if args else 0
            args = (365 * years + arg0,) + args[1:]
        self = timedelta.__new__(cls, *args, **kwargs)
        return self

    @classmethod
    def from_timedelta(cls, dt):
        return cls(days=dt.days, seconds=dt.seconds, microseconds=dt.microseconds)

    def __unicode__(self):
        return to_string(self)

    __str__ = __unicode__


def to_string(delta, include_microseconds=False, include_sign=False):
    negative = delta < timedelta(0)
    delta = abs(delta)

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

    if not output:
        result = 'now'
    elif len(output) == 1:
        result, = output
    else:
        left, right = output[:-1], output[-1:]
        result = ', '.join(left) + ' and ' + right[0]

    if include_sign and negative:
        result = '-' + result

    return result
