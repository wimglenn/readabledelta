from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
from datetime import timedelta
from StringIO import StringIO
from unittest import TestCase

from readabledelta import readabledelta


class TestReadableDelta(TestCase):

    def setUp(self):
        self.td = timedelta(days=400, hours=5, minutes=1, seconds=7, microseconds=8)
        self.rd = readabledelta(days=400, hours=5, minutes=1, seconds=7, microseconds=8)

    def test_is_a_timedelta(self):
        self.assertIsInstance(self.rd, timedelta)

    def test_has_equality_with_original(self):
        self.assertEqual(self.rd, self.td)

    def test_instantiate_from_classmethod(self):
        rd_from_td = readabledelta.from_timedelta(self.td)
        self.assertEqual(rd_from_td, self.rd)

    def test_creates_human_readable_string_when_formatted(self):
        actual = '{}'.format(self.rd)
        expected = '1 year, 35 days, 5 hours, 1 minute and 7 seconds'
        self.assertEqual(actual, expected)

    def test_skips_zero_values(self):
        actual = unicode(readabledelta(seconds=3 + 60*60))
        expected = '1 hour and 3 seconds'
        self.assertEqual(actual, expected)

    def test_repr_untouched(self):
        self.assertEqual(eval(repr(self.rd)), self.rd)

    def test_readable_when_printed(self):
        out = StringIO()
        print(readabledelta(days=1), file=out, end=' spam')
        actual = out.getvalue()
        expected = '1 day spam'
        self.assertEqual(actual, expected)

    def test_sign_included_for_negative_deltas(self):
        dt_before = datetime(year=1982, month=3, day=19, second=10)
        dt_after = datetime(year=1982, month=3, day=19, second=15)
        minus_5_seconds = readabledelta.from_timedelta(dt_before - dt_after)
        plus_5_seconds = readabledelta.from_timedelta(dt_after - dt_before)
        self.assertEqual(unicode(minus_5_seconds), '-5 seconds')
        self.assertEqual(unicode(plus_5_seconds), '5 seconds')
