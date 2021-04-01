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

external_stylesheets = ['app.css']

app = dash.Dash(__name__, serve_locally = False, external_stylesheets=external_stylesheets, url_base_pathname='/dash/')

server = app.server

# page layout
# app.layout = html.Div(className='maindiv')

app.layout = html.Div(
    style={
        'display': 'flex',
        'flex-wrap': 'wrap',
        'justify-content': 'space-between',
        'align-content': 'stretch',
        'padding-left': '5%', 'padding-right': '5%'
        }, children=[
    html.H2('Dashboard PBL Analytics'),
    # first row
    html.Div(style={'width':'100%', 'margin-bottom': '10px'},
    children=[html.H6('Quantidade de interações de estudantes com documentos da equipe ao longo do tempo'),

        html.Div(children=[dcc.Graph(id='bubble', figure=global_activity.get_fig())]),

    ]),
    
    # second row
    html.Div(style={'width':'100%',
                    'display': 'flex',
                    'flex-wrap': 'wrap',
                    'flex-direction': 'row',
                    },
    children=[
        # first column of first row
        html.Div(style={'width': '60%', 
                        'height': '100px',
                        'flex': 'flex-shrink',},
                children=[html.H6('Estudantes vs. arquivos da turma'),dcc.Graph(id='parcat', figure=alunos_vs_docs.get_fig('REQ1001'))]),

        # second column of first row
        html.Div(style={'width': '40%',
                    'display': 'flex',
                    'flex-wrap': 'wrap',
                    'flex-direction': 'column',
                    'flex': 'auto'},
                children=[html.H6('Wordcloud'),html.Img(style={'width': '100%', 'height': 'auto'}, src='data:image/png;base64,{}'.format(encoded_image.decode()),),])
    ])
])

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
