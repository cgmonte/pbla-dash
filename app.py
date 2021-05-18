import os
import logging

import dash  # pylint: disable=import-error
import dash_core_components as dcc  # pylint: disable=import-error
import dash_html_components as html  # pylint: disable=import-error

from vis import global_activity
from vis import alunos_vs_docs
# from vis import wordcloud
from vis import gateway

import base64
from dash.dependencies import Input, Output

# wc.get_plot()


image_filename = 'vis/wc_files/wc.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app = dash.Dash(__name__, serve_locally=False, url_base_pathname='/dash/')

server = app.server

tag_turma = 'GP0TGS20211'
tag_equipe = 'F4UL'

app.layout = html.Div(className='main-div', children=[
                dcc.Location(id='url', refresh=False),
                html.Div(className='first-row', children=[
                    html.Div(className='div1a', children=[
                        html.H5('Quantidade de interações de estudantes com documentos da equipe ao longo do tempo'),
                        html.Div(id='div_bubble')
                        ]),
                                    
                        html.Div(className='div1b', children=[
                            html.H5('Visualização Discord'),
                            html.Div(id='div_discord')
                            ]),
                ]
                ),
                html.Div(className='second-row', children=[
                    html.Div(className='div2a', children=[
                            html.H5('Estudantes vs. arquivos da turma'),
                            html.Div(id='subdiv_parcat')
                            ]),
                        # 1st column of 2nd row
                    html.Div(className='div2b', children=[
                            html.H5('Wordcloud'),
                            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),)
                            ])
                ]
                )
    ]
)


@ app.callback(dash.dependencies.Output('div_bubble', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_bubble(pathname):

    pathname=pathname[6:]
    tag_turma, tag_equipe=pathname.split('/')

    # print(tag_turma, tag_equipe, flush=True)

    return html.Div(children=[dcc.Graph(id='bubble', figure=global_activity.get_fig(
        tag_turma=tag_turma, tag_equipe=tag_equipe))])


@ app.callback(dash.dependencies.Output('subdiv_parcat', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_parcat(pathname):

    pathname=pathname[6:]
    tag_turma, tag_equipe=pathname.split('/')

    return html.Div(children=[dcc.Graph(id='parcat', figure=alunos_vs_docs.get_fig(
        tag_turma=tag_turma, tag_equipe=''))])

# @ app.callback(dash.dependencies.Output('p_sub', 'children'),
#               [dash.dependencies.Input('url', 'pathname')])
# def display_subtitle(pathname):

#     pathname=pathname[6:]
#     tag_turma, tag_equipe=pathname.split('/')

#     names=gateway.get_names(tag_turma=tag_turma, tag_equipe=tag_equipe)

#     disci=names['Disciplina']
#     sem=names['Semestre']
#     equipe=names['Equipe']

#     return html.P(f'Disciplina: {disci} | Semestre: {sem} | Equipe: {equipe}', id='sub')

if __name__ == '__main__':
    app.run_server(debug=True)

if __name__ != '__main__':
    gunicorn_logger=logging.getLogger('gunicorn.debug')
    app.logger.handlers=gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
