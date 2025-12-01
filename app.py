import streamlit as st
from PIL import Image
import os

# ======================
# CONFIGURAÇÃO DA PÁGINA
# ======================
st.set_page_config(page_title="Mapa Interativo", layout="wide")

st.title("🗺️ Mapa Interativo")
st.write("Passe o mouse e selecione as fachadas das lojas conforme o mapa.")

# ======================
# EXIBIR MAPA PRINCIPAL
# ======================
MAPA = "mapa.jpg"   # nome do arquivo do mapa

if os.path.exists(MAPA):
    st.image(MAPA, caption="Mapa das Lojas", use_column_width=True)
else:
    st.error(f"⚠️ Arquivo '{MAPA}' não encontrado. Coloque o mapa.jpg na raiz do projeto.")

# ======================
# LISTAR IMAGENS DE LOJAS
# ======================
st.subheader("📸 Fachadas das Lojas")

st.write("Coloque todas as imagens das fachadas **na mesma pasta do app.py**.")

# Todos os arquivos de imagem exceto o mapa
imagens = [
    arq for arq in os.listdir('.')
    if arq.lower().endswith((".jpg", ".jpeg", ".png"))
    and arq != MAPA
]

if len(imagens) == 0:
    st.warning("Nenhuma fachada encontrada. Adicione imagens .jpg/.png na pasta do projeto.")
else:
    escolha = st.selectbox("Selecione a loja:", sorted(imagens))
    st.image(escolha, caption=escolha, use_column_width=True)
