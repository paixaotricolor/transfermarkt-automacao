import os
import requests
from bs4 import BeautifulSoup
import time
import random

jogadores = [
    ("Rafael", "https://www.transfermarkt.com.br/rafael/leistungsdaten/spieler/68097/saison/2024/plus/1"),
    ("Jandrei", "https://www.transfermarkt.com.br/jandrei/leistungsdaten/spieler/512344/saison/2024/plus/1"),
    # ... continue com os demais jogadores
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

# Mapeamento de títulos originais -> nomes desejados
nomes_personalizados = {
    "Wettbewerb": "Campeonato",
    "Spiele": "Jogos",
    "Tore": "Gols",
    "Gegentore": "Gols sofridos",
    "Ein": "Suplente utilizado",
    "Aus": "Substituições",
    "Gelbe Karten": "Cartões amarelos",
    "Gelb-Rote Karten": "Expulsões (dois amarelos)",
    "Rote Karten": "Expulsões (vermelho direto)",
    "Zu-Null-Spiele": "Jogos sem gols sofridos",
    "Minuten": "Minutos jogados"
}

def get_html(url):
    headers = {"User-Agent": random.choice(user_agents)}
    for attempt in range(5):
        try:
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"⚠️ Tentativa {attempt+1} falhou para {url}: {e}")
            time.sleep(2)
    return None

def extrair_tabela(html):
    soup = BeautifulSoup(html, "html.parser")
    section = soup.find("div", class_="responsive-table")
    if not section:
        return None

    table = section.find("table")
    if not table:
        return None

    # Extrai cabeçalho real
    thead = table.find("thead")
    headers = []
    if thead:
        header_cells = thead.find_all("th", recursive=True)
        headers = [cell.get_text(strip=True) for cell in header_cells]

    # Aplica nomes personalizados se existirem
    headers_personalizados = [nomes_personalizados.get(h, h) for h in headers]

    # Extrai linhas
    body = table.find("tbody")
    linhas = []
    if body:
        for row in body.find_all("tr", recursive=False):
            cells = row.find_all(["td", "th"])
            valores = [cell.get_text(strip=True) for cell in cells]
            if valores:
                linhas.append(valores)

    return headers_personalizados, linhas

os.makedirs("public", exist_ok=True)

for nome, url in jogadores:
    print(f"🔄 Coletando dados de {nome}...")
    html = get_html(url)
    if not html:
        print(f"❌ Erro ao acessar página de {nome}")
        continue

    cabecalhos, linhas = extrair_tabela(html)
    if not linhas:
        print(f"⚠️ Tabela não encontrada ou vazia para {nome}")
        continue

    # Monta a tabela manualmente com cabeçalhos personalizados
    tabela_html = "<table>\n<thead><tr>" + "".join(f"<th>{col}</th>" for col in cabecalhos) + "</tr></thead>\n<tbody>\n"
    for linha in linhas:
        tabela_html += "<tr>" + "".join(f"<td>{valor}</td>" for valor in linha) + "</tr>\n"
    tabela_html += "</tbody></table>"

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
