import os
import requests
from bs4 import BeautifulSoup

jogadores = [
    ("Rafael", "https://www.transfermarkt.com.br/rafael/leistungsdaten/spieler/68097/saison/2024/plus/1"),
    ("Jandrei", "https://www.transfermarkt.com.br/jandrei/leistungsdaten/spieler/512344/saison/2024/plus/1"),
    ("Cédric", "https://www.transfermarkt.com.br/cedric-soares/leistungsdaten/spieler/112988/saison/2024/plus/1"),
    ("Maik", "https://www.transfermarkt.com.br/maik/leistungsdaten/spieler/1027026/saison/2024/plus/1"),
    ("Pablo Maia", "https://www.transfermarkt.com.br/pablo-maia/leistungsdaten/spieler/892089/saison/2024/plus/1"),
    ("Luan", "https://www.transfermarkt.com.br/luan-santos/leistungsdaten/spieler/574904/saison/2024/plus/1"),
    ("Negrucci", "https://www.transfermarkt.com.br/felipe-negrucci/leistungsdaten/spieler/980837/saison/2024/plus/1"),
]

def extrair_tabela(html):
    soup = BeautifulSoup(html, "html.parser")
    section = soup.find("div", class_="responsive-table")
    if not section:
        return None

    table = section.find("table")
    if not table:
        return None

    # Substitui o <thead> original por cabeçalhos fixos
    thead_html = """
    <thead>
        <tr>
            <th>Campeonato</th>
            <th>Jogos</th>
            <th>Gols</th>
            <th>Gols Sofridos</th>
            <th>Suplente utilizado</th>
            <th>Substituições</th>
            <th>Cartões amarelos</th>
            <th>Expulsões (dois amarelos)</th>
            <th>Expulsões (vermelho direto)</th>
            <th>Gols sofridos</th>
            <th>Jogos sem gols sofridos</th>
            <th>Minutos jogados</th>
        </tr>
    </thead>
    """

    # Substitui o <thead> da tabela original
    thead = table.find("thead")
    if thead:
        thead.replace_with(BeautifulSoup(thead_html, "html.parser"))
    else:
        table.insert(0, BeautifulSoup(thead_html, "html.parser"))

    return str(table)

os.makedirs("public", exist_ok=True)

for nome, url in jogadores:
    print(f"🔄 Coletando dados de {nome}...")
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        print(f"❌ Erro ao acessar página de {nome}: {e}")
        continue

    tabela_html = extrair_tabela(html)
    if not tabela_html:
        print(f"⚠️ Tabela não encontrada para {nome}")
        continue

    output_html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{nome} - Tabela de Desempenho</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
            thead th {{ position: sticky; top: 0; background-color: #f9f9f9; z-index: 1; }}
        </style>
    </head>
    <body>
        <h2>Tabela de desempenho - {nome}</h2>
        {tabela_html}
    </body>
    </html>
    """

    filename = f"public/{nome.lower().replace(' ', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output_html)

    print(f"✅ Tabela salva em {filename}")
