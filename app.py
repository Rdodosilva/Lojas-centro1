import streamlit as st
import os
from pathlib import Path

# ========================== #
# CONFIGURAÇÃO DA PÁGINA
# ========================== #
st.set_page_config(
    page_title="Mapa das Lojas",
    page_icon="🏪",
    layout="wide"
)

# ========================== #
# CSS — DARK THEME REAL
# ========================== #
st.markdown("""
<style>

    /* Fundo geral preto */
    .main, body, html {
        background-color: #000000 !important;
    }

    /* Sidebar preta */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
    }

    /* Texto branco em tudo */
    h1, h2, h3, h4, h5, h6, p, span, label, div, .stMarkdown, .stSelectbox, .stMetric {
        color: #ffffff !important;
    }

    /* Containers do mapa e foto */
    .mapa-container, .foto-container {
        background-color: #111111 !important;
        border-radius: 15px;
        padding: 18px;
        box-shadow: 0 0 25px rgba(255,255,255,0.08);
    }

    /* Card da loja */
    .store-info {
        background: linear-gradient(135deg, #6800ff 0%, #8f00ff 100%);
        color: #ffffff !important;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(130,0,255,0.4);
        text-align: center;
    }

    .store-name-big {
        font-size: 26px;
        font-weight: bold;
    }

    /* Caixa amarela retirada — agora dark */
    .instructions {
        background: #1a1a1a;
        border-left: 4px solid #8f00ff;
        padding: 14px;
        border-radius: 8px;
        margin: 20px 0;
        color: white !important;
    }

    /* Selectbox dark */
    .stSelectbox > div > div {
        background-color: #111111 !important;
        border: 1px solid #8f00ff !important;
        color: white !important;
    }

    /* Estilo das opções dentro do select */
    .css-26u2wg, .css-1n7v3ny, .css-16huue1 {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }

    /* Hover da opção */
    .css-1n7v3ny:hover {
        background-color: #333333 !important;
        color: white !important;
    }

</style>
""", unsafe_allow_html=True)

# ========================== #
# MAPEAMENTO DE IMAGENS
# ========================== #
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

# ========================== #
# HEADER
# ========================== #
st.title("🗺️ Mapa das Lojas")

# ========================== #
# LAYOUT
# ========================== #
col_mapa, col_foto = st.columns([1.2, 1])

# MAPA
with col_mapa:
    if os.path.exists("mapa.jpg"):
        st.markdown('<div class="mapa-container">', unsafe_allow_html=True)
        st.image("mapa.jpg", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("❌ Arquivo 'mapa.jpg' não encontrado.")

    st.markdown(
        '<div class="instructions">💡 Selecione uma loja ao lado para ver sua fachada.</div>',
        unsafe_allow_html=True
    )

# FOTO DA LOJA
with col_foto:
    st.markdown("### 🏪 Selecione uma Loja")

    loja = st.selectbox("Escolha a loja:", ["Selecione..."] + todas_lojas)

    if loja != "Selecione...":
        st.markdown(
            f'<div class="store-info"><div class="store-name-big">📍 {loja}</div></div>',
            unsafe_allow_html=True
        )

        nome = mapeamento_imagens.get(loja)
        caminhos = [nome, f"images/{nome}", nome.replace("images/", "")]

        achou = False
        for c in caminhos:
            if os.path.exists(c):
                st.markdown('<div class="foto-container">', unsafe_allow_html=True)
                st.image(c, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                achou = True
                break

        if not achou:
            st.warning(f"⚠️ Foto não encontrada: {nome}")

# RODAPÉ
st.markdown("---")
st.caption("Mapa das lojas do centro — Dark Mode Exclusivo 🔥")
