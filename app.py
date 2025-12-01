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
# CSS — TEMA ESCURO TOTAL
# ========================== #
st.markdown("""
<style>

/* Fundo geral preto */
.main {
    background-color: #000000 !important;
}

/* Texto branco global */
h1, h2, h3, h4, h5, h6,
label, p, span, div, .stMarkdown {
    color: #ffffff !important;
}

/* Containers escuros */
.mapa-container, .foto-container {
    border-radius: 18px;
    overflow: hidden;
    background-color: #111111 !important;
    padding: 15px;
    box-shadow: 0 6px 25px rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

/* Card da loja */
.store-info {
    background: linear-gradient(135deg, #1c1c1c 0%, #2b2b2b 100%);
    color: #ffffff !important;
    padding: 22px;
    border-radius: 12px;
    font-size: 22px;
    text-align: center;
    margin-bottom: 18px;
    box-shadow: 0 4px 14px rgba(255,255,255,0.10);
}

/* Selectbox texto branco */
.css-2trqyj, .stSelectbox div, .stSelectbox label {
    color: #ffffff !important;
}

/* Borda ciano no selectbox */
.stSelectbox > div > div {
    border: 1px solid #00c8ff !important;
}

/* Imagem do mapa */
.map-img {
    width: 100%;
    max-height: 900px;
    object-fit: contain;
}

/* Sidebar dark */
[data-testid="stSidebar"] {
    background-color: #0f0f0f !important;
}

/* Sidebar texto */
[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

</style>
""", unsafe_allow_html=True)

# ========================== #
# MAPA DE ARQUIVOS
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

if 'loja' not in st.session_state:
    st.session_state.loja = None

# ========================== #
# TÍTULO
# ========================== #
st.markdown("## 🗺️ Mapa das Lojas")

# ========================== #
# LAYOUT
# ========================== #
col_mapa, col_info = st.columns([1.3, 1])

# -------- MAPA -------- #
with col_mapa:
    st.markdown("### 📍 Mapa")

    if os.path.exists("mapa.jpg"):
        st.markdown('<div class="mapa-container">', unsafe_allow_html=True)
        st.image("mapa.jpg", use_column_width=True, output_format="PNG", caption="")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("❌ Arquivo 'mapa.jpg' não encontrado.")

# -------- INFO LOJA -------- #
with col_info:
    st.markdown("### 🏪 Selecione uma Loja")

    loja = st.selectbox("Escolha a loja:", [""] + todas_lojas)

    if loja:
        st.session_state.loja = loja

        st.markdown(
            f'<div class="store-info">📍 {loja}</div>',
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
                    st.image(c, use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    encontrada = True
                    break

            if not encontrada:
                st.warning(f"⚠️ Foto não encontrada: {nome_arquivo}")

# Rodapé
st.markdown("---")
st.caption("Mapa das lojas do centro — Desenvolvido para apresentação executiva")
