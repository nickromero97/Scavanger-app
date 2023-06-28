

import streamlit as st
import pandas as pd
import plotly.express as px

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
