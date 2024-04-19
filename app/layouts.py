import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_player


external_stylesheets = ['../style.css']

app = dash.Dash(__name__)

app_layout = html.Div([
    html.H1("Dashboard de Futebol"),

    html.Div([
        html.Div([
            dcc.RadioItems(
                id='team-selection',
                options=[
                    {'label': 'Time 1', 'value': 'team1'},
                    {'label': 'Time 2', 'value': 'team2'}
                ],
                value='team1',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '33%', 'float': 'left', 'text-align': 'center'}),

        html.Div([
            dcc.Dropdown(
                id='player-dropdown',
                options=[
                    {'label': f'Jogador {i+1}', 'value': f'p{i+1}'} for i in range(96)
                ],
                value='p1',
                style={'width': '150px', 'margin': 'auto'}
            )
        ], style={'width': '33%', 'float': 'left'}),

        html.Div([
            dcc.Input(
                id='video-input',
                type='text',
                placeholder='Insira o link do vídeo',
                style={'width': '100%'}
            )
        ], style={'width': '33%', 'float': 'right'})
    ], style={'clear': 'both', 'margin-bottom': '20px', 'margin-top': '20px', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),

    html.Div([
        # Vídeo e Gráfico de Velocidade
        html.Div([
            html.Div([
                dash_player.DashPlayer(
                    id='movie_player',
                    url=dash.get_asset_url('video_cortado_720p.mp4'),
                    controls=True,
                    style={'width': '100%', 'height': '100%', 'object-fit': 'contain'}
                ),
                html.Div([
                    html.Span(id='video-current-time')
                ], style={'text-align': 'center', 'margin-top': '10px'})
                
            ], style={'width': '50%', 'float': 'left'}),

            html.Div([
                # Gráfico de velocidade
                html.Div(id='velocity-chart-container', style={'width': '100%'})
            ], style={'width': '50%', 'float': 'left'})
        ], style={'clear': 'both'}),

        # Mapa de dispersão e Gráfico de Aceleração
        html.Div([
            html.Div([
                # Mapa de dispersão
                html.Div(id='scatter-plot-container', style={'width': '100%'})
            ], style={'width': '50%', 'float': 'left'}),

            html.Div([
                # Gráfico de aceleração
                html.Div(id='acceleration-chart-container', style={'width': '100%'})
            ], style={'width': '50%', 'float': 'left'})
        ], style={'clear': 'both'})
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)