import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO

# Configuração da página
st.set_page_config(page_title="Mapa de Lojas", layout="wide")

# CSS customizado para hover
st.markdown("""
<style>
    .store-container {
        position: relative;
        display: inline-block;
        margin: 5px;
        padding: 8px 12px;
        background: #f0f2f6;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .store-container:hover {
        background: #e0e5eb;
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .store-name {
        font-size: 14px;
        font-weight: 500;
        color: #1f1f1f;
    }
    
    .section-title {
        font-size: 18px;
        font-weight: 600;
        margin: 20px 0 10px 0;
        color: #0e1117;
        border-bottom: 2px solid #ff4b4b;
        padding-bottom: 5px;
    }
    
    .street-label {
        font-size: 16px;
        font-weight: 600;
        color: #ff4b4b;
        margin: 15px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Dados das lojas organizados por localização
lojas_data = {
    "Rua Trajano - Esquerda": [
        "Magazine Luiza", "Cia do H", "Damiller", "Pop Dente", "Lupo", 
        "ViVo", "Bazar das chaves", "Panvel"
    ],
    "Rua Trajano - Direita (Top)": [
        "Nfuzzi", "Para Alugar IBAGY", "Botton Utilidades", "bob's",
        "Artigos Religiosos", "Caixa", "Achadinhos", "U Mi Acessórios",
        "Vonny cosmeticos"
    ],
    "Rua Trajano - Direita (Centro)": [
        "Museu", "Café do Frank", "Massa Viva", "Floripa Implante",
        "Preço Popular", "Brasil Cacau", "Cia Do H", "Da Praça"
    ],
    "Rua Felipe Schmidt - Esquerda": [
        "Mil Bijus", "Colombo", "top1 Company", "Tim", "Corner bem",
        "Storil", "Mercadão", "Restaurante Magnolia", "Carioca calçados",
        "Kotzias", "Floripa Store", "JS Store", "Fuccs", "Vila Sucos",
        "Carioca cosmeticos", "Irmãos", "Fasbindrt", "Top1 Calçados",
        "Sabor do Tempero", "Procon"
    ],
    "Rua Felipe Schmidt - Direita": [
        "Loja de Acessórios", "Ótica Catarinense", "BMG", "Trid",
        "Claro", "Preço Unico", "Amo Biju", "AgiBank", "Cheirln Bão",
        "Oboticário", "Crefisa", "Ótica Rosangela", "MC Donalds",
        "Para Alugar", "Outlet Brás", "Suiê", "Tim revenda de chip",
        "Tudo Dez"
    ]
}

# Título principal
st.title("🗺️ Mapa Interativo de Lojas")
st.markdown("Passe o mouse sobre as lojas para ver a fachada")

# Seletor de loja para preview
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📍 Selecione uma loja")
    
    todas_lojas = []
    for secao, lojas in lojas_data.items():
        todas_lojas.extend(lojas)
    
    loja_selecionada = st.selectbox(
        "Escolha uma loja:",
        ["Selecione..."] + sorted(todas_lojas),
        key="loja_select"
    )

with col2:
    if loja_selecionada != "Selecione...":
        st.markdown(f"### 🏪 {loja_selecionada}")
        st.info("📸 Adicione a imagem da fachada em: `images/{nome_da_loja}.jpg`")
        
        # Tentar carregar a imagem se existir
        try:
            # Normalizar nome do arquivo
            filename = loja_selecionada.lower().replace(" ", "_").replace("'", "")
            img_path = f"images/{filename}.jpg"
            img = Image.open(img_path)
            st.image(img, caption=f"Fachada - {loja_selecionada}", use_container_width=True)
        except:
            st.warning("⚠️ Imagem não encontrada. Adicione em `images/` folder")

st.divider()

# Renderizar o mapa por seções
for secao, lojas in lojas_data.items():
    st.markdown(f'<div class="section-title">{secao}</div>', unsafe_allow_html=True)
    
    # Criar grid de lojas
    cols = st.columns(4)
    for idx, loja in enumerate(lojas):
        with cols[idx % 4]:
            # Criar botão interativo
            if st.button(loja, key=f"btn_{secao}_{loja}", use_container_width=True):
                st.session_state.loja_select = loja
                st.rerun()

st.divider()

# Instruções para setup
with st.expander("📚 Como usar este projeto"):
    st.markdown("""
    ### Estrutura de Pastas
    ```
    seu-projeto/
    ├── app.py                 # Este arquivo
    ├── images/                # Pasta com fotos das fachadas
    │   ├── magazine_luiza.jpg
    │   ├── cia_do_h.jpg
    │   └── ...
    ├── requirements.txt       # Dependências
    └── README.md
    ```
    
    ### Adicionar Imagens
    1. Crie uma pasta `images/` na raiz do projeto
    2. Adicione fotos com nomes: `nome_da_loja.jpg`
    3. Use letras minúsculas e substitua espaços por `_`
    
    ### Deploy no Streamlit Cloud
    1. Faça upload no GitHub
    2. Acesse [share.streamlit.io](https://share.streamlit.io)
    3. Conecte seu repositório
    4. Deploy automático! 🚀
    
    ### Requirements.txt
    ```
    streamlit
    pandas
    pillow
    ```
    """)

st.markdown("---")
st.caption("💡 Dica: Organize as imagens na pasta `images/` com nomes padronizados")
