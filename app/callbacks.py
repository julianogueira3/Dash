# Callback para atualizar o mapa de dispersão com base no jogador selecionado
# def update_scatter_plot(player_column, campo_img=campo_img):
#     player_id = int(player_column[1])
#     x = df[f'j{player_id}_x'].values * campo_img.shape[1]
#     y = df[f'j{player_id}_y'].values * campo_img.shape[0]

#     # Plotar o mapa de dispersão
#     fig, ax = plt.subplots(figsize=(10, 6))
#     ax.imshow(campo_img)
#     sc = ax.scatter(x, y, c='red', alpha=0.5)
#     ax.set_xlim(0, campo_img.shape[1])
#     ax.set_ylim(0, campo_img.shape[0])
#     buf = BytesIO()
#     fig.savefig(buf, format='png')
#     buf.seek(0)
#     img_str = "data:image/png;base64," + base64.b64encode(buf.read()).decode('utf-8')

#     return html.Img(src=img_str, style={'width': '100%'})

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import math
import base64
import matplotlib.pyplot as plt
from io import BytesIO
import re

campo_img = plt.imread('/home/julia/Dash/app/imagens/campo_corte.jpg')
df = pd.read_csv('/home/julia/Dash/data/coords.csv')

def extract_xy(cell_value):
    if isinstance(cell_value, str):
        match = re.match(r'\(([^,]+),([^)]+)\)', cell_value)
        if match:
            return float(match.group(1)), float(match.group(2))
    return None, None

# Função para calcular a velocidade e aceleração do jogador
def calculate_velocity_and_acceleration(player_id):
    count = 0
    linhas = len(df)
    listavt = []
    listaa = []
    listatime = []
    x_prev, y_prev, t_prev = 0, 0, 0  # Inicialização das variáveis anteriores
    while count < linhas:
        x, y = extract_xy(df[f'p{player_id}'].iloc[count])  # Extrai os valores x e y da célula
        if x is not None and y is not None:
            t = df['t'].iloc[count]
            if count == 0:
                vx = 0
                vy = 0
                vt = 0
                a = 0
            else:
                vx = (x - x_prev) / (t - t_prev)
                vy = (y - y_prev) / (t - t_prev)
                vt = math.sqrt((vx ** 2) + (vy ** 2))
                a = vt / t
            count += 1
            x_prev, y_prev, t_prev = x, y, t
            listavt.append(vt)
            listaa.append(a)
            listatime.append(count)
        else:
            count += 1  # Incrementa o contador sem calcular a velocidade e aceleração para este ponto

    return listatime, listavt, listaa

# Callback para atualizar o gráfico de velocidade com base no jogador selecionado
def update_velocity_chart(player_column):
    player_id = f"{int(player_column[1]):02d}"  # Formatando para dois dígitos com zero à esquerda
    tempo, velocidade, _ = calculate_velocity_and_acceleration(player_id)

    # Plotar o gráfico de velocidade
    velocity_fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(tempo, velocidade)
    ax.set_xlabel('Tempo')
    ax.set_ylabel('Velocidade')
    ax.set_title('Gráfico de Velocidade')
    velocity_buf = BytesIO()
    velocity_fig.savefig(velocity_buf, format='png')
    velocity_buf.seek(0)
    velocity_img_str = "data:image/png;base64," + base64.b64encode(velocity_buf.read()).decode('utf-8')
    velocity_chart = html.Img(src=velocity_img_str, style={'width': '100%'})

    return velocity_chart

# Callback para atualizar o gráfico de aceleração com base no jogador selecionado
def update_acceleration_chart(player_column):
    player_id = f"{int(player_column[1]):02d}"  # Formatando para dois dígitos com zero à esquerda
    tempo, _, aceleracao = calculate_velocity_and_acceleration(player_id)

    # Plotar o gráfico de aceleração
    acceleration_fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(tempo, aceleracao)
    ax.set_xlabel('Tempo')
    ax.set_ylabel('Aceleração')
    ax.set_title('Gráfico de Aceleração')
    acceleration_buf = BytesIO()
    acceleration_fig.savefig(acceleration_buf, format='png')
    acceleration_buf.seek(0)
    acceleration_img_str = "data:image/png;base64," + base64.b64encode(acceleration_buf.read()).decode('utf-8')
    acceleration_chart = html.Img(src=acceleration_img_str, style={'width': '100%'})

    return acceleration_chart

# Callback para atualizar o mapa de dispersão com base no jogador selecionado
def update_scatter_plot(player_column, campo_img=campo_img):
    player_id = f"{int(player_column[1]):02d}"  # Formatando para dois dígitos com zero à esquerda
    x = []
    y = []
    for cell_value in df[f'p{player_id}']:
        x_val, y_val = extract_xy(cell_value)
        if x_val is not None and y_val is not None:
            x.append(x_val)
            y.append(y_val)
    # print("Lista x:", x)
    # print("Lista y:", y)
    # Plotar o mapa de dispersão
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(campo_img)
    ax.scatter(x, y, c='red', alpha=0.5)
    
    # Ajustar os limites dos eixos x e y de acordo com as dimensões do campo de imagem
    ax.set_xlim(0, campo_img.shape[1])
    ax.set_ylim(0, campo_img.shape[0])
    
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_str = "data:image/png;base64," + base64.b64encode(buf.read()).decode('utf-8')

    return html.Img(src=img_str, style={'width': '100%'})

def update_video_current_time(current_time):
    if current_time is not None:
        formatted_time = "{:02}:{:02}".format(int(current_time / 60), int(current_time % 60))
        return f"Tempo Atual: {formatted_time}"
    else:
        return "Tempo Atual: --:--"  # ou qualquer outra mensagem que você queira exibir quando o tempo atual não estiver disponível


