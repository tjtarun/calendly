import datetime


def str_time_to_time(time_str):
    return datetime.datetime.strptime(time_str, "%H:%M:%S").time()


def timestamp_to_datetime(datetime_ts):
    return datetime.datetime.fromtimestamp(datetime_ts)
