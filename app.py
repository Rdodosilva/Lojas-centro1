import streamlit as st
import os

# ========================== #
# CONFIGURAÇÃO DA PÁGINA
# ========================== #
st.set_page_config(
    page_title="Mapa das Lojas",
    page_icon="🗺️",
    layout="wide"
)

# ========================== #
# CSS — DARK MODE + MAPA MAIOR + SELECT PRETO
# ========================== #
st.markdown("""
<style>

/* Tema escuro geral */
.main {
    background-color: #0f0f0f !important;
}
[data-testid="stSidebar"] {
    background-color: #111 !important;
}

/* Títulos e textos */
h1, h2, h3, h4, h5, h6, .stMarkdown, label, p, span, div {
    color: white !important;
}

/* Container do MAPA */
.mapa-container {
    border-radius: 18px;
    overflow: hidden;
    background-color: #1a1a1a;
    padding: 10px;
    margin-bottom: 18px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}

/* AUMENTA O MAPA */
img {
    max-height: 1100px !important;
    object-fit: contain;
}

/* Card da loja selecionada */
.store-info {
    background: linear-gradient(135deg, #3a0ca3 0%, #7209b7 100%);
    color: white !important;
    padding: 18px;
    border-radius: 12px;
    font-size: 24px;
    text-align: center;
    margin-bottom: 18px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.45);
}

/* Card da foto */
.foto-container {
    background-color: #1a1a1a;
    border-radius: 16px;
    padding: 12px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.45);
}

/* Selectbox — texto preto para melhor leitura */
div[data-baseweb="select"] * {
    color: black !important;
    font-weight: 600;
}

/* Caixa do select */
.stSelectbox > div > div {
    border: 2px solid #7209b7 !important;
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# ========================== #
# MAPEAMENTO DAS LOJAS
# ========================== #
mapeamento_imagens = {
    "Magazine Luiza": "Magazine Luiza.jpeg",
    "Cia do H": "Cia do Homem.jpeg",
    "Damiller": "Damyller.jpeg",
    "Pop Dente": "Pop dente - Lupo.jpeg",
    "Lupo": "Pop dente - Lupo.jpeg",
    "Vivo": "Lojas Vivo.jpeg",
    "Bazar das Chaves": "Bazar das chave - Panvel.jpeg",
    "Panvel": "Bazar das chave - Panvel.jpeg",

    "Nfuzzi": "Nluzzi.jpeg",
    "IBAGY – Para Alugar": "Aluga Ibagy.jpeg",
    "Botton Utilidades": "Botton Utilidades.jpeg",
    "Bob's": "Bob's.jpeg",
    "Artigos Religiosos": "Itens Religiosos.jpeg",
    "Achadinhos": "Achadinhos.jpeg",
    "U Mi Acessórios": "U mi Acessorios.jpeg",
    "Vonny Cosméticos": "Vonny cosmeticos.jpeg",

    "Café do Frank": "Café do Frank.jpeg",
    "Massa Viva": "Massa Viva.jpeg",
    "Floripa Implante": "Foripa Implantes.jpeg",
    "Preço Popular": "Preço popular.jpeg",
    "Brasil Cacau": "Brasil cacau.jpeg",
    "Da Praça": "Da Praça.jpeg",

    "Mil Bijus": "Mil Bijus.jpeg",
    "Colombo": "Colombo.jpeg",
    "Top1 Company": "Top 1 Company.jpeg",
    "Tim": "Tim.jpeg",
    "Comer Bem": "Restauante Comer bem.jpeg",
    "Estoril": "Estoril.jpeg",
    "Mercadão dos Óculos": "Mercadão dos Ocúlos.jpeg",
    "Magnólia": "Restaurante Magnolia.jpeg",
    "Carioca Calçados": "carioca calçados.jpeg",
    "Kotzias": "Kotzias.jpeg",
    "Floripa Store": "Floripa store.jpeg",
    "JS Store": "JS Store.jpeg",
    "Fucci's": "Fucci's.jpeg",
    "Vita Sucos": "Vita sucos.jpeg",
    "Carioca Cosméticos": "Carioca cosmeticos.jpeg",
    "Irmãos Dias": "Irmãos.jpeg",
    "Fasbinder": "Fasbinder.jpeg",
    "Top1 Calçados": "Top 1 calçados.jpeg",
    "Sabor do Tempero": "Restaurante sabor de tempero.jpeg",
    "Procon": "Procon.jpeg",

    "Loja de Acessórios": "Loja de acessorios.jpeg",
    "Ótica Catarinense": "Otica catarinense.jpeg",
    "BMG": "Banco BMG.jpeg",
    "Trid": "Trid.jpeg",
    "Claro": "Claro.jpeg",
    "Preço Único R$80": "Preço Unico 80,00.jpeg",
    "Amo Biju": "Amo bijuterias.jpeg",
    "Agibank": "Agibank.jpeg",
    "Cheirin Bão": "Cheirin bão.jpeg",
    "O Boticário": "Oboticario.jpeg",
    "Crefisa": "Crefisa.jpeg",
    "Ótica Rosângela": "Ótica Rosangela.jpeg",
    "Mc Donald's": "MC Donald.jpeg",
    "Para Alugar": "Para Alugar.jpeg",
    "Outlet Brás": "Outlet Brás.jpeg",
    "Suiê": "Suiê.jpeg",
    "Tim (Revenda de Chip)": "Tim revenda de chip.jpeg",
    "Tudo Dez": "Tudo dez.jpeg"
}

todas_lojas = sorted(mapeamento_imagens.keys())

# ========================== #
# TÍTULO
# ========================== #
st.markdown("## 🗺️ Mapa das Lojas")

# ========================== #
# LAYOUT
# ========================== #
col_mapa, col_info = st.columns([1.5, 1])

# -------- MAPA -------- #
with col_mapa:
    st.markdown("### 📍 Mapa Completo")

    if os.path.exists("mapa.jpg"):
        st.markdown('<div class="mapa-container">', unsafe_allow_html=True)
        st.image("mapa.jpg", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("❌ Arquivo 'mapa.jpg' não encontrado.")

# -------- INFORMAÇÕES -------- #
with col_info:
    st.markdown("### 🏪 Selecione uma Loja")

    loja = st.selectbox("Escolha a loja:", [""] + todas_lojas)

    if loja:
        st.markdown(
            f'<div class="store-info">📍 {loja}</div>',
            unsafe_allow_html=True
        )

        nome_arquivo = mapeamento_imagens.get(loja)

        caminhos = [nome_arquivo, f"images/{nome_arquivo}"]
        encontrada = False

        for c in caminhos:
            if c and os.path.exists(c):
                st.markdown('<div class="foto-container">', unsafe_allow_html=True)
                st.image(c, use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                encontrada = True
                break

        if not encontrada:
            st.warning(f"⚠️ Foto não encontrada: {nome_arquivo}")

# Rodapé
st.markdown("---")
st.caption("Mapa das lojas do centro — Visualização executiva")
