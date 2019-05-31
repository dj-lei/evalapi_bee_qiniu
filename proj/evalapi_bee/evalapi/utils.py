import datetime
from dateutil.relativedelta import relativedelta

from monthdelta import monthdelta, monthmod


def days2datetime(days, base_datetime=None):
    base_datetime = datetime.datetime.now() if not base_datetime else base_datetime

    month_diff = int(days / 30)

    return base_datetime + relativedelta(months=month_diff)


def month_diff(d1, d2):
    """
    return the difference between d1, d2
    """
    # year_diff = d2.year - d1.year
    # month = year_diff * 12 + abs(d1.month - d2.month)
    # month = month if month else 1
    month_diff = monthmod(d1, d2)[0].months
    return month_diff if month_diff else 1


def month_diff2date(diff, base_datetime=None):
    base_datetime = datetime.datetime.now() if not base_datetime else base_datetime
    return base_datetime + monthdelta(diff)