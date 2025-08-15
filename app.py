from __future__ import annotations

import datetime as dt

import pandas as pd
import plotly.express as px
import streamlit as st

from databot.config import DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_HISTORY_DAYS
from databot.data import fetch_weather_daily, enrich_daily
from databot.agent.orchestrator import answer_question


st.set_page_config(page_title="DataBot – Clima", layout="wide")


st.title("DataBot – Agente Inteligente de Dados Climáticos")

# Parâmetros de entrada
with st.sidebar:
    st.header("Parâmetros")

    cidades = {
        "São Paulo": (-23.5505, -46.6333),
        "Rio de Janeiro": (-22.9068, -43.1729),
        "Lisboa": (38.7223, -9.1393),
        "Nova York": (40.7128, -74.0060),
    }

    cidade = st.selectbox("Cidade (exemplo)", options=list(cidades.keys()), index=0)
    lat_default, lon_default = cidades[cidade]

    lat = st.number_input("Latitude", value=float(lat_default), format="%.4f")
    lon = st.number_input("Longitude", value=float(lon_default), format="%.4f")

    days = st.slider("Dias de histórico", min_value=7, max_value=90, value=DEFAULT_HISTORY_DAYS)

    st.caption("Dados por Open-Meteo (sem necessidade de chave de API)")

@st.cache_data(show_spinner=False)
def load_data(latitude: float, longitude: float, days: int) -> pd.DataFrame:
    end = dt.date.today()
    start = end - dt.timedelta(days=days - 1)
    raw = fetch_weather_daily(latitude, longitude, start, end)
    proc = enrich_daily(raw)
    return proc

# Carrega dados
try:
    df = load_data(lat, lon, days)
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# Visualizações
st.subheader("Séries Temporais")
fig = px.line(
    df.reset_index(),
    x="date",
    y=["tmax", "tmin", "tavg"],
    title="Temperaturas diárias",
    labels={"value": "°C", "date": "Data", "variable": "Métrica"},
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Resumo")
col1, col2, col3, col4 = st.columns(4)
col1.metric("T. máx média", f"{df['tmax'].mean():.1f} °C")
col2.metric("T. mín média", f"{df['tmin'].mean():.1f} °C")
col3.metric("T. média", f"{df['tavg'].mean():.1f} °C")
col4.metric("Precipitação total", f"{df['precip'].sum():.1f} mm")

st.subheader("Pergunte ao DataBot")
question = st.text_input("Faça uma pergunta (ex.: 'qual a média de temperatura dos últimos 7 dias?' ou 'qual a previsão para amanhã?')")
if st.button("Responder") and question.strip():
    with st.spinner("Gerando resposta..."):
        response = answer_question(question, df)
    st.success(response)
