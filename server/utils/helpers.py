from datetime import datetime
from dateutil.relativedelta import relativedelta

DAILY = "daily"
MONTHLY = "monthly"
YEARLY = "yearly"


def resolve_date_range(frame, date_range):
    # subtract one from the range as today is included
    date_range = int(date_range) - 1
    from_date = datetime.now()
    to_date = datetime.now()

    if frame == DAILY:
        from_date -= relativedelta(days=date_range)
    elif frame == MONTHLY:
        from_date = from_date.replace(day=1)
        from_date -= relativedelta(months=date_range)
    elif frame == YEARLY:
        from_date = from_date.replace(day=1, month=1)
        from_date -= relativedelta(years=date_range)

    from_date = from_date.replace(hour=0, minute=0, second=0, microsecond=0)
    return {"from_date": from_date, "to_date": to_date}
