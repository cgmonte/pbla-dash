import yaml
import requests

import sqlalchemy # pylint: disable=import-error
from sqlalchemy import create_engine # pylint: disable=import-error

import pandas as pd # pylint: disable=import-error
import plotly.express as px # pylint: disable=import-error
from vis import parsers, gateway

# display.max_rows and display.max_columns sets the maximum number of rows and columns displayed when a frame is pretty-printed. 
# Truncated lines are replaced by an ellipsis.
pd.set_option('display.max_rows', 10)

# open config file to get credentials and connect to DB
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

db_username = cfg['db_creds']['user']
db_pass = cfg['db_creds']['pass']
engine_gdrive_app_db = create_engine(f"postgresql://{db_username}:{db_pass}@pbla_db_1/db-micros-gdrive")
# engine_gdrive_app_db = create_engine(f"postgresql://{db_username}:{db_pass}@pbla_db_1/micros-gdrive-app")
# engine_gdrive_data_db = create_engine(f"postgresql://{db_username}:{db_pass}@pbla_db_1/micros-gdrive-data")

# # update user data
# url = "http://pbla_gdrive_1/api/integ/gdrive/user/update/records"
# payload = {'user_id': 1}
# post = requests.post(url, params=payload)
# print(post.text)

def get_fig(tag_turma: str, tag_equipe: str):

    # integrantes = gateway.get_integrantes(tag_equipe=tag_equipe)

    # for integrante in integrantes['user']:
    #     gateway.update_gdrive_records(integrante)
            
    conn = engine_gdrive_app_db.connect()
    where_conditions = parsers.where_conditions(integrantes)
    statement_b = sqlalchemy.text(f'SELECT * FROM "users" WHERE {where_conditions};')
    db_users = pd.read_sql_query(statement_b, con=conn)
    conn.close()
    engine_gdrive_app_db.dispose()
    
    conn = engine_gdrive_app_db.connect()
    statement_a = sqlalchemy.text(f"SELECT activity_fields FROM files_records WHERE tag_turma = \'{tag_turma}\' AND tag_equipe = \'{tag_equipe}\';")
    file_records = pd.read_sql_query(statement_a, con=conn)
    conn.close()
    engine_gdrive_app_db.dispose()
   
    df = pd.DataFrame()

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
                data = {'actor': event['actors'][0]['user']['knownUser']['personName'], 'event_date':event_date, 'event_type': event_type[0]}
                df = df.append(pd.DataFrame.from_dict([data]))

    df = df.sort_values(by='event_date')
    df = df.set_index('event_date')

    ##################### notebook 

    all_dates = []
    all_actors = []
    data = {}
    df4 = pd.DataFrame()
    total = 0

    for row in df.iterrows():
        all_dates.append(row[0])
        
    unique_dates = list(set(all_dates))
    unique_dates.sort()

    for date in unique_dates:
        df2 = df.loc[[date]] # we need to pass a list to make sure it returns a data frame
        if isinstance(df2, pd.core.frame.DataFrame):
            for row in df2.iterrows():
                all_actors.append(row[1]['actor'])
            unique_actors = list(set(all_actors))
            all_actors = []
        for actor in unique_actors:
            global_activity_data = {'event_date':date, 
            'actor': actor,
            'create': 0,
            'edit': 0,
            'move': 0,
            'rename': 0,
            'delete': 0,
            'restore': 0,
            'permissionChange': 0,
            'comment': 0,
            'dlpChange': 0,
            'reference': 0,
            'settingsChange': 0,
            'total': 0,
        }
            
            df3 = df2.loc[df2['actor'] == actor]
            info = df3['event_type'].value_counts()
            unique_event_types = info.axes[0].tolist()
            for event_type in unique_event_types:
                global_activity_data[event_type] = info.get(event_type, default=None)
                total = total + global_activity_data[event_type]
            global_activity_data['total'] = total
            total = 0
            df4 = df4.append(pd.DataFrame.from_dict([global_activity_data]))
    df4 = df4.loc[df4['event_date'] >= date.fromisoformat('2020-11-01')]
    df4 = df4.set_index('event_date')

    #######################3 notebooks

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
    label_map['actor'] = ''
    label_map['event_date'] = ''
    label_map['total'] = 'Interações totais (tamanho da circuferência)'

    # replaces google user identifiers with real names
    # it can only run once
    df4 = df4.loc[df4['actor'].isin(gdrive_people_field)]

    for person in gdrive_people_field:
        df4 = df4.replace(person, users[person])

    fig = px.scatter(df4, 
                 x=df4.index, 
                 y="actor", 
                 size="total", 
                 color="actor", 
                 labels=users, 
                 title="Contribuições a documentos da equipe ao longo do tempo",
                )
    fig.layout.update(showlegend=False)
    fig.update_yaxes(visible=True, showticklabels=True)
    fig.update_layout(
        margin=dict(l=0, t=26, b=0, r=0),
        title_font_family="Roboto",
        title_font_color="#01579B",
        font_size=10,
        paper_bgcolor="whitesmoke",
        autosize = True,
    )
    return fig