import yaml
import requests

import sqlalchemy
from sqlalchemy import create_engine

import pandas as pd
import plotly.express as px

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
    
db_username = cfg['db_creds']['user']
db_pass = cfg['db_creds']['pass']
engine_gdrive_app_db = create_engine(f"postgresql://{db_username}:{db_pass}@pbla_db_1/db-micros-discord")

connection = engine_gdrive_app_db.connect()

def get_fig():
    statement = sqlalchemy.text(f"SELECT * FROM discord_message_log")
    messages = pd.read_sql_query(statement, con=connection)
    contagem = messages['author'].value_counts()
    # print(contagem, flush=True)
    fig = px.bar(contagem,
                 labels={'value': 'Mensagens', 'index': 'Estudante'},
                 title=f"Quantidade de mensagens enviadas no Discord",
                 color=contagem.index,
                )
    
    fig.update_layout(
        margin=dict(t=35, r=0, b=10),
        title_font_family="Roboto",
        title_font_color="#01579B",
        paper_bgcolor="whitesmoke",
        autosize = True,
        showlegend = False,
        title_font_size=14,
    )

    return fig