import pandas as pd
import sqlalchemy 
import matplotlib.pyplot as plt
import yaml
from sqlalchemy import create_engine
from wordcloud import WordCloud
import base64

plt.close("all")

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
db_username = cfg['db_creds']['user']
db_pass = cfg['db_creds']['pass']

engine_gdrive_app_db = create_engine(f"postgresql://{db_username}:{db_pass}@pbla_db_1/db-micros-discord")

connection = engine_gdrive_app_db.connect()

def get_fig():
    statement = sqlalchemy.text(f"SELECT * FROM discord_message_log")
    messages = pd.read_sql_query(statement, con=connection)

    new_words_list = ' '.join([i for i in messages['message']]).split()
    new_words_list_string =(" ").join(new_words_list)

    stopwords_pt = []
    with open('vis/wc_files/stopwords.txt','r') as f:
        text = f.read()
        text = text.split()
    for word in text:
        stopwords_pt.append(word)
    stopwords_pt = set(stopwords_pt)

    wordcloud = WordCloud(stopwords=stopwords_pt, width=800, height=450, max_font_size=150, background_color="whitesmoke")
    wordcloud.generate(new_words_list_string)
    wordcloud.to_file("vis/wc_files/wc.png")
    
    # plt.figure(figsize=(30,10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    
    image_filename = 'vis/wc_files/wc.png'
    return base64.b64encode(open(image_filename, 'rb').read())