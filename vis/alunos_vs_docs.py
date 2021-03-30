import pandas as pd
import sqlalchemy 
from sqlalchemy import create_engine
# import openpyxl
# import matplotlib.pyplot as plt
from datetime import date, datetime
import yaml
# import re
import requests

# import chart_studio.plotly as charsplot
# import plotly.figure_factory as pff
# from plotly.offline import iplot
import plotly.express as px

# pd.set_option('display.max_rows', None)
# plt.close("all")

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
db_username = cfg['db_creds']['user']
db_pass = cfg['db_creds']['pass']

engine_gdrive_app_db = create_engine(f"postgresql://{db_username}:{db_pass}@pbla_db_1/micros-gdrive-app")
engine_gdrive_data_db = create_engine(f"postgresql://{db_username}:{db_pass}@pbla_db_1/micros-gdrive-data")

############ notebook

turma_to_analyse = 'REQ1001'

def get_files_from_turma(turma_tag: str):
    turma_files = dict()
    turma_file_list = []
    statement = sqlalchemy.text(f'SELECT * FROM "file_turma_association"')
    db_file_turmas = pd.read_sql_query(statement, con=engine_gdrive_app_db)
    for row in db_file_turmas.iterrows():
        if row[1]['pblacore_tag_turma'] == turma_tag:
            turma_file_list.append(row[1]['local_fileid'])
            turma_files[turma_tag] = turma_file_list
    return turma_file_list



def get_fig():
    files_turma = get_files_from_turma(turma_to_analyse)

    statement = sqlalchemy.text(f'SELECT * FROM "users"')
    db_users = pd.read_sql_query(statement, con=engine_gdrive_app_db)

    statement = sqlalchemy.text(f'SELECT * FROM "turmas"')
    db_turmas = pd.read_sql_query(statement, con=engine_gdrive_app_db)


    # display(tables)
    # statement = sqlalchemy.text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
    # tables = pd.read_sql_query(statement, con=engine_gdrive_data_db)
    # tables = tables.loc[tables['tablename'].isin(files_turma)]

    columns = ['actor','timestamp','date']
    df = pd.DataFrame()
    name_vs_id = dict()

    # loop through table names
    for row in files_turma:
        tablename = row
    
        statement = sqlalchemy.text(f'SELECT * FROM \"{tablename}\" ORDER BY sequencial DESC LIMIT 1;')
        latest = pd.read_sql_query(statement, con=engine_gdrive_data_db)
        if not latest.empty:
            for row in latest.iterrows():
                metadata = latest.at[row[0],"file_fields"]
                id = metadata['id']
                name = metadata['name']
                name_vs_id[id] = name
    #             print(name_vs_id)

        statement = sqlalchemy.text(f"SELECT activity_fields FROM \"{tablename}\"")
        file_records = pd.read_sql_query(statement, con=engine_gdrive_data_db) # get file records
        rows_count = len(file_records.index) 
        if not file_records.empty:
            # loop through file records, get the field 'activity' for each record
            for row in file_records.iterrows():
                activity_fields = file_records.at[row[0],"activity_fields"]
                #loop through a list of events (serveral primaryActionDetail)
                for event in activity_fields:
                    event_date = datetime.strptime(event['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
                    event_date = event_date.date()
    #                 print(type(date))
                    event_type = event['actions'][0]['detail']
                    event_type = list(event_type.keys())
                    event_target = event['targets'][0]['driveItem']['name'][6:]
                    data = {'actor': event['actors'][0]['user']['knownUser']['personName'], 
                            'target': event_target}
                    df = df.append(pd.DataFrame.from_dict([data]))

    df = df.sort_values(by='actor')
    # display(df)

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
                                width=400,
                                labels={'actor': 'Estudantes', 'target': 'Arquivo'},
                                title=f"Turma {turma_to_analyse}: Estudantes vs. contribuições em arquivos da disciplina")
    fig.layout.update(showlegend=False, hovermode='closest', width=400)
    return fig