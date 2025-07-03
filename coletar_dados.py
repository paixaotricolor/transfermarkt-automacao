import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.transfermarkt.com.br/rafael/leistungsdaten/spieler/68097/saison/2024/plus/1"
HEADERS = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

# Captura a seção da tabela completa (Gesamt)
div = soup.find("div", id="tab-leistungsdaten-gesamt")
table = div.find("table", class_="items") if div else soup.find("table", class_="items")

# Captura a linha de títulos (segunda linha do thead)
header_rows = table.find("thead").find_all("tr")
header_cells = header_rows[1].find_all(["th", "td"])  # a linha real dos títulos é a 2ª
headers = [cell.get_text(strip=True) for cell in header_cells]

# Captura todas as linhas de dados (tbody)
rows = table.find("tbody").find_all("tr")

html_rows = ""
for row in rows:
    # Pega a célula com o nome da competição (primeira coluna é th)
    competencia = row.find("th").get_text(strip=True)

    # Depois pega o resto das colunas
    cols = row.find_all("td")
    values = [col.get_text(strip=True) for col in cols]

    # Junta a primeira coluna (competição) com as demais
    all_cells = [competencia] + values
    html_cells = "".join(f"<td>{cell}</td>" for cell in all_cells)
    html_rows += f"<tr>{html_cells}</tr>\n"

# Constrói a tabela HTML final
html_table = "<table border='1' style='width:100%;border-collapse:collapse;text-align:center;'>\n<thead>\n<tr>"
for h in headers:
    html_table += f"<th>{h}</th>"
html_table += "</tr>\n</thead>\n<tbody>\n"
html_table += html_rows
html_table += "</tbody>\n</table>"

# Salva o HTML no diretório public
os.makedirs("public", exist_ok=True)
with open("public/tabela_desempenho_completo.html", "w", encoding="utf-8") as f:
    f.write(html_table)

print("✅ Tabela completa corrigida e salva
