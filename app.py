import streamlit as st
import base64
import os

st.set_page_config(page_title="Mapeamento lojas centro", layout="wide")

st.title("🗺️ Mapa Interativo com Hover")

# ===== CARREGA O MAPA =====
mapa_path = "mapa.jpg"
if not os.path.exists(mapa_path):
    st.error("Arquivo mapa.jpg não encontrado.")
else:
    st.image(mapa_path, use_column_width=True)

st.write("Passe o mouse sobre os nomes no mapa para ver as fachadas.")

# ===== CARREGAR TODAS AS IMAGENS DAS FACHADAS =====
def carregar_imagem_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# mapeamento automático: usa o nome do arquivo como chave (sem extensão)
mapeamento = {}
for arq in os.listdir('.'):
    if arq.lower().endswith((".jpg", ".jpeg", ".png")) and arq != "mapa.jpg":
        chave = os.path.splitext(arq)[0].strip().lower()  # nome base
        mapeamento[chave] = carregar_imagem_base64(arq)

# ===== CSS PARA O POPUP =====
st.markdown("""
<style>
.tooltip {
  position: relative;
  display: inline-block;
  font-weight: bold;
  color: #00e1ff;
  cursor: pointer;
}

.tooltip .tooltip-image {
  visibility: hidden;
  width: 260px;
  background: #000;
  padding: 6px;
  border-radius: 10px;
  position: absolute;
  z-index: 10;
  top: 20px;
  left: 0px;
}

.tooltip:hover .tooltip-image {
  visibility: visible;
}
</style>
""", unsafe_allow_html=True)

# ===== GERAR HTML DINÂMICO DOS NOMES =====
# o usuário vai colocar manualmente a lista de nomes conforme aparece no mapa
# você precisa substituir abaixo pelos nomes EXATOS do mapa!

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

html = "<h3>Lojas Detectadas</h3>"

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
        html += f"<div style='color:red'>{nome} — imagem não encontrada</div>"

st.markdown(html, unsafe_allow_html=True)
