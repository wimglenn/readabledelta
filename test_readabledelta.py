from __future__ import unicode_literals

from datetime import timedelta
from unittest import TestCase

from readabledelta import readabledelta


class TestReadableDelta(TestCase):

    def setUp(self):
        self.dt_original = timedelta(days=400, hours=5, minutes=6, seconds=7, microseconds=8)
        self.dt_readable = readabledelta(days=400, hours=5, minutes=6, seconds=7, microseconds=8)

    def test_is_a_timedelta(self):
        self.assertIsInstance(self.dt_readable, timedelta)

    def test_has_equality_with_original(self):
        self.assertEqual(self.dt_readable, self.dt_original)

    def test_instantiate_from_classmethod(self):
        dt_readable_from_dt_original = readabledelta.from_timedelta(self.dt_original)
        self.assertEqual(dt_readable_from_dt_original, self.dt_readable)
