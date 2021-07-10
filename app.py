import logging

import dash  # pylint: disable=import-error
import dash_core_components as dcc  # pylint: disable=import-error
import dash_html_components as html  # pylint: disable=import-error

from vis import global_activity, discord_qtde, alunos_vs_docs
from vis import wc

app = dash.Dash(__name__, serve_locally=False, url_base_pathname='/dash/')

server = app.server

external_css = ["https://fonts.googleapis.com/css?family=Roboto|Lato",]

for css in external_css:
    app.css.append_css({"external_url": css})

app.layout = html.Div(className='main-div', children=[
    dcc.Location(id='url', refresh=False),
    html.Div(className='first-row', children=[

        html.Div(className='div1a', children=[
            dcc.Loading(
                html.Div(id='div_bubble'))
        ]),

        html.Div(className='div2a', children=[
            dcc.Loading(
                html.Div(id='subdiv_parcat'))
        ]),

        html.Div(className='div2b', children=[
            dcc.Loading(
                html.Div(id='div_discord_count'))
        ]),

        html.Div(className='div1b', children=[
            dcc.Loading(
                html.Div(children=[
                    html.P('Nuvem de palavras de mensagens do Discord', className="native_title_fake"),
                    html.Img(src='data:image/png;base64,{}'.format(wc.get_fig().decode()),)
                ])
            )
        ])
    ])
])


@ app.callback(dash.dependencies.Output('div_bubble', 'children'),
             [dash.dependencies.Input('url', 'pathname')])
def display_bubble(pathname):
    pathname = pathname[6:]
    tag_turma, tag_equipe = pathname.split('/')
    return html.Div(className="return_div", children=[dcc.Graph(
        style={'width': '100%', 'height': '100%'}, 
        config={'responsive': True}, 
        responsive='auto', 
        id='bubble', 
        figure=global_activity.get_fig(tag_turma=tag_turma, tag_equipe=tag_equipe)
        )])


@ app.callback(dash.dependencies.Output('subdiv_parcat', 'children'),
             [dash.dependencies.Input('url', 'pathname')])
def display_parcat(pathname):
    pathname = pathname[6:]
    tag_turma, tag_equipe = pathname.split('/')
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