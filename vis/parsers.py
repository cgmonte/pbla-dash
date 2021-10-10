from datetime import date, datetime

def timestamp_parser(timestamp):
    # print('         timestamp:', timestamp, type(timestamp), flush=True)
    if timestamp[19:][:1] == '.':
        event_date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    elif timestamp[19:][:1] == 'Z':
        event_date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    # print('         event_date:', event_date, type(event_date), flush=True)
    return event_date

# função usada para formatar uma string que será 
def where_conditions(integrantes: dict):
    # print('         integrantes', integrantes)
    if len(integrantes['user']) > 1:
        where_conditions = str()
        for i, integrante in enumerate(integrantes['user']):
            # print("         index is:", i, "          integrante is:", integrante, flush=True)
            if i < (len(integrantes['user']) - 1):
                new_condition = f' pbla_uid = {integrante} OR'
                where_conditions = where_conditions + new_condition
            else:
                new_condition = f' pbla_uid = {integrante}'
                where_conditions = where_conditions + new_condition
    # print('         where_conditions', where_conditions, flush=True)
    return where_conditions