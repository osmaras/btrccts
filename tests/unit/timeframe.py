import pandas
import unittest
from sccts.timeframe import Timeframe
from tests.common import pd_ts


class TimeframeTest(unittest.TestCase):

    def test__init__end_date_smaller_than_start_date(self):
        with self.assertRaises(ValueError) as e:
            Timeframe(pd_start_date=pd_ts('2017-02-01'),
                      pd_end_date=pd_ts('2017-01-01'),
                      pd_timedelta=pandas.Timedelta(minutes=1))
        self.assertEqual(str(e.exception),
                         'Timeframe: end date is smaller then start date')

    def test__init__timedelta_negative(self):
        with self.assertRaises(ValueError) as e:
            Timeframe(pd_start_date=pd_ts('2017-01-01 1:00'),
                      pd_end_date=pd_ts('2017-01-01 1:03'),
                      pd_timedelta=pandas.Timedelta(minutes=-1))
        self.assertEqual(str(e.exception),
                         'Timeframe: timedelta needs to be positive')

    def test__add_timedelta__date(self):
        t = Timeframe(pd_start_date=pd_ts('2017-01-01 1:00'),
                      pd_end_date=pd_ts('2017-01-01 1:03'),
                      pd_timedelta=pandas.Timedelta(minutes=1))
        self.assertEqual(t.date(), pd_ts('2017-01-01 1:00'))
        # should return the same value
        self.assertEqual(t.date(), pd_ts('2017-01-01 1:00'))
        t.add_timedelta()
        self.assertEqual(t.date(), pd_ts('2017-01-01 1:01'))
        t.add_timedelta()
        t.add_timedelta()
        self.assertEqual(t.date(), pd_ts('2017-01-01 1:03'))
        t.add_timedelta()
        self.assertEqual(t.date(), None)

    def test__different_timedelta(self):
        t = Timeframe(pd_start_date=pd_ts('2017-01-01 1:00'),
                      pd_end_date=pd_ts('2017-01-01 1:35'),
                      pd_timedelta=pandas.Timedelta(minutes=15))
        t.add_timedelta()
        self.assertEqual(t.date(), pd_ts('2017-01-01 1:15'))
        t.add_timedelta()
        self.assertEqual(t.date(), pd_ts('2017-01-01 1:30'))
        t.add_timedelta()
        self.assertEqual(t.date(), None)

    def test__start_date(self):
        t = Timeframe(pd_start_date=pd_ts('2017-01-01 1:00'),
                      pd_end_date=pd_ts('2017-01-01 1:35'),
                      pd_timedelta=pandas.Timedelta(minutes=15))
        self.assertEqual(t.start_date(), pd_ts('2017-01-01 1:00'))

    def test__end_date(self):
        t = Timeframe(pd_start_date=pd_ts('2017-01-01 1:00'),
                      pd_end_date=pd_ts('2017-01-01 1:35'),
                      pd_timedelta=pandas.Timedelta(minutes=15))
        self.assertEqual(t.end_date(), pd_ts('2017-01-01 1:35'))
