from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
from datetime import timedelta
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO  # Python 3
from unittest import TestCase

from readabledelta import readabledelta


class TestReadableDelta(TestCase):

    def setUp(self):
        self.dt = datetime(year=1982, month=3, day=19)
        self.td = timedelta(days=400, hours=5, minutes=1, seconds=7, microseconds=8)
        self.rd = readabledelta(days=400, hours=5, minutes=1, seconds=7, microseconds=8)

    def test_is_a_timedelta(self):
        self.assertIsInstance(self.rd, timedelta)

    def test_has_equality_with_original(self):
        self.assertEqual(self.rd, self.td)

    def test_can_instantiate_from_classmethod(self):
        rd_from_td = readabledelta.from_timedelta(self.td)
        self.assertEqual(rd_from_td, self.rd)

    def test_readable_when_formatted(self):
        actual = '{}'.format(self.rd)
        expected = '1 year, 35 days, 5 hours, 1 minute and 7 seconds'
        self.assertEqual(actual, expected)

    def test_readable_when_printed(self):
        out = StringIO()
        print(readabledelta(days=1), file=out, end=' spam')
        actual = out.getvalue()
        expected = '1 day spam'
        self.assertEqual(actual, expected)

    def test_skips_zero_values(self):
        actual = str(readabledelta(seconds=3 + 60*60))
        expected = '1 hour and 3 seconds'
        self.assertEqual(actual, expected)

    def test_repr_untouched(self):
        self.assertEqual(eval(repr(self.rd)), self.rd)

    def test_can_instantiate_with_years(self):
        rd1 = readabledelta(years=1, hours=1)
        rd2 = readabledelta(days=365, hours=1)
        self.assertEqual(rd1, rd2)
        self.assertEqual(str(rd1), str(rd2))

    def test_can_add_to_datetime(self):
        actual = self.dt + self.rd
        expected = datetime(1983, 4, 23, 5, 1, 7, 8)
        self.assertEqual(actual, expected)

    def test_can_subtract_from_datetime(self):
        actual = self.dt - self.rd
        expected = datetime(1981, 2, 11, 18, 58, 52, 999992)
        self.assertEqual(actual, expected)

    def test_arithmetic_returns_to_native_delta(self):
        rd, td = self.rd, self.td
        tests = [rd + rd, rd + td, td + rd, td - rd, rd - td, -rd, abs(rd), rd * 2, rd / 2, rd // 2]
        for x in tests:
            self.assertIsInstance(x, timedelta)
