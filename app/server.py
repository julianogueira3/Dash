import dash
from layouts import app_layout
from callbacks import (
    update_velocity_chart,
    update_acceleration_chart,
    update_scatter_plot,
    update_video_current_time
)

app = dash.Dash(__name__)

app.layout = app_layout

app.callback(
    dash.dependencies.Output('velocity-chart-container', 'children'),
    [dash.dependencies.Input('player-dropdown', 'value')]
)(update_velocity_chart)

app.callback(
    dash.dependencies.Output('acceleration-chart-container', 'children'),
    [dash.dependencies.Input('player-dropdown', 'value')]
)(update_acceleration_chart)

app.callback(
    dash.dependencies.Output('scatter-plot-container', 'children'),
    [dash.dependencies.Input('player-dropdown', 'value')]
)(update_scatter_plot)

# Callback para atualizar o tempo atual do vídeo
app.callback(
    dash.dependencies.Output('video-current-time', 'children'),
    [dash.dependencies.Input('movie_player', 'currentTime')]
)(update_video_current_time)


if __name__ == '__main__':
    app.run_server(debug=True)
