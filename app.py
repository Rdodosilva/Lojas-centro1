import streamlit as st
import os
from pathlib import Path

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(
    page_title="Mapa das Lojas",
    page_icon="🗺️",
    layout="wide"
)

# ==============================
# CSS MODERNO / VISUAL MELHORADO
# ==============================
st.markdown("""
<style>

    /* Fundo da página */
    .main {
        background-color: #f5f6fa;
    }

    /* Título */
    .main-title {
        font-size: 44px;
        font-weight: 800;
        padding: 0;
        margin-bottom: -10px;
        color: #1a1a1a;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Contêiner do mapa */
    .mapa-container {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 8px 22px rgba(0,0,0,0.12);
        margin: 25px 0;
        background: white;
        padding: 12px;
    }

    /* Contêiner da imagem */
    .foto-container {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 8px 22px rgba(0,0,0,0.12);
        margin-top: 25px;
        background: white;
        padding: 20px;
    }

    /* Card da loja selecionada */
    .store-info {
        background: linear-gradient(135deg, #6a5acd 0%, #8250df 100%);
        color: white;
        padding: 22px;
        border-radius: 14px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        text-align: center;
    }

    .store-name-big {
        font-size: 30px;
        font-weight: 700;
        margin: 0;
    }

    /* Aviso amarelo */
    .instructions {
        background: #fff1b8;
        border-left: 5px solid #ffcd39;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
        font-size: 16px;
    }

</style>
""", unsafe_allow_html=True)

# ==============================
# MAPA DE NOMES → IMAGENS
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
    "Tudo Dez": "Tudo dez.jpeg"
}

todas_lojas = sorted(mapeamento_imagens.keys())

# ==============================
# SESSION STATE
# ==============================
if "loja_selecionada" not in st.session_state:
    st.session_state.loja_selecionada = None

# ==============================
# TÍTULO
# ==============================
st.markdown('<div class="main-title">🗺️ Mapa das Lojas</div>', unsafe_allow_html=True)

# ==============================
# LAYOUT (MAPA + FOTO)
# ==============================
col_mapa, col_foto = st.columns([1.25, 1])

# 📍 MAPA
with col_mapa:
    st.markdown("### 📍 Mapa")

    if os.path.exists("mapa.jpg"):
        st.markdown('<div class="mapa-container">', unsafe_allow_html=True)
        st.image("mapa.jpg", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("❌ Arquivo 'mapa.jpg' não foi encontrado!")

# 🏪 SELETOR + FOTO
with col_foto:
    st.markdown("### 🏪 Selecione uma Loja")

    loja = st.selectbox(
        "Escolha a loja:",
        ["Selecione uma loja..."] + todas_lojas
    )

    if loja != "Selecione uma loja...":
        st.session_state.loja_selecionada = loja

        st.markdown(
            f'<div class="store-info"><div class="store-name-big">📍 {loja}</div></div>',
            unsafe_allow_html=True
        )

        arquivo = mapeamento_imagens.get(loja)

        if arquivo:
            caminhos = [
                arquivo,
                f"images/{arquivo}",
                arquivo.replace("images/", "")
            ]

            exibida = False
            for path in caminhos:
                if os.path.exists(path):
                    st.markdown('<div class="foto-container">', unsafe_allow_html=True)
                    st.image(path, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    exibida = True
                    break

            if not exibida:
                st.warning(f"⚠️ Não encontrei a imagem: `{arquivo}`")

    else:
        st.info("👈 Escolha uma loja acima para visualizar a fachada.")

# Rodapé
st.markdown("---")
st.caption("📍 Mapa das lojas do centro — Desenvolvido para apresentação executiva")

