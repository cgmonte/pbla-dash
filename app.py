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

app = dash.Dash(__name__, serve_locally = False, url_base_pathname='/dash/')

server = app.server

app.layout = html.Div(className='main-div',
    children=[
        html.H1('Dashboard PBL Analytics'),
        # first row
        html.Div(className='first-row',
                children=[
                    html.H4('Quantidade de interações de estudantes com documentos da equipe ao longo do tempo'),
                    html.Div(children=[dcc.Graph(id='bubble', figure=global_activity.get_fig())]),
                ]
        ),
        # second row
        html.Div(className='second-row',
                children=[
                    # 1st column of 2nd row
                    html.Div(className='first-col',
                            children=[
                                html.H4('Estudantes vs. arquivos da turma'),
                                dcc.Graph(id='parcat', figure=alunos_vs_docs.get_fig('REQ1001'))]),
                    # 1st column of 2nd row
                    html.Div(className='second-col',
                            children=[
                                html.H4('Wordcloud'),
                                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),)])
                ]
        )
    ]
)

# @app.callback(dash.dependencies.Output('display-value', 'children'),
#               [dash.dependencies.Input('dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)
#     # return  {'data':[]}

if __name__ == '__main__':
    app.run_server(debug=True)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.debug')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)