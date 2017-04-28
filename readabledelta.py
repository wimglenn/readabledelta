from __future__ import unicode_literals

from datetime import timedelta

__version__ = '0.0.2'


class readabledelta(timedelta):

    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], timedelta):
            td = args[0]
            self = timedelta.__new__(cls, td.days, td.seconds, td.microseconds)
        else:
            self = timedelta.__new__(cls, *args, **kwargs)
        return self

    def __unicode__(self):
        return to_string(self)

    __str__ = __unicode__


def to_string(delta):
    negative = delta < timedelta(0)
    delta = abs(delta)

    keys = 'weeks', 'days', 'hours', 'minutes', 'seconds', 'milliseconds', 'microseconds'
    # datetime.timedelta are normalized internally in Python to the units days, seconds, microseconds allowing a unique
    # representation.  This is not the only possible basis; the calculations below rebase onto more human friendly keys
    data = {}
    # rebase days onto weeks, days
    data['weeks'], data['days'] = divmod(delta.days, 7)
    # rebase seconds onto hours, minutes, seconds
    data['hours'], data['seconds'] = divmod(delta.seconds, 60*60)
    data['minutes'], data['seconds'] = divmod(data['seconds'], 60)
    # rebase microseconds onto milliseconds, microseconds
    data['milliseconds'], data['microseconds'] = divmod(delta.microseconds, 1000)

    output = ['{} {}'.format(data[k], k[:-1] if data[k] == 1 else k) for k in keys if data[k] != 0]

    if not output:
        result = 'an instant'
    elif len(output) == 1:
        [result] = output
    else:
        left, right = output[:-1], output[-1:]
        result = ', '.join(left) + ' and ' + right[0]

    if negative:
        result = '-' + result

    return result
