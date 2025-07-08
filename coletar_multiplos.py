import os
import requests
from bs4 import BeautifulSoup
import time
import random

jogadores = [
    ("Rafael", "https://www.transfermarkt.com.br/rafael/leistungsdaten/spieler/68097/saison/2024/plus/1"),
    ("Jandrei", "https://www.transfermarkt.com.br/jandrei/leistungsdaten/spieler/512344/saison/2024/plus/1"),
    ("Young", "https://www.transfermarkt.com.br/young/leistungsdaten/spieler/894532/saison/2024/plus/1"),
    ("Leandro Mathias", "https://www.transfermarkt.com.br/leandro-mathias/leistungsdaten/spieler/838386/saison/2024/plus/1"),
    ("Alan Franco", "https://www.transfermarkt.com.br/alan-franco/leistungsdaten/spieler/503343/saison/2024/plus/1"),
    ("Ferraresi", "https://www.transfermarkt.com.br/nahuel-ferraresi/leistungsdaten/spieler/466336/saison/2024/plus/1"),
    ("Sabino", "https://www.transfermarkt.com.br/sabino/leistungsdaten/spieler/546033/saison/2024/plus/1"),
    ("Matheus Belém", "https://www.transfermarkt.com.br/matheus-belem/leistungsdaten/spieler/980825/saison/2024/plus/1"),
    ("Arboleda", "https://www.transfermarkt.com.br/robert-arboleda/leistungsdaten/spieler/139867/saison/2024/plus/1"),
    ("Igão", "https://www.transfermarkt.com.br/igao/leistungsdaten/spieler/1223221/saison/2024/plus/1"),
    ("Wendell", "https://www.transfermarkt.com.br/wendell/leistungsdaten/spieler/228433/saison/2024/plus/1"),
    ("Enzo Díaz", "https://www.transfermarkt.com.br/enzo-dias/leistungsdaten/spieler/540458/saison/2024/plus/1"),
    ("Patryck", "https://www.transfermarkt.com.br/patryck/leistungsdaten/spieler/662326/saison/2024/plus/1"),
    ("Moreira", "https://www.transfermarkt.com.br/joao-moreira/leistungsdaten/spieler/929866/saison/2024/plus/1"),
    ("Cédric", "https://www.transfermarkt.com.br/cedric-soares/leistungsdaten/spieler/112988/saison/2024/plus/1"),
    ("Maik", "https://www.transfermarkt.com.br/maik/leistungsdaten/spieler/1027026/saison/2024/plus/1"),
    ("Pablo Maia", "https://www.transfermarkt.com.br/pablo-maia/leistungsdaten/spieler/892089/saison/2024/plus/1"),
    ("Luan", "https://www.transfermarkt.com.br/luan-santos/leistungsdaten/spieler/574904/saison/2024/plus/1"),
    ("Negrucci", "https://www.transfermarkt.com.br/felipe-negrucci/leistungsdaten/spieler/980837/saison/2024/plus/1"),
    ("Luiz Gustavo", "https://www.transfermarkt.com.br/luiz-gustavo/leistungsdaten/spieler/10471/saison/2024/plus/1"),
    ("Marcos Antônio", "https://www.transfermarkt.com.br/marcos-antonio/leistungsdaten/spieler/468301/saison/2024/plus/1"),
    ("Rodriguinho", "https://www.transfermarkt.com.br/rodriguinho/leistungsdaten/spieler/743593/saison/2024/plus/1"),
    ("Bobadilla", "https://www.transfermarkt.com.br/damian-bobadilla/leistungsdaten/spieler/861852/saison/2024/plus/1"),
    ("Alisson", "https://www.transfermarkt.com.br/alisson/leistungsdaten/spieler/229736/saison/2024/plus/1"),
    ("Oscar", "https://www.transfermarkt.com.br/oscar/leistungsdaten/spieler/85314/saison/2024/plus/1"),
    ("Matheus Alves", "https://www.transfermarkt.com.br/matheus-alves/leistungsdaten/spieler/1127813/saison/2024/plus/1"),
    ("Ferreirinha", "https://www.transfermarkt.com.br/ferreirinha/leistungsdaten/spieler/689017/saison/2024/plus/1"),
    ("Lucca", "https://www.transfermarkt.com.br/lucca/leistungsdaten/spieler/1269378/saison/2024/plus/1"),
    ("Lucas Ferreira", "https://www.transfermarkt.com.br/lucas-ferreira/leistungsdaten/spieler/1219849/saison/2024/plus/1"),
    ("Lucas Moura", "https://www.transfermarkt.com.br/lucas-moura/leistungsdaten/spieler/77100/saison/2024/plus/1"),
    ("Henrique Carmo", "https://www.transfermarkt.com.br/henrique-carmo/leistungsdaten/spieler/1009031/saison/2024/plus/1"),
    ("Luciano", "https://www.transfermarkt.com.br/luciano/leistungsdaten/spieler/223560/saison/2024/plus/1"),
    ("Ryan Francisco", "https://www.transfermarkt.com.br/ryan-francisco/leistungsdaten/spieler/1202387/saison/2024/plus/1"),
    ("André Silva", "https://www.transfermarkt.com.br/andre-silva/leistungsdaten/spieler/565232/saison/2024/plus/1"),
    ("Calleri", "https://www.transfermarkt.com.br/jonathan-calleri/leistungsdaten/spieler/284727/saison/2024/plus/1"),
    ("Juan Dinenno", "https://www.transfermarkt.com.br/juan-dinenno/leistungsdaten/spieler/288786/saison/2024/plus/1")
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

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

def extrair_linhas_tabela(html):
    soup = BeautifulSoup(html, "html.parser")
    section = soup.find("div", class_="responsive-table")
    if not section:
        return []

    table = section.find("table")
    if not table:
        return []

    body_rows = table.find("tbody").find_all("tr", recursive=False)

    linhas = []
    for row in body_rows:
        cells = row.find_all(["td", "th"])
        valores = [cell.get_text(strip=True) for cell in cells]
        if valores:
            linhas.append(valores)
    return linhas

# Cabeçalhos manuais com base no padrão desejado
cabecalhos_finais = [
    "Campeonato", "Jogos", "Gols", "Gols sofridos", "Suplente utilizado",
    "Substituições", "Cartões amarelos", "Expulsões (dois amarelos)",
    "Expulsões (vermelho direto)", "Jogos sem gols sofridos", "Minutos jogados"
]

os.makedirs("public", exist_ok=True)

for nome, url in jogadores:
    print(f"🔄 Coletando dados de {nome}...")
    html = get_html(url)
    if not html:
        print(f"❌ Erro ao acessar página de {nome}")
        continue

    linhas = extrair_linhas_tabela(html)
    if not linhas:
        print(f"⚠️ Tabela não encontrada para {nome}")
        continue

    # Constrói HTML da tabela com cabeçalhos fixos
    tabela_html = "<table>\n<thead><tr>" + "".join(f"<th>{col}</th>" for col in cabecalhos_finais) + "</tr></thead>\n<tbody>\n"
    for linha in linhas:
        tabela_html += "<tr>" + "".join(f"<td>{valor}</td>" for valor in linha[:len(cabecalhos_finais)]) + "</tr>\n"
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
