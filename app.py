

import streamlit as st
import pandas as pd
import plotly.express as px

from mplsoccer import Radar, FontManager, grid
import matplotlib.pyplot as plt

# Leer los datos
df = pd.read_excel("Jugadores de Colombia.xlsx")

with st.sidebar:
  st.write("Filtros")
  League = st.multiselect("Liga", sorted(df["Ligas"].unique()))
  Player = st.multiselect("Jugador", sorted(df["Colombian Players"].unique()))
  Position = st.multiselect("Posicion", sorted(df["Posicion"].unique()))

def filter_data(df, League, Player, Position):
  df_copy = df.copy()
  if len(League)> 0:
    df_copy = df_copy[df_copy["Ligas"].isin(League)]
  if len(Position) > 0:
    df_copy = df_copy[df_copy["Posicion"].isin(Position)]
  if len(Player)> 0:
    df_copy= df_copy[df_copy["Colombian Players"].isin(Player)]
  return df_copy
  

df_= filter_data(df, League, Player, Position)
st.title("Selecion Colombia")
st.subheader("Scout de jugadores colombianos")

total_jugadores = len(df_)
rating_medio = df_["Goles"].mean()

col1, col2 = st.columns(2)
col1.metric("#Jugadores", f"{total_jugadores:,.0f}")
col2.metric("Rating Goles", f"{rating_medio:,.1f}")

def get_player_statistics(df):
  radar_columns=['Goles', 'Asistencias', 'xG', 'xA',
               'Tiros', 'Tiros a puerta', '%Pases completados',
               'Pases clave', '%Centros Completados',
               '%Dribles exitosos', 'Perdidas de Balon', 'Entradas',
               'Intercepciones', '%Porcentaje de Duelos  Ganados ',
               'Duelos Aereos Ganados', 'Despejes', 'Tiros Bloqueados',
               'Penalty cometidos', 'Faltas cometidas', 'Faltas recibidas',
               'Tarjeta Amarilla', 'Tarjeta Roja']
  metrics = []
  for metric in radar_columns:
    metrics.append(df_[metric].mean())

  return pd.DataFrame(dict(metrics=metrics, theta=radar_columns))

radar_fig = px.line_polar(get_player_statistics(df_), r="metrics", theta="theta", line_close=True)

radar_fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True)
    ),
    showlegend=False
)
st.plotly_chart(radar_fig)

st.dataframe(df_)             

  # Los limites de las estadísticas para cada columna
low =  [0, 0, 0, 0, 1, 0, 64.68, 0, 0, 0, 0, 3, 1, 38, 3, 0, 0, 0, 0, 0, 0, 0]
high = [5, 5, 2.67, 6.16, 28, 10, 91, 27, 50, 75, 69, 69, 23, 67, 29, 34, 8, 1, 34, 37, 7, 1]

def radar_chart_2(df, player, player2, col_name_player, col_name_team, cols):
  pl1 = df[df[col_name_player] == player]
  val1 = pl1[radar_columns].values[0]

  pl2 = df[df[col_name_player] == player2]
  val2 = pl2[radar_columns].values[0]

  values = [val1, val2]
  ranges = [(df[radar_columns].min(), df[radar_columns].max()) for col in radar_columns]

  title = dict(
      title_name=player,
      title_color= "#B6282F",
      subtitle_name=pl1[col_name_team].values[0],
      subtitle_color= "#B6282F",

      title_name_2=player2,
      title_color_2= "#344D94",
      subtitle_name_2=pl2[col_name_team].values[0],
      subtitle_color_2= "#344D94",
      title_fontsize=18,
      subtitle_fontsize=15,
  )
  fig, ax = plt.subplots(figsize=(18, 15))
  radar = Radar(label_fontsize=20, range_fontsize=12)
  fig, ax = radar.plot_radar(ranges=ranges, params=cols, values=values, radar_color=["#B6282F", "344094"],)
