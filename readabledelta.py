from __future__ import unicode_literals

from datetime import timedelta


def to_human_readable(dt):
    return ''


class readabledelta(timedelta):
    def __str__(self):
        return to_human_readable(self)
