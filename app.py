import streamlit as st
import streamlit.components.v1 as components
import os
import json   #  <<<<<<<<<<  ESSENCIAL — estava faltando!

# Configuração da página
st.set_page_config(
    page_title="Mapa Interativo de Lojas",
    page_icon="🏪",
    layout="wide"
)

# Mapeamento: Nome da loja -> Nome do arquivo
mapeamento_imagens = {
    # Rua Trajano - Esquerda
    "Magazine Luiza": "Magazine Luiza.jpeg",
    "Cia do H": "Cia do Homem.jpeg",
    "Damiller": "Damyller.jpeg",
    "Pop Dente": "Pop dente - Lupo.jpeg",
    "Lupo": "Pop dente - Lupo.jpeg",
    "ViVo": "Lojas Vivo.jpeg",
    "Bazar das chaves": "Bazar das chave - Panvel.jpeg",
    "Panvel": "Bazar das chave - Panvel.jpeg",
    
    # Rua Trajano - Direita Superior
    "Nfuzzi": "Nluzzi.jpeg",
    "Para Alugar IBAGY": "Aluga Ibagy.jpeg",
    "Botton Utilidades": "Botton Utilidades.jpeg",
    "bob's": "Bob's.jpeg",
    "Artigos Religiosos": "Itens Religiosos.jpeg",
    "Achadinhos": "Achadinhos.jpeg",
    "U Mi Acessórios": "U mi Acessorios.jpeg",
    "Vonny cosmeticos": "Vonny cosmeticos.jpeg",
    
    # Rua Trajano - Direita Inferior
    "Café do Frank": "Café do Frank.jpeg",
    "Massa Viva": "Massa Viva.jpeg",
    "Floripa Implante": "Foripa Implantes.jpeg",
    "Preço Popular": "Preço popular.jpeg",
    "Brasil Cacau": "Brasil cacau.jpeg",
    "Cia Do H": "Cia do Homem 1.jpeg",
    "Da Praça": "Da Praça.jpeg",
    
    # Rua Felipe Schmidt - Esquerda
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
    
    # Rua Felipe Schmidt - Direita
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

# Criar HTML interativo com o mapa
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f8f9fa;
        }}
        
        .container {{
            display: flex;
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .mapa-wrapper {{
            flex: 1.2;
            position: relative;
            background: white;
            border-radius: 15px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
            padding: 20px;
        }}
        
        .foto-wrapper {{
            flex: 1;
            background: white;
            border-radius: 15px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
            padding: 20px;
            position: sticky;
            top: 20px;
            height: fit-content;
        }}
        
        #mapa {{
            width: 100%;
            height: auto;
            display: block;
            border-radius: 10px;
        }}
        
        .store-name {{
            position: absolute;
            cursor: pointer;
            padding: 4px 8px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            transition: all 0.3s ease;
            border: 2px solid transparent;
            white-space: nowrap;
        }}
        
        .store-name:hover {{
            background: #ff4b4b;
            color: white;
            transform: scale(1.15);
            z-index: 100;
            box-shadow: 0 4px 12px rgba(255, 75, 75, 0.4);
            border-color: #ff4b4b;
        }}
        
        .foto-container {{
            text-align: center;
        }}
        
        .foto-container img {{
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            margin-top: 20px;
        }}
        
        .store-title {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .store-title h2 {{
            margin: 0;
            font-size: 24px;
        }}
        
        .placeholder {{
            color: #666;
            text-align: center;
            padding: 40px;
            font-size: 16px;
        }}
        
        .instructions {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="mapa-wrapper">
            <h2 style="margin-top: 0; color: #333;">🗺️ Mapa Interativo</h2>
            <div style="position: relative; display: inline-block;">
                <img id="mapa" src="mapa.jpg" alt="Mapa das Lojas">

<script>
    const mapeamento = {json.dumps(mapeamento_imagens, ensure_ascii=False)};
    
    function mostrarLoja(nomeLoja) {{
        const nomeArquivo = mapeamento[nomeLoja];
        
        if (nomeArquivo) {{
            document.getElementById('foto-content').innerHTML = `
                <div class="foto-container">
                    <div class="store-title">
                        <h2>📍 ${{nomeLoja}}</h2>
                    </div>
                    <img src="${{nomeArquivo}}" alt="${{nomeLoja}}">
                </div>
            `;
        }} else {{
            document.getElementById('foto-content').innerHTML = `
                <div class="placeholder">
                    ❌ Loja não mapeada: <strong>${{nomeLoja}}</strong>
                </div>
            `;
        }}
    }}
</script>

</body>
</html>
"""

# Renderizar o HTML
components.html(html_code, height=900, scrolling=True)

st.markdown("---")
st.caption("🏢 Mapa Interativo de Lojas do Centro | Desenvolvido para apresentação executiva")
