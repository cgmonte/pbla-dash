import os
import logging

import dash  # pylint: disable=import-error
import dash_core_components as dcc  # pylint: disable=import-error
import dash_html_components as html  # pylint: disable=import-error

from vis import global_activity, discord_qtde, alunos_vs_docs
from vis import wc
from vis import gateway

import base64
# from dash.dependencies import Input, Output, State
import json



image_filename = 'vis/wc_files/wc.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app = dash.Dash(__name__, serve_locally=False, url_base_pathname='/dash/')

server = app.server

external_css = [
    "https://fonts.googleapis.com/css?family=Roboto|Lato",
]

for css in external_css:
    app.css.append_css({"external_url": css})

app.layout = html.Div(className='main-div', children=[
    dcc.Location(id='url', refresh=False),
    # html.Div(id='pseudo_div'),
    # dcc.Store(id='preload-state'),
    html.Div(className='first-row', children=[
        html.Div(className='div1a', children=[
            html.Div(id='div_bubble')
        ]),

        html.Div(className='div2a', children=[
            # html.H5('Estudantes vs. arquivos da turma'),
            html.Div(id='subdiv_parcat')
        ]),
        html.Div(className='div2b', children=[html.Div(id='div_discord_count'),
            # html.H5('Wordcloud'),
        ]),
        html.Div(className='div1b', children=[
            html.P('Nuvem de palavras de mensagens do Discord', className="native_title_fake"),
            html.Img(
                src='data:image/png;base64,{}'.format(encoded_image.decode()),),
            # html.Div(wc.get_fig())
        ])
    ]
    )
]
)

# @app.callback(dash.dependencies.Output('preload-state', 'data'), 
#              [dash.dependencies.Input('url', 'pathname')])
# def update_data(pathname):
#     state_dict = dict()

#     pathname = pathname[6:]
#     tag_turma, tag_equipe = pathname.split('/')

#     integrantes = gateway.get_integrantes(tag_equipe=tag_equipe)
    
#     # some expensive clean data step    
#     integrantes = gateway.get_integrantes(tag_equipe=tag_equipe)
#     for integrante in integrantes['user']:
#         print("                       integrante:", integrante, flush=True)
#         gateway.update_gdrive_records(integrante)

#     state_dict['tag_turma'] = tag_turma
#     state_dict['tag_equipe'] = tag_equipe
#     state_dict['uptodate'] = True

#      # more generally, this line would be
#      # json.dumps(cleaned_df)
#     return json.dumps(state_dict)

# @ app.callback(dash.dependencies.Output('pseudo_div', 'children'),
#                [dash.dependencies.Input('url', 'pathname')])
# def update_records(pathname):

#     pathname = pathname[6:]
#     tag_turma, tag_equipe = pathname.split('/')

#     integrantes = gateway.get_integrantes(tag_equipe=tag_equipe)

#     # for integrante in integrantes['user']:
#     #     print("                       integrante:", integrante, flush=True)
#     #     gateway.update_gdrive_records(integrante)

#     return html.Div()


@ app.callback(dash.dependencies.Output('div_bubble', 'children'),
             [dash.dependencies.Input('url', 'pathname')])
            #    [dash.dependencies.Input('preload-state', 'state_data')])
def display_bubble(pathname):

    pathname = pathname[6:]
    tag_turma, tag_equipe = pathname.split('/')

    # print(tag_turma, tag_equipe, flush=True)

    # state_data = json.loads(state_data)
    # tag_turma = state_data['tag_turma']
    # tag_equipe = state_data['tag_equipe']
    # state_dict = state_data['state_dict']

    return html.Div(className="return_div", children=[dcc.Graph(
        style={'width': '100%', 'height': '100%'}, 
        config={'responsive': True}, 
        responsive='auto', 
        id='bubble', 
        figure=global_activity.get_fig(tag_turma=tag_turma, tag_equipe=tag_equipe)
        )])


@ app.callback(dash.dependencies.Output('subdiv_parcat', 'children'),
             [dash.dependencies.Input('url', 'pathname')])
            #    [dash.dependencies.Input('preload_state', 'state_data')])
def display_parcat(pathname):

    pathname = pathname[6:]
    tag_turma, tag_equipe = pathname.split('/')

    # print("app.py", tag_turma, tag_equipe)


    # state_data = json.loads(state_data)
    # tag_turma = state_data['tag_turma']
    # tag_equipe = state_data['tag_equipe']
    # state_dict = state_data['state_dict']

    return html.Div(className="return_div", children=[dcc.Graph(
        style={'width': '100%', 'height': '100%'}, 
        config={'responsive': True}, 
        responsive='auto', 
        id='parcat', 
        figure=alunos_vs_docs.get_fig(tag_turma=tag_turma, tag_equipe=tag_equipe)
        )])
    

@ app.callback(dash.dependencies.Output('div_discord_count', 'children'),
               [dash.dependencies.Input('url', 'pathname')])
def display_discord_bars(pathname):

    pathname = pathname[6:]
    tag_turma, tag_equipe = pathname.split('/')

    # print(tag_turma, tag_equipe, flush=True)

    return html.Div(className="return_div", children=[dcc.Graph(
            style={'width': '100%', 'height': '100%'}, 
            config={'responsive': True}, 
            responsive='auto', id='parcat', 
            figure=discord_qtde.get_fig())])


if __name__ == '__main__':
    app.run_server(debug=True)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.debug')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)