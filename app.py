import os
import logging

import dash
import dash_core_components as dcc
import dash_html_components as html

from vis import global_activity
from vis import alunos_vs_docs
# from vis import wordcloud

import base64

# wc.get_plot()

image_filename = 'vis/wc_files/wc.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, serve_locally = False, external_stylesheets=external_stylesheets, url_base_pathname='/dash/')

server = app.server

app.layout = html.Div([
    html.H2('Dashboard PBL Analytics'),
    # dcc.Dropdown(
    #     id='dropdown',
    #     options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
    #     value='LA'
    # ),
    # html.Div(id='display-value'),
    html.Div(dcc.Graph(id='bubble', figure=global_activity.get_fig())),
    html.Div(dcc.Graph(style={'width': '50%'},id='parcat', figure=alunos_vs_docs.get_fig())),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),height=400,
                sizes='(max-height: 100px) 100x, 100px")', 
                title='Nuvem de palavras')])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
    # return  {'data':[]}

if __name__ == '__main__':
    app.run_server(debug=True)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.debug')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)