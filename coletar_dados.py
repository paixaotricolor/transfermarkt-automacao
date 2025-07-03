import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.transfermarkt.com.br/rafael/leistungsdaten/spieler/68097/saison/2024/plus/1#gesamt"
HEADERS = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

# Acessa a seção "Gesamt" (tabela completa)
div = soup.find("div", id="tab-leistungsdaten-gesamt")
table = div.find("table", class_="items") if div else soup.find("table", class_="items")

if not table:
    raise Exception("Tabela não encontrada na página")

# 🧠 Encontra a linha de cabeçalho com mais colunas (ignora linhas de agrupamento)
thead_rows = table.find("thead").find_all("tr")
header_row = max(thead_rows, key=lambda tr: len(tr.find_all(["th", "td"])))
headers = [cell.get_text(strip=True) for cell in header_row.find_all(["th", "td"])]

# 🔄 Monta linhas do corpo da tabela
tbody_rows = table.find("tbody").find_all("tr")
html_rows = ""
for row in tbody_rows:
    th = row.find("th")  # normalmente a competição
    competencia = th.get_text(strip=True) if th else ""
    
    td_values = [td.get_text(strip=True) for td in row.find_all("td")]
    full_row = [competencia] + td_values if competencia else td_values
    html_cells = "".join(f"<td>{cell}</td>" for cell in full_row)
    html_rows += f"<tr>{html_cells}</tr>\n"

# 🧱 Gera a tabela HTML final
html_table = "<table border='1' style='width:100%;border-collapse:collapse;text-align:center;'>\n<thead>\n<tr>"
for h in headers:
