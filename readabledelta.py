from __future__ import unicode_literals, division

from collections import OrderedDict
from datetime import timedelta

__version__ = '0.1.0'


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


def to_string(delta, include_sign=False):
    negative = delta < timedelta(0)
    delta = abs(delta)

    # datetime.timedelta are normalized internally in Python to the units days, seconds, microseconds allowing a unique
    # representation.  This is not the only possible basis; the calculations below rebase onto more human friendly keys
    units = {
        'millennia': None,
        'centuries': 10,
        'decades': 10,
        'years': 10,
        'weeks': 365.25/7,
        'days': 7,
        'hours': 24,
        'minutes': 60,
        'seconds': 60,
        'milliseconds': 1000,
        'microseconds': 1000,
    }
    data = OrderedDict.fromkeys(units, 0)
    # rebase days onto years, weeks, days
    data['years'], data['days'] = divmod(delta.days, 365)
    data['weeks'], data['days'] = divmod(data['days'], 7)
    # rebase seconds onto hours, minutes, seconds
    data['hours'], data['seconds'] = divmod(delta.seconds, 60*60)
    data['minutes'], data['seconds'] = divmod(data['seconds'], 60)
    # rebase microseconds onto milliseconds, microseconds
    data['milliseconds'], data['microseconds'] = divmod(delta.microseconds, 1000)

    # round to 2 significant "digits"
    try:
        first_significant_unit, first_significant_value = next((k,v) for (k,v) in data.items() if v > 0)
    except StopIteration:
        assert delta == timedelta(0)
        assert set(data.values()) == {0}
        return 'an instant'

    if first_significant_unit == 'microseconds':
        result = '{} microsecond{}'.format(first_significant_value, '' if first_significant_value == 1 else 's')
    elif first_significant_unit == 'milliseconds':
        result = ''

    if include_sign and negative:
        result = '-' + result

    return result


# TODO: better test suite
#       wheel packaging
#       travis CI
#       coverage
#       docs
#       add arithmetic operators
