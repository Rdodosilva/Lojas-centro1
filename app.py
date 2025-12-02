import streamlit as st
import os

st.set_page_config(
    page_title="Mapa das Lojas",
    page_icon="🗺️",
    layout="wide"
)

# ===========================
#  TEMA DARK REAL (CSS)
# ===========================
st.markdown("""
<style>

    /* FUNDO GERAL PRETO */
    .main, body, html {
        background-color: #000000 !important;
        color: #ffffff !important;
    }

    /* Todos os textos brancos */
    h1, h2, h3, h4, h5, h6,
    p, span, label, div,
    .stMarkdown, .stText, .stCaption, .stMetric {
        color: #ffffff !important;
    }

    /* Sidebar dark */
    [data-testid="stSidebar"] {
        background-color: #0d0d0d !important;
        color: white !important;
    }

    /* Selectbox fundo preto + texto branco */
    .stSelectbox div, .stSelectbox label {
        color: white !important;
    }
    .stSelectbox > div > div {
        background-color: #111 !important;
        border: 1px solid #444 !important;
        color: #fff !important;
    }

    /* Dropdown da selectbox */
    div[data-baseweb="popover"] {
        background-color: #111 !important;
        border: 1px solid #555 !important;
    }
    div[data-baseweb="popover"] * {
        color: white !important;
    }

    /* Containers do mapa e fotos */
    .mapa-container, .foto-container {
        background-color: #111 !important;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 0 20px rgba(255,255,255,0.05);
    }

    /* Card da loja */
    .store-info {
        background: linear-gradient(135deg, #4a00e0, #8e2de2);
        color: white !important;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 22px;
        box-shadow: 0 0 15px rgba(142,45,226,0.4);
    }

    /* Métricas brancas */
    .stMetric {
        color: white !important;
    }

    /* Rodapé */
    footer, .stFooter {
        color: #fff !important;
    }

</style>
""", unsafe_allow_html=True)

# ===========================
#  MAPEAMENTO DAS IMAGENS
# ===========================
mapeamento_imagens = {
    "Magazine Luiza": "Magazine Luiza.jpeg",
    "Cia do H": "Cia do Homem.jpeg",
    "Damiller": "Damyller.jpeg",
    "Pop Dente": "Pop dente - Lupo.jpeg",
    "Lupo": "Pop dente - Lupo.jpeg",
    "Vivo": "Lojas Vivo.jpeg",
    # ... (continue com seu dicionário completo)
}

todas_lojas = sorted(mapeamento_imagens.keys())

# ===========================
#  UI
# ===========================
st.title("🗺️ Mapa das Lojas")

col_mapa, col_info = st.columns([1.3, 1])

# -------- MAPA -------- #
with col_mapa:
    st.subheader("📍 Mapa")
    st.markdown('<div class="mapa-container">', unsafe_allow_html=True)

    if os.path.exists("mapa.jpg"):
        st.image("mapa.jpg", use_container_width=True)
    else:
        st.error("❌ Arquivo 'mapa.jpg' não encontrado.")

    st.markdown("</div>", unsafe_allow_html=True)

# -------- INFO -------- #
with col_info:
    st.subheader("🏪 Selecione uma Loja")

    loja = st.selectbox("Escolha a loja:", [""] + todas_lojas)

    if loja:
        st.markdown(f'<div class="store-info">📍 {loja}</div>', unsafe_allow_html=True)

        nome_arquivo = mapeamento_imagens.get(loja)

        if nome_arquivo:
            for caminho in [nome_arquivo, f"images/{nome_arquivo}"]:
                if os.path.exists(caminho):
                    st.markdown('<div class="foto-container">', unsafe_allow_html=True)
                    st.image(caminho, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    break
            else:
                st.warning(f"⚠️ Foto não encontrada: {nome_arquivo}")

st.markdown("---")
st.caption("Mapa das lojas do centro — Tema Dark Real aplicado")

