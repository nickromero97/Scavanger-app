!pip install plotly.express

import streamlit as st
import pandas as pd
import plotly.express as px

# Leer los datos
df = pd.read_excel("/content/Jugadores de Colombia.xlsx")

with st.sidebar:
  st.write("Filtros")
  League = st.multiselect("Liga", sorted(df["Ligas"].unique()))
  Age = st.multiselect("Edad", sorted(df["Edad"].unique()))
  Player = st.multiselect("Jugador", sorted(df["Colombian Players"].unique()))
  Position = st.multiselect("Posición", sorted(df["Posicion"].unique()))

def filter_data(df, League, age, Player, Position):
  df_copy = df_copy()

  if len(League)> 0:
    df_copy = df_copy[df_copy["Liga"].isin(League)]
  if len(Position) > 0:
    df_copy = df_copy[df_copy["Posicion"].isin(Position)]
  return df_copy

df_=filter_data(df, League, age, Player, Position)
st.title("Selecion Colombia")
st.subheader("Scout de jugadores colombianos")

total_jugadores = len(df_)
rating_medio = df_["Goles"].mean()

col1, col2 = st.columns(2)
col1.metric("#Jugadores", f"{total_jugadores:,.0f}")
col2.metric("Rating Goles", f"{rating_medio:,.1f}")

def get_team_statistics(df):
  radar_columns=['Goles', 'Asistencias', 'xG', 'xA', 'G-P', 'Penalty',
       'P cobrados', 'Tiros', 'Tiros a puerta', 'Tiros/90',
       'Tiros a puerta/90', 'Tiros por Gol', 'Pases', '%Pases completados',
       'Pases clave', 'Centros', '%Centros Completados', 'Dribles',
       '%Dribles exitosos', 'Perdidas de Balon', 'Entradas',
       'Intercepciones', 'Duelos ', '%Porcentaje de Duelos  Ganados ',
       'Duelos Aereos Ganados', 'Despejes', 'Tiros Bloqueados',
       'Penalty cometidos', 'Faltas cometidas', 'Faltas recibidas',
       'Tarjeta Amarilla', 'Tarjeta Roja']

  metrics = []
  for metric in radar_columns:
    metrics.append(df_[metric].mean())

  return pd.DataFrame(dict(metrics=metrics, theta=radar_columns))

radar_fig = px.line_polar(get_team_statistics(df_), r="metrics", theta="theta", line_close=True)

radar.fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True)
    ),
    showlegend=False
)
st.ploty_chart(radar_fig)

st.dataframe(df_)
