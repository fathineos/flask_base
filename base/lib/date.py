from datetime import datetime
from pytz import timezone as tz
from .exceptions import NoTimezoneSet
from iso8601 import parse_date


FMT_ANSI = "%Y-%m-%d %H:%M:%S"
FMT_ISO8601 = "%Y-%m-%dT%H:%M:%SZ"
TZ_UTC = "UTC"
TZ_EET = "EET"


class Date(object):

    def __init__(self, timezone):
        if not timezone:
            raise NoTimezoneSet
        self._timezone = tz(timezone)
        self._datetime = datetime.now(self._timezone)

    def from_datetime(self, datetime):
        self._datetime = datetime
        return self

    def from_timestamp(self, timestamp):
        self._datetime = datetime.fromtimestamp(int(timestamp),
                                                self._timezone)
        return self

    def from_string(self, datestring, fmt=FMT_ISO8601):
        if fmt == FMT_ISO8601:
            self._datetime = parse_date(datestring, self._timezone)
        else:
            self._datetime = self._timezone.localize(
                datetime.strptime(datestring, fmt))
        return self

    def to_datetime(self):
        return self._datetime

    def to_string(self, date_format=FMT_ANSI):
        return self._datetime.strftime(date_format)
