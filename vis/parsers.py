from datetime import date, datetime

def timestamp_parser(timestamp):
    if timestamp[19:][:1] == '.':
        event_date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    elif timestamp[19:][:1] == 'Z':
        event_date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    return event_date