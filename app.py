# app.py
import streamlit as st
import os
import json
from streamlit.components.v1 import html as components_html

st.set_page_config(page_title="Mapa das Lojas", page_icon="🏪", layout="wide")

st.markdown("""
# 🗺️ Mapa das Lojas
""")

# Encontrar imagens na raiz do projeto (exceto o mapa)
image_files = sorted([f for f in os.listdir('.') if f.lower().endswith(('.jpg','.jpeg','.png'))])
map_name = "mapa.jpg"
if map_name in image_files:
    image_files.remove(map_name)

# Aviso se mapa não existir
if not os.path.exists(map_name):
    st.error("Arquivo 'mapa.jpg' não encontrado na raiz do projeto. Coloque o mapa com esse nome e recarregue.")
    st.stop()

# Sidebar com instruções e lista de imagens detectadas
with st.sidebar:
    st.markdown("## ⚙️ Instruções rápidas")
    st.markdown("""
- Pressione **E** para alternar *Editor / Visualização*.  
- No **Editor**, clique no mapa para adicionar um hotspot (será pedido o nome do arquivo da fachada).  
- Arraste hotspots para ajustar.  
- Pressione **D** para apagar o último hotspot.  
- No modo **Visualização**, passe o mouse sobre o nome para ver a fachada.  
- Use **Export** dentro do editor para copiar JSON das posições (guardar externamente).
""")
    st.markdown("---")
    st.markdown("### 🖼️ Imagens detectadas")
    if image_files:
        for f in image_files:
            st.write(f"- `{f}`")
    else:
        st.write("Nenhuma imagem encontrada (exceto o mapa).")

# ==== Gerar HTML/JS que roda o mapa com hotspots e salva no localStorage ====
images_json = json.dumps(image_files)  # lista de nomes de arquivo
initial_hotspots = "[]"  # vazio por padrão (editor salva no localStorage do navegador)

html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Mapa interativo</title>
<style>
  :root {{
    --bg: #0b0f14;
    --card: rgba(20,18,30,0.9);
    --accent: linear-gradient(135deg, #7b2ff7 0%, #b83cff 100%);
    --muted: rgba(255,255,255,0.06);
    --text: #e6e6e6;
  }}
  html,body {{
    margin:0; padding:0; height:100%; background:var(--bg); color:var(--text); font-family:Inter, system-ui, sans-serif;
  }}
  .wrap {{
    box-sizing:border-box;
    padding:16px;
    display:flex;
    gap:18px;
    height:calc(100vh - 32px);
  }}
  .map-panel {{
    flex:1.6;
    background: linear-gradient(180deg, rgba(255,255,255,0.02), transparent);
    border-radius:12px;
    padding:12px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.6);
    position:relative;
    overflow:hidden;
  }}
  .side-panel {{
    flex:0.9;
    min-width:300px;
    background:var(--card);
    border-radius:12px;
    padding:16px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.6);
    display:flex;
    flex-direction:column;
    gap:12px;
  }}
  .map-wrapper {{
    position:relative;
    width:100%;
    height:calc(100% - 10px);
    display:flex;
    align-items:center;
    justify-content:center;
  }}
  #map {{
    max-width:100%;
    max-height:100%;
    width:auto;
    height:auto;
    object-fit:contain;
    border-radius:8px;
    box-shadow: 0 8px 24px rgba(10,10,20,0.6);
    display:block;
  }}
  #layer {{
    position:absolute;
    left:0; top:0;
    pointer-events:none;
  }}
  .hotspot {{
    position:absolute;
    transform:translate(-50%,-50%);
    pointer-events:auto;
    cursor:grab;
    padding:6px 10px;
    border-radius:8px;
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
    color:var(--text);
    font-weight:600;
    font-size:13px;
    border:1px solid rgba(255,255,255,0.06);
    transition:transform .12s ease, box-shadow .12s ease;
    backdrop-filter: blur(4px);
  }}
  .hotspot:active {{ cursor:grabbing; }}
  .hotspot:hover {{
    transform:translate(-50%,-50%) scale(1.06);
    box-shadow: 0 8px 24px rgba(123,47,247,0.18);
    z-index:40;
  }}
  .label-badge {{
    display:inline-block;
    padding:4px 8px;
    border-radius:6px;
    background:rgba(0,0,0,0.45);
    color:var(--text);
    border:1px solid rgba(255,255,255,0.04);
  }}
  .preview-box {{
    margin-top:6px;
    border-radius:10px;
    overflow:hidden;
    background:#000;
    padding:8px;
    text-align:center;
  }}
  .preview-box img {{
    width:100%;
    height:auto;
    display:block;
    border-radius:8px;
  }}
  .controls {{
    display:flex;
    gap:8px;
    flex-wrap:wrap;
  }}
  .btn {{
    padding:8px 12px;
    border-radius:8px;
    background:linear-gradient(90deg,#6a00f4,#b83cff);
    color:white;
    border:0;
    font-weight:700;
    cursor:pointer;
    box-shadow:0 8px 18px rgba(184,60,255,0.12);
  }}
  .btn.ghost {{
    background:transparent;
    border:1px solid rgba(255,255,255,0.06);
    color:var(--text);
    box-shadow:none;
  }}
  .muted {{
    color: #bfc7cf;
    font-size:13px;
  }}
  .small {{
    font-size:12px;
    opacity:0.9;
  }}
  .export-area {{
    width:100%;
    height:100px;
    background: rgba(255,255,255,0.02);
    border-radius:8px;
    padding:8px;
    color:var(--text);
    font-family:monospace;
    font-size:12px;
    overflow:auto;
    border:1px dashed rgba(255,255,255,0.03);
  }}
  .legend-list {{
    display:flex; flex-direction:column; gap:6px;
    max-height:220px; overflow:auto; padding-right:6px;
  }}
  .legend-item {{
    display:flex; gap:8px; align-items:center; justify-content:space-between;
    padding:6px 8px; background: rgba(255,255,255,0.02); border-radius:6px;
  }}
  .legend-item .name {{ font-weight:600; color:var(--text); font-size:13px; }}
  .hint {{ font-size:13px; color:#9aa6b2; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="map-panel">
    <div class="map-wrapper">
      <img id="map" src="{map_name}" crossorigin="anonymous" alt="map">
      <div id="layer"></div>
    </div>
    <div class="muted small" style="margin-top:8px;">
      Pressione <strong>E</strong> para alternar <strong>Editor</strong>. No editor: clique para adicionar (escreva nome exato do arquivo, ex: <em>Nluzzi.jpeg</em>).
    </div>
  </div>

  <div class="side-panel">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-weight:800; font-size:16px;">Mapa — Hotspots</div>
        <div class="hint">Hover sobre um nome no mapa para ver a foto.</div>
      </div>
      <div>
        <button id="toggleEditor" class="btn ghost">Editor</button>
      </div>
    </div>

    <div style="margin-top:8px;">
      <div style="font-weight:700; margin-bottom:6px;">Arquivos de fachadas detectados</div>
      <div class="legend-list" id="filesList"></div>
    </div>

    <div style="margin-top:8px;">
      <div style="font-weight:700; margin-bottom:6px;">Ações</div>
      <div class="controls">
        <button id="exportBtn" class="btn">Exportar JSON</button>
        <button id="clearBtn" class="btn ghost">Limpar todos</button>
        <button id="undoBtn" class="btn ghost">Desfazer último (D)</button>
      </div>
    </div>

    <div style="margin-top:8px;">
      <div style="font-weight:700; margin-bottom:6px;">Preview</div>
      <div class="preview-box" id="previewBox">
        <div class="muted">Passe o mouse sobre uma loja (hotspot) no mapa para abrir sua fachada aqui.</div>
      </div>
    </div>

    <div style="margin-top:8px;">
      <div style="font-weight:700; margin-bottom:6px;">JSON export (copie para salvar)</div>
      <div id="exportArea" class="export-area" contenteditable="false"></div>
    </div>
  </div>
</div>

<script>
const files = {images_json};
const layer = document.getElementById('layer');
const mapEl = document.getElementById('map');
const previewBox = document.getElementById('previewBox');
const filesList = document.getElementById('filesList');
const exportArea = document.getElementById('exportArea');
const toggleEditorBtn = document.getElementById('toggleEditor');
const exportBtn = document.getElementById('exportBtn');
const clearBtn = document.getElementById('clearBtn');
const undoBtn = document.getElementById('undoBtn');

let editor = false;
let hotspots = JSON.parse(localStorage.getItem('hotspots_v1') || '[]'); // [{name, xPct, yPct, wPct, hPct, file}]
let dragging = null;

// populate files list
files.forEach(f => {
  const d = document.createElement('div');
  d.className = 'legend-item';
  d.innerHTML = `<div style="display:flex; gap:8px; align-items:center;"><div style="width:36px; height:28px; background:#111; border-radius:6px; display:flex;align-items:center;justify-content:center;color:#9aa6b2;font-size:11px">IMG</div><div class="name">${f}</div></div><div class="small">${f.split('.').pop().toUpperCase()}</div>`;
  filesList.appendChild(d);
});

function save() {{
  localStorage.setItem('hotspots_v1', JSON.stringify(hotspots));
  render();
  exportArea.textContent = JSON.stringify(hotspots, null, 2);
}}

function clearHotspots() {{
  hotspots = [];
  save();
}}

function undoHotspot() {{
  hotspots.pop();
  save();
}}

function createHotspotElement(hs, idx) {{
  const div = document.createElement('div');
  div.className = 'hotspot';
  div.dataset.idx = idx;
  div.textContent = hs.name;
  div.style.left = (hs.xPct) + '%';
  div.style.top = (hs.yPct) + '%';
  div.style.zIndex = hs.z || 20;

  // hover preview
  div.addEventListener('mouseenter', () => {{
    showPreview(hs.file, hs.name);
  }});
  div.addEventListener('mouseleave', () => {{
    hidePreview();
  }});

  // drag (editor only)
  div.addEventListener('mousedown', (ev) => {{
    if (!editor) return;
    dragging = {{el: div, startX: ev.clientX, startY: ev.clientY, idx}};
    div.style.cursor = 'grabbing';
    ev.preventDefault();
  }});

  return div;
}}

function render() {{
  layer.innerHTML = '';
  const r = mapEl.getBoundingClientRect();
  layer.style.left = r.left + 'px';
  layer.style.top = r.top + 'px';
  layer.style.width = r.width + 'px';
  layer.style.height = r.height + 'px';
  layer.style.pointerEvents = editor ? 'auto' : 'none';

  hotspots.forEach((hs, i) => {{
    const el = createHotspotElement(hs, i);
    layer.appendChild(el);
  }});
  exportArea.textContent = JSON.stringify(hotspots, null, 2);
}}

function showPreview(file, name) {{
  if (!file) return;
  previewBox.innerHTML = `<div style="font-weight:700; margin-bottom:8px;">📍 ${name}</div><img src="${file}" onerror="this.style.display='none';">`;
}}

function hidePreview() {{
  previewBox.innerHTML = `<div class="muted">Passe o mouse sobre uma loja (hotspot) no mapa para abrir sua fachada aqui.</div>`;
}}

// add hotspot on click (editor)
mapEl.addEventListener('click', (e) => {{
  if (!editor) return;
  const r = mapEl.getBoundingClientRect();
  const xpx = e.clientX - r.left;
  const ypx = e.clientY - r.top;
  const xPct = (xpx / r.width) * 100;
  const yPct = (ypx / r.height) * 100;

  // ask for filename (helpful: show list in console)
  let file = prompt("Nome do arquivo da fachada (caso exista). Ex: 'Nluzzi.jpeg'.\\nArquivos detectados:\\n" + files.join('\\n'));
  if (!file) return;
  file = file.trim();

  // find matching file (case-insensitive)
  const found = files.find(f => f.toLowerCase() === file.toLowerCase());
  const fileToUse = found || file; // even if not found, user can type a path

  let name = prompt("Texto que aparecerá no mapa (ex: Nluzzi). Se deixar vazio, usarei o nome do arquivo:");
  if (!name) name = fileToUse;

  hotspots.push({{name: name, xPct: Number(xPct.toFixed(2)), yPct: Number(yPct.toFixed(2)), file: fileToUse}});
  save();
}});

// drag logic (mouse move/up)
window.addEventListener('mousemove', (e) => {{
  if (!dragging) return;
  const el = dragging.el;
  const idx = dragging.idx;
  const r = mapEl.getBoundingClientRect();
  const xpx = e.clientX - r.left;
  const ypx = e.clientY - r.top;
  const xPct = Math.max(0, Math.min(100, (xpx / r.width) * 100));
  const yPct = Math.max(0, Math.min(100, (ypx / r.height) * 100));
  hotspots[idx].xPct = Number(xPct.toFixed(2));
  hotspots[idx].yPct = Number(yPct.toFixed(2));
  render();
}});

window.addEventListener('mouseup', (e) => {{
  if (dragging) {{
    try {{ dragging.el.style.cursor = 'grab'; }}catch(e){{}}
    dragging = null;
    save();
  }}
}});

// keyboard shortcuts
window.addEventListener('keydown', (e) => {{
  if (e.key.toLowerCase() === 'e') {{
    editor = !editor;
    toggleEditorBtn.classList.toggle('ghost', !editor);
    toggleEditorBtn.textContent = editor ? 'Editor (ON)' : 'Editor';
    render();
  }}
  if (e.key.toLowerCase() === 'd') {{
    // delete last
    undoHotspot();
  }}
}});

// buttons
toggleEditorBtn.addEventListener('click', () => {{
  editor = !editor;
  toggleEditorBtn.classList.toggle('ghost', !editor);
  toggleEditorBtn.textContent = editor ? 'Editor (ON)' : 'Editor';
  render();
}});

exportBtn.addEventListener('click', () => {{
  const txt = JSON.stringify(hotspots, null, 2);
  exportArea.textContent = txt;
  navigator.clipboard && navigator.clipboard.writeText(txt).then(() => {{
    exportBtn.textContent = 'Copiado!';
    setTimeout(()=> exportBtn.textContent = 'Exportar JSON', 1300);
  }}).catch(()=>{{ exportBtn.textContent = 'Exportar JSON'; }});
}});

clearBtn.addEventListener('click', () => {{
  if (confirm('Remover todos os hotspots?')) {{
    clearHotspots();
  }}
}});

undoBtn.addEventListener('click', () => {{
  undoHotspot();
}});

// initial render
render();
</script>
</body>
</html>
"""

# Render inside Streamlit; height tuned for large map
components_html(html, height=900, scrolling=True)

st.markdown("---")
st.caption("Futurista, tema escuro com toques roxos — editor local salva posições no navegador (localStorage).")
