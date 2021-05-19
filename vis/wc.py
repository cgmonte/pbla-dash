import pandas as pd
import sqlalchemy 
import matplotlib.pyplot as plt
import yaml
import unidecode
import os
from sqlalchemy import create_engine
import textract
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import requests

# pd.set_option('display.max_rows', None)
plt.close("all")

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
db_username = cfg['db_creds']['user']
db_pass = cfg['db_creds']['pass']

engine_gdrive_app_db = create_engine(f"postgresql://{db_username}:{db_pass}@pbla_db_1/micros-gdrive-app")
engine_gdrive_data_db = create_engine(f"postgresql://{db_username}:{db_pass}@pbla_db_1/micros-gdrive-data")

# url = "http://pbla_gdrive_1/api/integ/gdrive/user/update/records"
# payload = {'user_id': 1}
# post = requests.post(url, params=payload)
# print(post.text)

# def get_extension(original_mimetype: str):

#     mimetypes = {'application/vnd.google-apps.document': '.docx', 
#                 'application/vnd.google-apps.spreadsheet': '.xlsx', 
#                 'application/vnd.google-apps.presentation': '.pptx'}

#     if original_mimetype in mimetypes:
#         converted_mimetype = mimetypes[f'{original_mimetype}']
#         return converted_mimetype

#     return False

def get_plot():
#     statement = sqlalchemy.text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
#     tables = pd.read_sql_query(statement, con=engine_gdrive_data_db)
#     df = pd.DataFrame()
#     columns = ['actor','timestamp','date']
#     df2 = pd.DataFrame()
#     index = 0
#     for row in tables.iterrows():
#         tablename = row[1][0]
#         statement = sqlalchemy.text(f"SELECT activity_fields FROM \"{tablename}\"")
#         activity = pd.read_sql_query(statement, con=engine_gdrive_data_db)
        
#         statement = sqlalchemy.text(f'SELECT * FROM \"{tablename}\" ORDER BY sequencial DESC LIMIT 1;')
#         latest = pd.read_sql_query(statement, con=engine_gdrive_data_db)

#         if not latest.empty:
#             for row in latest.iterrows():
#                 metadata = latest.at[row[0],"file_fields"]
#                 if get_extension(original_mimetype=metadata['mimeType']) != False:
#                     ext = get_extension(original_mimetype=metadata['mimeType'])
#                     name = metadata['name'] + ext
#                     file_name = name.replace(" ", "_")
#                     file_name = unidecode.unidecode(file_name)
                    
#                     file_data = latest.at[row[0],"file_revision"]
#                     if not os.path.isdir('vis/wc_files/tmp'):
#                         os.mkdir('vis/wc_files/tmp')
#                     fh = open('vis/wc_files/tmp/'+file_name, "wb")
#                     fh.write(file_data)
#                     fh.close
#     tmp_list = os.listdir('vis/wc_files/tmp')
#     # print(tmp_list)
#     # acessar arquivos na pasta tmp, extrair texto e acrescenta-lo a um novo arquivo
#     # print("aaaaaaaaaaaaaaaaaaqui é:", len(tmp_list))
#     for f in tmp_list:
#         # tem que checar, senão se for um diretório, dá erro o textract
#         if os.path.isfile(f'vis/wc_files/tmp/{f}'):
#             # print(f)
#             # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQUII")
#             text = textract.process('vis/wc_files/tmp/'+f).decode("utf8")
#             af = open('vis/wc_files/all895897348956.txt','a')
#             af.write(text)
#             af.close

    # composição de um set de stopwords que serão retiradas da wordcloud final
    stopwords_pt = []
    with open('vis/wc_files/stopwords.txt','r') as f:
        text = f.read()
        text = text.split()
    for word in text:
        stopwords_pt.append(word)
    stopwords_pt = set(stopwords_pt)

    with open('vis/wc_files/all895897348956.txt','r') as f:
        wordcloud = WordCloud(stopwords=stopwords_pt, width=800, height=450, max_font_size=150, background_color="whitesmoke").generate(f.read())
        wordcloud.to_file("vis/wc_files/wc.png")
    # plt.figure(figsize=(30,10))
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    # plt.show()

# get_plot()