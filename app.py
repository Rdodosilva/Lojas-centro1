import streamlit as st
import os
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Mapa das Lojas",
    page_icon="🏪",
    layout="wide"
)

#######################################
# 🔵 LISTA DAS LOJAS DO HÉLIO BEZ
#######################################
helio_bez_lojas = {
    "Cia. do Homem",
    "Mil Bijus",
    "Colombo",
    "top1 Company",
    "Vila Sucos",
    "Carioca cosmeticos",
    "Amo Biju"
}

#######################################
# 🎨 CSS — colore NOME no mapa e cria legenda
#######################################
st.markdown("""
<style>

    .main { background-color: #f8f9fa; }

    /* Caixa do mapa */
    .mapa-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        margin: 20px 0;
        position: relative;
    }

    /* Foto da loja */
    .foto-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        margin-top: 20px;
        background: white;
        padding: 20px;
    }

    /* Nome grande da loja */
    .store-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        text-align: center;
    }

    .store-name-big {
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }

    /* Caixa de instruções */
    .instructions {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
    }

    /* 🔵 Cor azul do Hélio Bez */
    .helio-bez {
        font-weight: 900;
        color: #007BFF !important;
        text-shadow: 0px 0px 4px rgba(0,123,255,0.6);
    }

    /* Caixa da legenda */
    .legenda-box {
        background: #eef5ff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #cce0ff;
        margin: 10px 0 20px 0;
    }

</style>
""", unsafe_allow_html=True)

#######################################
# 🔀 Mapeamento loja → arquivo de imagem
#######################################
mapeamento_imagens = {
    "Magazine Luiza": "Magazine Luiza.jpeg",
    "Cia. do Homem": "Cia do Homem.jpeg",
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

#######################################
# Lista única de lojas
#######################################
todas_lojas = sorted(mapeamento_imagens.keys())

#######################################
# Estado
#######################################
if 'loja_selecionada' not in st.session_state:
    st.session_state.loja_selecionada = None

#######################################
# Título
#######################################
st.title("🗺️ Mapa das Lojas")

#######################################
# Layout
#######################################
col_mapa, col_foto = st.columns([1.2, 1])

with col_mapa:

    # LEGENDA
    st.markdown("""
    <div class="legenda-box">
        <b>🔵 Lojas do Hélio Bez:</b><br>
        Cia. do Homem, Mil Bijus, Colombo, Top1 Company, Vila Sucos, Carioca Cosméticos, Amo Biju
    </div>
    """, unsafe_allow_html=True)

    # Exibir o mapa
    if os.path.exists("mapa.jpg"):

        # APLICAR COR NOS NOMES
        with open("mapa.jpg", "rb") as f:
            st.markdown('<div class="mapa-container">', unsafe_allow_html=True)
            st.image("mapa.jpg", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Gerar CSS para colorir nomes no mapa
        for loja in helio_bez_lojas:
            st.markdown(
                f"<style>span:contains('{loja}') {{ color:#007BFF !important; font-weight:900; }}</style>",
                unsafe_allow_html=True
            )

    else:
        st.error("❌ Arquivo 'mapa.jpg' não encontrado na raiz do projeto")

    st.markdown(
        '<div class="instructions">💡 <b>Dica:</b> Selecione uma loja ao lado para ver sua fachada.</div>',
        unsafe_allow_html=True
    )

with col_foto:

    st.markdown("### 🏪 Selecione uma Loja")

    loja_selecionada = st.selectbox(
        "Escolha a loja:",
        ["Selecione uma loja..."] + todas_lojas,
        key="loja_selector"
    )

    if loja_selecionada and loja_selecionada != "Selecione uma loja...":
        st.session_state.loja_selecionada = loja_selecionada

        st.markdown(
            f'<div class="store-info"><div class="store-name-big">📍 {loja_selecionada}</div></div>',
            unsafe_allow_html=True
        )

        nome_arquivo = mapeamento_imagens.get(loja_selecionada)

        if nome_arquivo:
            caminhos = [
                nome_arquivo,
                f"images/{nome_arquivo}",
                nome_arquivo.replace("images/", "")
            ]

            imagem_encontrada = False
            for c in caminhos:
                if os.path.exists(c):
                    st.markdown('<div class="foto-container">', unsafe_allow_html=True)
                    st.image(c, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    imagem_encontrada = True
                    break

            if not imagem_encontrada:
                st.warning(f"⚠️ Foto não encontrada: `{nome_arquivo}`")
        else:
            st.error("❌ Loja não mapeada.")
    else:
        st.info("👈 Veja o mapa ao lado e selecione uma loja acima.")

#######################################
# Footer + reset
#######################################
st.markdown("---")
st.caption("🏢 Mapa das lojas do centro | Desenvolvido para apresentação executiva")

if st.session_state.loja_selecionada:
    if st.button("🔄 Resetar Seleção", use_container_width=True):
        st.session_state.loja_selecionada = None
        st.rerun()
