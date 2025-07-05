import requests
from bs4 import BeautifulSoup
import os

HEADERS = {"User-Agent": "Mozilla/5.0"}

def extrair_tabela(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    div = soup.find("div", id="tab-leistungsdaten-gesamt")
    table = div.find("table", class_="items") if div else None
    if not table:
        raise Exception(f"Tabela não encontrada em {url}")

    # Extrai os cabeçalhos
    header_cells = table.find("thead").find_all("th")
    headers = [th.get_text(strip=True) for th in header_cells if th.get_text(strip=True)]

    # Extrai as linhas de dados
    rows = table.find("tbody").find_all("tr")
    html_rows = ""
    for row in rows:
        cols = row.find_all("td")
        if not cols:
            continue

        # Primeira coluna com nome da competição (ignorando ícones)
        competencia_td = cols[0].find_all("td")
        competencia = cols[0].get_text(strip=True)
        values = [competencia] + [td.get_text(strip=True) for td in cols[1:]]

        cells = "".join(f"<td>{v}</td>" for v in values)
        html_rows += f"<tr>{cells}</tr>\n"

    # Monta a tabela HTML
    html_table = "<table border='1' style='width:100%;border-collapse:collapse;text-align:center;'>\n<thead>\n<tr>"
    for h in headers:
        html_table += f"<th>{h}</th>"
    html_table += "</tr>\n</thead>\n<tbody>\n"
    html_table += html_rows
    html_table += "</tbody>\n</table>"

    return html_table

# Cria pasta de saída
os.makedirs("public", exist_ok=True)

# Lê a lista de jogadores
with open("jogadores.txt", "r", encoding="utf-8") as file:
    linhas = file.readlines()

for linha in linhas:
    if not linha.strip():
        continue
    nome, url = linha.strip().split(",", 1)
    nome_arquivo = nome.strip().lower().replace(" ", "_") + ".html"
    try:
        tabela_html = extrair_tabela(url.strip())
        with open(f"public/{nome_arquivo}", "w", encoding="utf-8") as f:
            f.write(tabela_html)
        print(f"✅ Tabela de {nome.strip()} salva com sucesso.")
    except Exception as e:
        print(f"⚠️ Erro ao processar {nome.strip()}: {e}")
