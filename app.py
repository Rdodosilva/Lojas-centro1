import streamlit as st
import os

# ==============================
# CONFIG DA PÁGINA
# ==============================
st.set_page_config(
    page_title="Mapa das Lojas",
    page_icon="🗺️",
    layout="wide"
)

# ==============================
# CSS — DARK MODE + MAPA GRANDE
# ==============================
st.markdown("""
<style>

/* Fundo geral */
.main {
    background-color: #0d0d0d;
    color: white;
}

/* Títulos */
h1, h2, h3, h4, h5, h6, label, .store-name-big {
    color: white !important;
}

/* Container do mapa — AGORA MAIOR */
.mapa-container {
    border-radius: 18px;
    overflow: hidden;
    margin: 10px 0 20px 0;
    box-shadow: 0 0px 25px rgba(200,200,255,0.15);
}

.mapa-container img {
    width: 100% !important;
    border-radius: 18px;
}

/* Foto da loja */
.foto-container {
    background: #1a1a1a;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 0px 20px rgba(255,255,255,0.08);
    margin-top: 15px;
}

/* Card da loja */
.store-info {
    background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
    color: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 0px 25px rgba(0,0,0,0.6);
    text-align: center;
    margin-bottom: 15px;
}

.store-name-big {
    font-size: 26px;
    font-weight: 700;
}

/* Dropdown dark */
select {
    background-color: #1a1a1a !important;
    color: white !important;
}

/* Avisos */
.instructions {
    background: rgba(255, 255, 0, 0.1);
    border-left: 4px solid #ffeb3b;
    padding: 10px;
    border-radius: 10px;
    margin-top: 10px;
    color: #f5f5a5;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# MAPA DAS LOJAS
# ==============================

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
    "Achadinhos": "Achadinhos.jpeg",
    "U Mi Acessórios": "U mi Acessorios.jpeg",
    "Vonny cosmeticos": "Vonny cosmeticos.jpeg",
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
    "Tudo Dez": "Tudo dez.jpeg",
}

todas_lojas = sorted(mapeamento_imagens.keys())

# Estado
if "loja_selecionada" not in st.session_state:
    st.session_state.loja_selecionada = None

# ==============================
# TÍTULO
# ==============================
st.markdown("## 🗺️ **Mapa das Lojas**")

# ==============================
# LAYOUT
# ==============================
col_map, col_info = st.columns([1.4, 1])

with col_map:
    st.markdown("### 📍 Mapa")

    if os.path.exists("mapa.jpg"):
        st.markdown('<div class="mapa-container">', unsafe_allow_html=True)
        st.image("mapa.jpg")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("❌ Arquivo 'mapa.jpg' não encontrado na raiz.")

with col_info:
    st.markdown("### 🏪 Selecione uma Loja")

    loja_selecionada = st.selectbox(
        "Escolha a loja:",
        ["Selecione uma loja..."] + todas_lojas
    )

    if loja_selecionada and loja_selecionada != "Selecione uma loja...":

        st.markdown(f"""
        <div class="store-info">
            <div class="store-name-big">📍 {loja_selecionada}</div>
        </div>
        """, unsafe_allow_html=True)

        nome_arquivo = mapeamento_imagens.get(loja_selecionada)

        if nome_arquivo:
            caminhos = [nome_arquivo, f"images/{nome_arquivo}", nome_arquivo.replace("images/", "")]
            carregou = False
            for c in caminhos:
                if os.path.exists(c):
                    st.markdown('<div class="foto-container">', unsafe_allow_html=True)
                    st.image(c, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    carregou = True
                    break

            if not carregou:
                st.warning(f"⚠️ Foto não encontrada: {nome_arquivo}")
        else:
            st.error("❌ Lo
