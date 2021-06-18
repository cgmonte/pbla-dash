import pandas as pd # pylint: disable=import-error
import sqlalchemy # pylint: disable=import-error
from sqlalchemy import create_engine # pylint: disable=import-error

from datetime import date, datetime 
import yaml
import requests
from vis import parsers

import plotly.express as px # pylint: disable=import-error

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
db_username = cfg['db_creds']['user']
db_pass = cfg['db_creds']['pass']

engine_gdrive_app_db = create_engine(f"postgresql://{db_username}:{db_pass}@pbla_db_1/db-micros-gdrive")


def get_files_from_equipe(tag_equipe: str):

    conn = engine_gdrive_app_db.connect()
    statement_a = sqlalchemy.text(f"SELECT driveapi_fileid FROM files_records WHERE tag_equipe = \'{tag_equipe}\';")
    file_records = pd.read_sql_query(statement_a, con=conn)
    conn.close()
    engine_gdrive_app_db.dispose()

    equipe_file_set = set()
    
    for row in file_records.iterrows():

        equipe_file_set.add(row[1]['driveapi_fileid'])

    return equipe_file_set

def get_files_from_turma(tag_turma: str):

    conn = engine_gdrive_app_db.connect()
    statement_a = sqlalchemy.text(f"SELECT driveapi_fileid FROM files_records WHERE tag_turma = \'{tag_turma}\';")
    file_records = pd.read_sql_query(statement_a, con=conn)
    conn.close()
    engine_gdrive_app_db.dispose()

    turma_file_set = set()
    
    for row in file_records.iterrows():

        turma_file_set.add(row[1]['driveapi_fileid'])

    return turma_file_set


def get_fig(tag_turma: str, tag_equipe: str):
    files_turma = get_files_from_turma(tag_turma=tag_turma)

    statement = sqlalchemy.text(f'SELECT * FROM "users"')
    db_users = pd.read_sql_query(statement, con=engine_gdrive_app_db)

    df = pd.DataFrame()
    name_vs_id = dict()

    for file in files_turma:

        statement = sqlalchemy.text(f'SELECT file_fields FROM files_records WHERE driveapi_fileid = \'{file}\' ORDER BY sequencial DESC LIMIT 1;')
        latest = pd.read_sql_query(statement, con=engine_gdrive_app_db)
        if not latest.empty:
            for row in latest.iterrows():
                # print(row)
                metadata = latest.at[row[0],"file_fields"]
                id = metadata['id']
                name = metadata['name']
                name_vs_id[id] = name
            # print (name_vs_id, flush=True)

        statement = sqlalchemy.text(f"SELECT activity_fields FROM files_records WHERE driveapi_fileid = \'{file}\';")
        file_records = pd.read_sql_query(statement, con=engine_gdrive_app_db) # get file records

        if not file_records.empty:
            # loop through file records, get the field 'activity' for each record

            for row in file_records.iterrows():

                activity_fields = file_records.at[row[0],"activity_fields"]

                #loop through a list of events (serveral primaryActionDetail)
                for event in activity_fields:
                    event_date = parsers.timestamp_parser(event['timestamp'])
                    event_date = event_date.date()
                    event_type = event['actions'][0]['detail']
                    event_type = list(event_type.keys())

                    if 'driveItem' in event['targets'][0]:
                        event_target = event['targets'][0]['driveItem']['name'][6:]
                        # print("DDDDDDDDDDDDDDDDDDDDDDDDDDD driveItem", event_target, flush=True)
                    elif 'fileComment' in event['targets'][0]:
                        event_target = event['targets'][0]['fileComment']['parent']['name'][6:]
                        # print("FFFFFFFFFFFFFFFFFFFFFFFFFFF fileComment", event_target, flush=True)
                    
                    data = {'actor': event['actors'][0]['user']['knownUser']['personName'], 
                            'target': event_target}
                    df = df.append(pd.DataFrame.from_dict([data]))

    df = df.sort_values(by='actor')

    users = dict()
    for row in db_users.iterrows():
        users[row[1]['driveapi_account_id']] = row[1]['driveapi_name']
        
    gdrive_people_field = []
    for key in users:
        if key != None:
            gdrive_people_field.append(key)
            name = users[key]
            name = name.split(' ')[0] + " " + name.split(' ')[1][:1] + "."
            users[key] = name
    label_map = users
    label_map['actor'] = 'Estudante'
    label_map['event_date'] = 'Data das interações'
    label_map['total'] = 'Interações totais (tamanho da circuferência)'

    # it can only run once
    df = df.loc[df['actor'].isin(gdrive_people_field)]

    # replaces google user identifiers with real names
    for person in gdrive_people_field:
        df = df.replace(person, users[person])
        
    # replaces google file ids with file names
    for file_id in name_vs_id:
        df = df.replace(file_id, name_vs_id[file_id])

    # display(px.colors.qualitative.Antique)
    fig = px.parallel_categories(df,
                                width=None,
                                labels={'actor': 'Estudantes', 'target': 'Documentos'},
                                title=f"Estudantes vs. documentos da disciplina",
                                )
    fig.layout.update(showlegend=False, hovermode='closest', margin=dict(r=210))
    fig.update_yaxes(automargin=True)

    fig.update_layout(
        margin=dict(l=30, t=40, b=10, r=150),
        title_font_family="Roboto",
        title_font_color="#01579B",
        # font_size=10,
        paper_bgcolor="whitesmoke",
        autosize = True,
    )

    return fig
    # return tag_turma