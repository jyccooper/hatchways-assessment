from datetime import datetime
from dateutil.relativedelta import relativedelta

DAILY = "daily"
MONTHLY = "monthly"
YEARLY = "yearly"


def resolve_date_range(frame, date_range):
    """
    Calculate date range based on time frame and range parameters
    
    Args:
        frame (str): Time frame ('daily', 'monthly', 'yearly')
        date_range (int): Number of time periods to include
        
    Returns:
        dict: {'from_date': datetime, 'to_date': datetime}
    """
    today = datetime.now()
    from_date = today
    
    # Convert to integer and ensure positive value
    try:
        date_range = max(1, int(date_range))
    except (ValueError, TypeError):
        date_range = 1
    
    # Calculate start date based on frame
    if frame == DAILY:
        from_date = today - relativedelta(days=date_range-1)
    elif frame == MONTHLY:
        from_date = today - relativedelta(months=date_range-1)
        # Ensure we start from first day of month for monthly ranges
        from_date = from_date.replace(day=1)
    elif frame == YEARLY:
        from_date = today - relativedelta(years=date_range-1)
        # Ensure we start from first day of year for yearly ranges
        from_date = from_date.replace(month=1, day=1)
    
    # Normalize time components to start of day
    from_date = from_date.replace(
        hour=0, 
        minute=0, 
        second=0, 
        microsecond=0
    )
    to_date = today.replace(
        hour=23,
        minute=59,
        second=59,
        microsecond=999999
    )
    
    return {
        "from_date": from_date,
        "to_date": to_date
    }