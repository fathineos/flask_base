from datetime import datetime, timedelta
from base.lib.date import Date, FMT_ANSI, FMT_ISO8601, TZ_UTC
from base.lib.testing import TestCase
from pytz import timezone


class TestDate(TestCase):

    def test_to_datetime(self):
        date = Date(timezone=TZ_UTC)
        date.from_timestamp(timestamp="1451260800")
        expected_datetime = datetime(2015, 12, 28, 0, 0, 0, 0,
                                     timezone(TZ_UTC))
        self.assertEquals(date.to_datetime(), expected_datetime)

    def test_from_string_when_format_is_ansi(self):
        date = Date(timezone=TZ_UTC)
        date.from_string(datestring="2015-12-28 01:02:03", fmt=FMT_ANSI)
        expected_datetime = datetime(2015, 12, 28, 1, 2, 3, 0,
                                     timezone(TZ_UTC))
        self.assertEquals(expected_datetime, date.to_datetime())

    def test_from_string_when_format_is_iso8601(self):
        date = Date(timezone=TZ_UTC)
        date.from_string(datestring="2015-12-28T01:02:03Z", fmt=FMT_ISO8601)
        expected_datetime = datetime(2015, 12, 28, 1, 2, 3, 0,
                                     timezone(TZ_UTC))
        self.assertEquals(expected_datetime, date.to_datetime())

    def test_from_string_when_format_is_iso8601_not_overrites_datestring_timezone(self):
        date = Date(timezone=TZ_UTC)
        date.from_string(datestring="2015-12-28T01:02:03+02:00",
                         fmt=FMT_ISO8601)
        utc_datetime = datetime(2015, 12, 28, 1, 2, 3, 0, timezone(TZ_UTC))
        self.assertNotEquals(utc_datetime, date.to_datetime())
        self.assertEquals(timedelta(hours=2),
                          utc_datetime - date.to_datetime())

    def test_to_string(self):
        date = Date(timezone=TZ_UTC)
        date.from_timestamp(timestamp="1451260800")
        self.assertEquals("2015-12-28T00:00:00Z", date.to_string(FMT_ISO8601))

    def test_to_string_from_not_utc_timezone(self):
        date = Date(timezone=TZ_UTC)
        date.from_string(datestring="2015-12-28T05:00:00+02:00",
                         fmt=FMT_ISO8601)
        self.assertEquals("2015-12-28 03:00:00", date.to_string())

    def test_to_datetime_without_tz_info(self):
        date = Date(timezone=TZ_UTC)
        date.from_string(datestring="2015-12-28T05:00:00+02:00",
                         fmt=FMT_ISO8601)
        result_datetime = date.to_datetime_without_tz_info()
        expected_datetime = datetime(2015, 12, 28, 3, 0, 0)
        self.assertEquals(expected_datetime, result_datetime)
