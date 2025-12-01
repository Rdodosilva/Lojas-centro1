import streamlit as st
import os
from pathlib import Path

# ============================
# CONFIGURAÇÃO DA PÁGINA
# ============================
st.set_page_config(
    page_title="Mapa das Lojas",
    page_icon="🏪",
    layout="wide"
)

# ============================
#  CSS — DARK MODE REAL
# ============================
st.markdown("""
<style>

    /* ===== FUNDO GERAL ===== */
    .main, body {
        background-color: #000000 !important;
        color: #ffffff !important;
    }

    /* ===== TEXTOS ===== */
    h1, h2, h3, h4, h5, h6,
    p, span, div, label {
        color: #ffffff !important;
    }

    /* Corrige texto dentro de elementos internos */
    [data-testid="stMarkdown"] p,
    [data-testid="stMarkdown"] span,
    [data-testid="stMarkdown"] div {
        color: #ffffff !important;
    }

    /* ===== SELECTBOX ===== */
    .stSelectbox div, .stSelectbox label {
        color: #ffffff !important;
    }

    .stSelectbox > div > div {
        background-color: #111 !important;
        border: 1px solid #555 !important;
        color: white !important;
    }

    /* Placeholders brancos */
    .stSelectbox div[data-baseweb="select"] span {
        color: #cccccc !important;
    }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background-color: #0d0d0d !important;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* ===== MAPA / FOTO CARD ===== */
    .mapa-container, .foto-container {
        background-color: #111 !important;
        border-radius: 16px;
        padding: 15px;
        box-shadow: 0 0 20px rgba(255,255,255,0.08);
        margin-bottom: 20px;
    }

    /* ===== CARD DA LOJA ===== */
    .store-info {
        background: linear-gradient(135deg, #4c00ff55, #8700ff55);
        color: #ffffff !important;
        padding: 22px;
        border-radius: 14px;
        text-align: center;
        font-size: 22px;
        box-shadow: 0 0 25px rgba(130,0,255,0.25);
    }

    .store-name-big {
        font-size: 28px;
        font-weight: bold;
        color: white !important;
    }

    /* ===== ALERTAS ===== */
    .stAlert {
        background-color: #222 !important;
        color: white !important;
        border-left: 4px solid #9147ff !important;
    }

    /* ===== METRICS ===== */
    [data-testid="stMetricValue"] {
        color: white !important;
    }
    [data-testid="stMetricLabel"] {
        color: #cccccc !important;
    }

</style>
""", unsafe_allow_html=True)

# ============================
# MAPEAMENTO
# ============================
mapeamento_imagens = {
    "Magazine Luiza": "Magazine Luiza.jpeg",
    "Cia do H": "Cia do Homem.jpeg",
    "Damiller": "Damyller.jpeg",
    "Pop Dente": "Pop dente - Lupo.jpeg",
    "Lupo": "Pop dente - Lupo.jpeg",
    "ViVo": "Lojas Vivo.jpeg",
    "Bazar das chaves": "Bazar das chave - Panvel.jpeg",
    "Panvel": "Bazar das chave - Panvel.jpeg",
    "Nfuzzi": "Nluzzi.jpeg",
    "Para Alugar IBAGY": "Aluga Ibagy.jpeg",
    "Botton Utilidades": "Botton Utilidades.jpeg",
    "bob's": "Bob's.jpeg",
    "Artigos Religiosos": "Itens Religiosos.jpeg",
    "Caixa": "images/caixa.jpeg",
    "Achadinhos": "Achadinhos.jpeg",
    "U Mi Acessórios": "U mi Acessorios.jpeg",
    "Vonny cosmeticos": "Vonny cosmeticos.jpeg",
    "Museu": "images/museu.jpeg",
    "Café do Frank": "Café do Frank.jpeg",
    "Massa Viva": "Massa Viva.jpeg",
    "Floripa Implante": "Foripa Implantes.jpeg",
    "Preço Popular": "Preço popular.jpeg",
    "Brasil Cacau": "Brasil cacau.jpeg",
    "Cia Do H": "Cia do Homem 1.jpeg",
    "Da Praça": "Da Praça.jpeg",
    "Mil Bijus": "Mil Bijus.jpeg",
    "Colombo": "Colombo.jpeg",
    "top1 Company": "Top 1 Company.jpeg",
    "Tim": "Tim.jpeg",
    "Corner bem": "Restauante Comer bem.jpeg",
    "Storil": "Estoril.jpeg",
    "Mercadão": "Mercadão dos Ocúlos.jpeg",
    "Restaurante Magnolia": "Restaurante Magnolia.jpeg",
    "Carioca calçados": "carioca calçados.jpeg",
    "Kotzias": "Kotzias.jpeg",
    "Floripa Store": "Floripa store.jpeg",
    "JS Store": "JS Store.jpeg",
    "Fuccs": "Fucci's.jpeg",
    "Vila Sucos": "Vita sucos.jpeg",
    "Carioca cosmeticos": "Carioca cosmeticos.jpeg",
    "Irmãos": "Irmãos.jpeg",
    "Fasbindrt": "Fasbinder.jpeg",
    "Top1 Calçados": "Top 1 calçados.jpeg",
    "Sabor do Tempero": "Restaurante sabor de tempero.jpeg",
    "Procon": "Procon.jpeg",
    "Loja de Acessórios": "Loja de acessorios.jpeg",
    "Ótica Catarinense": "Otica catarinense.jpeg",
    "BMG": "Banco BMG.jpeg",
    "Trid": "Trid.jpeg",
    "Claro": "Claro.jpeg",
    "Preço Unico": "Preço Unico 80,00.jpeg",
    "Amo Biju": "Amo bijuterias.jpeg",
    "AgiBank": "Agibank.jpeg",
    "Cheirln Bão": "Cheirin bão.jpeg",
    "Oboticário": "Oboticario.jpeg",
    "Crefisa": "Crefisa.jpeg",
    "Ótica Rosangela": "Ótica Rosangela.jpeg",
    "MC Donalds": "MC Donald.jpeg",
    "Para Alugar": "Para Alugar.jpeg",
    "Outlet Brás": "Outlet Brás.jpeg",
    "Suiê": "Suiê.jpeg",
    "Tim revenda de chip": "Tim revenda de chip.jpeg",
    "Tudo Dez": "Tudo dez.jpeg"
}

todas_lojas = sorted(mapeamento_imagens.keys())

if "loja_selecionada" not in st.session_state:
    st.session_state.loja_selecionada = None

# ============================
# TÍTULO
# ============================
st.title("🗺️ Mapa das Lojas")

# ============================
# LAYOUT PRINCIPAL
# ============================
col_mapa, col_foto = st.columns([1.2, 1])

with col_mapa:
    if os.path.exists("mapa.jpg"):
        st.markdown('<div class="mapa-container">', unsafe_allow_html=True)
        st.image("mapa.jpg", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("❌ Arquivo 'mapa.jpg' não encontrado")

with col_foto:
    st.markdown("### 🏪 Loja")

    loja = st.selectbox(
        "Escolha a loja:",
        ["Selecione..."] + todas_lojas
    )

    if loja != "Selecione...":
        st.session_state.loja_selecionada = loja

        st.markdown(
            f'<div class="store-info"><div class="store-name-big">📍 {loja}</div></div>',
            unsafe_allow_html=True
        )

        nome_arquivo = mapeamento_imagens.get(loja)

        if nome_arquivo:
            caminhos = [
                nome_arquivo,
                f"images/{nome_arquivo}"
            ]

            encontrada = False
            for c in caminhos:
                if os.path.exists(c):
                    st.markdown('<div class="foto-container">', unsafe_allow_html=True)
                    st.image(c, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    encontrada = True
                    break

            if not encontrada:
                st.warning(f"⚠️ Foto não encontrada: `{nome_arquivo}`")

# ============================
# RODAPÉ
# ============================
st.markdown("---")
st.caption("🏢 Mapa das lojas do centro | Tema Dark Premium | Desenvolvido para apresentação executiva")

