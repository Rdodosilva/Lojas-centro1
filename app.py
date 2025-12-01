import streamlit as st
import base64
import os

st.set_page_config(page_title="Mapa Interativo", layout="wide")

st.title("🗺️ Mapa Interativo — Hover nas Lojas")

# ========= MOSTRA O MAPA =========
mapa_path = "mapa.jpg"
if not os.path.exists(mapa_path):
    st.error("Arquivo mapa.jpg não encontrado no diretório do app.")
else:
    st.image(mapa_path, use_column_width=True)

st.write("Passe o mouse sobre os nomes do mapa para ver as fachadas.")

# ========= FUNÇÃO PARA CONVERTER IMAGEM EM BASE64 =========
def carregar_imagem_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ========= MAPEAMENTO AUTOMÁTICO (usa nome do arquivo) =========
mapeamento = {}
for arquivo in os.listdir('.'):
    if arquivo.lower().endswith((".jpg", ".jpeg", ".png")) and arquivo != "mapa.jpg":
        chave = os.path.splitext(arquivo)[0].strip().lower()
        mapeamento[chave] = carregar_imagem_base64(arquivo)

# ========= CSS PARA POPUP =========
st.markdown("""
<style>
.tooltip {
  position: relative;
  font-weight: bold;
  color: #00e1ff;
  cursor: pointer;
  padding: 4px;
}
.tooltip .tooltip-image {
  visibility: hidden;
  width: 260px;
  background: black;
  padding: 6px;
  border-radius: 10px;
  position: absolute;
  z-index: 99;
  top: 22px;
  left: 0px;
}
.tooltip:hover .tooltip-image {
  visibility: visible;
}
</style>
""", unsafe_allow_html=True)

# ========= NOMES EXATOS DO MAPA (extraídos da imagem) =========
nomes_no_mapa = [
    "niuzzi",
    "para alugar ibagy",
    "botton utilidades",
    "bob's",
    "outlet brás",
    "suie",
    "tim revenda de chip",
    "tudo dez"
]

# ========= GERAR HTML INTERATIVO =========
html = "<h3>Lojas Detectadas no Projeto</h3>"

for nome in nomes_no_mapa:
    chave = nome.lower().strip()

    if chave in mapeamento:
        img64 = mapeamento[chave]
        html += f"""
        <div class='tooltip'>{nome}
            <img class='tooltip-image' src='data:image/jpeg;base64,{img64}' />
        </div><br>
        """
    else:
        html += f"<div style='color:red'>{nome} — imagem NÃO encontrada</div>"

st.markdown(html, unsafe_allow_html=True)
