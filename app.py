import streamlit as st
import os
from pathlib import Path

# ================================
# CONFIGURAÇÃO DA PÁGINA
# ================================
st.set_page_config(
    page_title="Mapa das Lojas",
    page_icon="🗺️",
    layout="wide"
)

# ================================
# TEMA ESCURO + CSS
# ================================
st.markdown("""
<style>
    body, .main {
        background-color: #0e0e0e !important;
        color: white !important;
    }

    h1, h2, h3, h4, h5, h6, label, p, span {
        color: white !important;
    }

    /* Caixa do mapa */
    .mapa-container {
        border-radius: 12px;
        overflow: hidden;
        margin: 10px 0 25px 0;
        border: 1px solid #333;
    }

    /* Caixa da foto */
    .foto-container {
        border-radius: 12px;
        overflow: hidden;
        background: #1a1a1a;
        padding: 20px;
        border: 1px solid #333;
    }

    /* Card da loja selecionada */
    .store-info {
        background: linear-gradient(90deg, #4c2aff, #822aff);
        color: white !important;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 15px;
    }

    /* Ajuste do selectbox */
    .stSelectbox div {
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# ================================
# MAPEAMENTO DAS LOJAS
# ================================
mapeamento_imagens = {
    "Magazine Luiza": "Magazine Luiza.jpeg",
    "Cia do H": "Cia do Homem.jpeg",
    "Damiller": "Damyller.jpeg",
    "Pop Dente": "Pop dente - Lupo.jpeg",
    "Lupo": "Pop dente - Lupo.jpeg",
    "ViVo": "Lojas Vivo.jpeg",
    "Bazar das chaves": "Bazar das chave - Panvel.jpeg",
    "Panvel": "Bazar das chave - Panvel.jpeg",

    # Direita superior
    "Nfuzzi": "Nluzzi.jpeg",
    "Para Alugar IBAGY": "Aluga Ibagy.jpeg",
    "Botton Utilidades": "Botton Utilidades.jpeg",
    "bob's": "Bob's.jpeg",
    "Artigos Religiosos": "Itens Religiosos.jpeg",
    "Achadinhos": "Achadinhos.jpeg",
    "U Mi Acessórios": "U mi Acessorios.jpeg",
    "Vonny cosmeticos": "Vonny cosmeticos.jpeg",

    # Direita inferior
    "Café do Frank": "Café do Frank.jpeg",
    "Massa Viva": "Massa Viva.jpeg",
    "Floripa Implante": "Foripa Implantes.jpeg",
    "Preço Popular": "Preço popular.jpeg",
    "Brasil Cacau": "Brasil cacau.jpeg",
    "Da Praça": "Da Praça.jpeg",

    # Felipe Schmidt esquerda
    "Mil Bijus": "Mil Bijus.jpeg",
    "Colombo": "Colombo.jpeg",
    "top1 Company": "Top 1 Company.jpeg",
    "Ti

    
