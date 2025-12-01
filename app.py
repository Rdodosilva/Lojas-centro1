import streamlit as st
import pandas as pd
import folium
from folium.features import DivIcon
from streamlit_folium import st_folium

st.set_page_config(page_title="Mapa Interativo de Lojas", layout="wide")

# ================================
# 1. CARREGA O CSV DE LOJAS
# ================================
@st.cache_data
def load_data():
    return pd.read_csv("lojas.csv")

df = load_data()

st.title("🗺️ Mapa Interativo das Lojas")
st.write("Passe o mouse por cima do nome da loja para ver a fachada.")

# ================================
# 2. CRIA O MAPA
# ================================
map_center = [df["latitude"].mean(), df["longitude"].mean()]
m = folium.Map(location=map_center, zoom_start=14)

# ================================
# 3. ADICIONA LOJAS AO MAPA
# ================================
for _, row in df.iterrows():
    nome = row["nome"]
    lat = row["latitude"]
    lon = row["longitude"]
    imagem = row["imagem"]  # caminho ou URL da imagem

    html_popup = f"""
    <div style="width:220px">
        <h4>{nome}</h4>
        <img src='{imagem}' style='width:200px;border-radius:8px'>
    </div>
    """

    folium.Marker(
        location=[lat, lon],
        tooltip=f"{nome}",
        popup=html_popup,
        icon=folium.Icon(color="purple", icon="info-sign"),
    ).add_to(m)

# ================================
# 4. MOSTRA O MAPA NO STREAMLIT
# ================================
st_folium(m, width=900, height=600)
