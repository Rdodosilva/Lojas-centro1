# app.py
# Streamlit app — Mapa das Lojas (dark / futurista) com hover de fachadas + editor visual (localStorage)
# Coloque este arquivo na raiz do repositório junto com mapa.jpg e suas imagens de fachadas.

import streamlit as st
import json
import os
from pathlib import Path

st.set_page_config(page_title="Mapa das Lojas", page_icon="🏪", layout="wide")

# ----------------------------
# Configs - ajuste rápido aqui
# ----------------------------
MAP_FILE = "mapa.jpg"
# Se suas fachadas estão espalhadas na raiz, usamos o nome do arquivo exato. Caso estejam em "images/", altere o caminho nas regras JS.
# O dicionário abaixo mapeia o NOME_VISÍVEL -> NOME_DE_ARQUIVO (exato como está no seu repo)
mapeamento_imagens = {
    "Magazine Luiza": "Magazine Luiza.jpeg",
    "Cia do H": "Cia do Homem.jpeg",
    "Damiller": "Damyller.jpeg",
    "Pop Dente": "Pop dente - Lupo.jpeg",
    "Lupo": "Pop dente - Lupo.jpeg",
    "Vivo": "Lojas Vivo.jpeg",
    "Bazar das Chaves": "Bazar das chave - Panvel.jpeg",
    "Panvel": "Panvel.jpeg",
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

# Convert to JSON string for injecting in JS (ensure ascii preserved)
mapeamento_json = json.dumps(mapeamento_imagens, ensure_ascii=False)

# ----------------------------
# UI
# ----------------------------
st.markdown("<style>html, body, .block-container{background:#07070a; color: #e8eaf6;}</style>", unsafe_allow_html=True)
st.markdown("""
    <style>
    /* Futurista / Dark theme */
    .stApp, .reportview-container, .main {
        background: linear-gradient(180deg,#06060a 0%, #0d0b14 100%) !important;
    }
    .card { background: rgba(255,255,255,0.02); border-radius: 12px; padding: 12px; }
    .title { color: #e8eaf6; font-weight:700; }
    .subtitle { color: #bdb8ff; }
    /* Purple accent */
    .accent { color: #b892ff; }
    /* Tooltip image */
    .hot-img { border-radius: 8px; box-shadow: 0 10px 30px rgba(135,0,255,0.18); border: 1px solid rgba(182,146,255,0.12); }
    /* make select text legible in dark */
    .stSelectbox > div[role="listbox"] { color: #000 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>Mapa das Lojas</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Passe o mouse sobre os nomes no mapa para ver a fachada. Ative <span class='accent'>Edit Mode</span> para posicionar hotspots.</p>", unsafe_allow_html=True)

# Columns layout: mapa à esquerda maior
col_map, col_right = st.columns([1.4, 0.8])

with col_right:
    st.markmark = st  # noop to keep line count even (no effect)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin:6px 0 4px 0'>Controls</h3>", unsafe_allow_html=True)
    edit_mode = st.checkbox("Edit Mode (clique no mapa para adicionar hotspot)", value=False)
    show_labels = st.checkbox("Mostrar labels (nomes no mapa)", value=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("**Export / Import hotspots**", unsafe_allow_html=True)
    if st.button("Exportar hotspots (copiar JSON)"):
        # We'll instruct user to use the export button in the map widget (JS) — server can't access localStorage
        st.info("Abra o painel do mapa (à esquerda) e clique em 'Export JSON' para copiar os hotspots. (O editor usa localStorage do navegador.)")
    st.markdown("<p style='font-size:13px; color:#cfc8ff'>Observação: o editor salva no <code>localStorage</code> do navegador. Depois de ajustar, copie o JSON e cole num arquivo hotspots.json no repo para manter permanente.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_map:
    # Prepare hotspots default: try load hotspots.json from repo if exists, else empty
    hotspots_file = Path("hotspots.json")
    hotspots_data = []
    if hotspots_file.exists():
        try:
            hotspots_data = json.loads(hotspots_file.read_text(encoding="utf-8"))
        except Exception:
            hotspots_data = []

    # Pass data to the HTML widget
    hotspots_json = json.dumps(hotspots_data, ensure_ascii=False)
    # Build the HTML+JS that draws the map, overlays labels and shows image tooltips on hover.
    # Editor allows clicks to add hotspots and buttons to export JSON (copy to clipboard).
    html = f"""
    <div style="position:relative; max-width:1200px;">
      <div style="position:relative; display:block;">
        <img id="mapImg" src="{MAP_FILE}" style="width:100%; height:auto; display:block; border-radius:10px; box-shadow: 0 12px 36px rgba(0,0,0,0.6);" />
        <div id="overlay" style="position:absolute; left:0; top:0; right:0; bottom:0; pointer-events:none;"></div>
      </div>

      <div style="margin-top:8px; display:flex; gap:8px;">
        <button id="exportBtn" style="background:#6b4cff; color:white; border:none; padding:8px 12px; border-radius:8px; cursor:pointer;">Export JSON</button>
        <button id="clearBtn" style="background:#222; color:white; border:1px solid rgba(255,255,255,0.06); padding:8px 12px; border-radius:8px; cursor:pointer;">Limpar Hotspots</button>
        <div id="msg" style="color:#bdb8ff; margin-left:10px; align-self:center;"></div>
      </div>

      <textarea id="exportArea" style="width:100%; height:80px; margin-top:8px; background:#0b0b10; color:#e8eaf6; display:none;"></textarea>
    </div>

    <script>
    // Data passed from Python
    const mapping = {mapeamento_json};
    let hotspots = {hotspots_json}; // [{name, x (pct), y (pct), w (pct), h (pct), file}]
    const editMode = {str(edit_mode).lower()};
    const showLabels = {str(show_labels).lower()};

    const mapImg = document.getElementById("mapImg");
    const overlay = document.getElementById("overlay");
    const exportBtn = document.getElementById("exportBtn");
    const clearBtn = document.getElementById("clearBtn");
    const msg = document.getElementById("msg");
    const exportArea = document.getElementById("exportArea");

    // Try load saved hotspots from localStorage (prefer local changes)
    try {{
      const saved = localStorage.getItem("hotspots_saved_v1");
      if (saved) {{
        hotspots = JSON.parse(saved);
        msg.innerText = "Hotspots carregados do localStorage";
      }}
    }} catch(e){{ console.warn(e); }}

    function pct(n) {{ return (parseFloat(n) || 0).toFixed(2) + "%"; }}

    function renderHotspots() {{
      overlay.innerHTML = "";
      const rect = mapImg.getBoundingClientRect();
      const w = rect.width, h = rect.height;
      hotspots.forEach((hs, idx) => {{
        const left = (hs.x/100) * w;
        const top = (hs.y/100) * h;

        // label
        if (showLabels) {{
          const d = document.createElement("div");
          d.className = "store-label";
          d.style.position = "absolute";
          d.style.left = left + "px";
          d.style.top = top + "px";
          d.style.transform = "translate(-50%,-120%)";
          d.style.pointerEvents = "auto";
          d.style.background = "rgba(11,6,23,0.7)";
          d.style.color = "#e8eaf6";
          d.style.padding = "6px 8px";
          d.style.borderRadius = "6px";
          d.style.fontWeight = "700";
          d.style.fontSize = "14px";
          d.style.border = "1px solid rgba(180,130,255,0.12)";
          d.style.cursor = "pointer";

          d.innerText = hs.name;

          // tooltip image
          const img = document.createElement("img");
          img.src = hs.file && hs.file.length ? hs.file : (mapping[hs.name] || "");
          img.className = "hot-img";
          img.style.width = "300px";
          img.style.display = "block";
          img.style.visibility = "hidden";
          img.style.position = "absolute";
          img.style.top = "18px";
          img.style.left = "50%";
          img.style.transform = "translateX(-50%)";
          img.style.pointerEvents = "none";

          // show/hide on hover
          d.addEventListener("mouseenter", () => {{
            img.style.visibility = "visible";
          }});
          d.addEventListener("mouseleave", () => {{
            img.style.visibility = "hidden";
          }});

          d.appendChild(img);

          // if in edit mode, allow removal on right click
          if (editMode) {{
            d.addEventListener("contextmenu", (ev) => {{
              ev.preventDefault();
              if (confirm('Remover hotspot: ' + hs.name + '?')) {{
                hotspots.splice(idx,1);
                localStorage.setItem('hotspots_saved_v1', JSON.stringify(hotspots));
                renderHotspots();
              }}
            }});
          }}

          overlay.appendChild(d);
        }}
      }});
    }}

    // Initial render when image loads and on resize
    mapImg.addEventListener('load', renderHotspots);
    window.addEventListener('resize', renderHotspots);
    if (mapImg.complete) renderHotspots();

    // Click to add hotspot (only if editMode true)
    mapImg.addEventListener('click', function(e) {{
      if (!{str(edit_mode).lower()}) return;
      const r = mapImg.getBoundingClientRect();
      const xpx = e.clientX - r.left;
      const ypx = e.clientY - r.top;
      const xPct = (xpx / r.width) * 100;
      const yPct = (ypx / r.height) * 100;

      const name = prompt("Nome da loja (exatamente como no mapa / no mapeamento):");
      if (!name) return alert("Nome vazio — operação cancelada.");

      // Resolve arquivo pelo mapeamento (se existir)
      let file = "";
      if (mapping[name]) {{
        file = mapping[name];
      }}

      hotspots.push({{name: name, x: parseFloat(xPct.toFixed(2)), y: parseFloat(yPct.toFixed(2)), file: file}});
      localStorage.setItem('hotspots_saved_v1', JSON.stringify(hotspots));
      renderHotspots();
      msg.innerText = "Hotspot adicionado (salvo no localStorage). Use Export JSON para copiar.";
    }});

    // Export JSON (copy to clipboard)
    exportBtn.addEventListener('click', async () => {{
      const s = JSON.stringify(hotspots, null, 2);
      try {{
        await navigator.clipboard.writeText(s);
        msg.innerText = "Hotspots copiados para a área de transferência!";
      }} catch(e) {{
        exportArea.style.display = 'block';
        exportArea.value = s;
        msg.innerText = "Falha no clipboard — JSON aparece abaixo (copie manualmente).";
      }}
    }});

    clearBtn.addEventListener('click', () => {{
      if (!confirm("Limpar todos os hotspots do localStorage?")) return;
      hotspots = [];
      localStorage.removeItem('hotspots_saved_v1');
      renderHotspots();
      msg.innerText = "Hotspots removidos do localStorage.";
    }});

    </script>
    """

    # Render the HTML widget
    st.components.v1.html(html, height=820, scrolling=True)

# Right column also show quick list and target preview (server-side fallback)
st.markdown("---")
st.markdown("### Lista rápida de lojas mapeadas")
lst = sorted(list(mapeamento_imagens.keys()))
st.write(", ".join(lst))

st.markdown("<small style='color:#9a8cff'>Dica: ative <b>Edit Mode</b> e clique no mapa para posicionar uma loja. Depois clique em <b>Export JSON</b> e cole o JSON em um arquivo hotspots.json no repo para usar permanentemente.</small>", unsafe_allow_html=True)

# Show basic stats
st.metric("Lojas mapeadas", len(mapeamento_imagens))
imgs_found = sum(1 for v in mapeamento_imagens.values() if Path(v).exists() or Path(f"images/{v}").exists())
st.metric("Fachadas encontradas (arquivo)", imgs_found)
