from datetime import date, datetime

def timestamp_parser(timestamp):
    if timestamp[19:][:1] == '.':
        event_date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    elif timestamp[19:][:1] == 'Z':
        event_date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    return event_date

def where_conditions(integrantes: dict):
    if len(integrantes['user']) > 1:
        where_conditions = str()
        for i, integrante in enumerate(integrantes['user']):
            # print("         index is:", i, "          integrante is:", integrante)
            if i < (len(integrantes['user']) - 1):
                new_condition = f' pbla_uid = {integrante} OR'
                where_conditions = where_conditions + new_condition
            else:
                new_condition = f' pbla_uid = {integrante}'
                where_conditions = where_conditions + new_condition
    return where_conditions