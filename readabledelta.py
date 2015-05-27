from __future__ import unicode_literals

from datetime import timedelta


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

    def __str__(self):
        return to_string(self)

    def __add__(self, other):
        if isinstance(other, timedelta):
            return readabledelta(
                self.days + other.days,
                self.seconds + other.seconds,
                self.microseconds + other.microseconds,
            )
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, timedelta):
            return readabledelta(
                self.days - other.days,
                self.seconds - other.seconds,
                self.microseconds - other.microseconds,
            )
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, timedelta):
            return -self + other
        return NotImplemented

    def __abs__(self):
        return -self if self.days < 0 else self

    def __neg__(self):
        return readabledelta(-self.days, -self.seconds, -self.microseconds)

    def __mul__(self, other):
        if isinstance(other, int):
            return readabledelta(
                self.days * other,
                self.seconds * other,
                self.microseconds * other,
            )
        return NotImplemented

    __rmul__ = __mul__

    def __floordiv__(self, other):
        if not isinstance(other, (int, timedelta)):
            return NotImplemented
        usec = delta_to_microseconds(self)
        if isinstance(other, timedelta):
            return usec // delta_to_microseconds(other)
        elif isinstance(other, int):
            return readabledelta(0, 0, usec // other)

    def __mod__(self, other):
        if isinstance(other, timedelta):
            r = delta_to_microseconds(self) % delta_to_microseconds(other)
            return readabledelta(0, 0, r)
        return NotImplemented

    def __divmod__(self, other):
        if isinstance(other, timedelta):
            q, r = divmod(delta_to_microseconds(self), delta_to_microseconds(other))
            return q, readabledelta(0, 0, r)
        return NotImplemented


def delta_to_microseconds(td):
    return (td.days * (24*60*60) + td.seconds) * 1000000 + td.microseconds


def to_string(delta, include_microseconds=False, include_sign=True):
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
