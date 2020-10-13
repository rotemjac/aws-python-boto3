import datetime

def get_time_diff(time_to_compare):

    time_to_compare = time_to_compare[0]

    if isinstance(time_to_compare, datetime.date):
        timezone = time_to_compare.tzinfo
        current_time = datetime.datetime.now(timezone)
        time_interval = current_time - time_to_compare
        return time_interval

    return 'None'