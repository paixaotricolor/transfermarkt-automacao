import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.transfermarkt.com.br/rafael/leistungsdaten/spieler/68097/saison/2024/plus/1"
HEADERS = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

# Captura a seção completa de desempenho (Gesamt)
div = soup.find("div", id="tab-leistungsdaten-gesamt")
table = div.find("table", class_="items") if div else soup.find("table", class_="items")

# Captura todos os cabeçalhos da tabela
header_cells = table.find("thead").find_all("th")
headers = [th.get_text(strip=True) for th in header_cells]

# Captura todas as linhas do corpo
rows = table.find("tbody").find_all("tr")

# Monta linhas HTML
html_rows = ""
for row in rows:
    cols = row.find_all("td")
    if not cols:
        continue
    # extrai todo texto, col por col
    values = [c.get_text(strip=True) for c in cols]
    cells = "".join(f"<td>{v}</td>" for v in values)
    html_rows += f"<tr>{cells}</tr>\n"

# Constrói a tabela HTML completa
html_table = "<table border='1' style='width:100%;border-collapse:collapse;text-align:center;'>\n<thead>\n<tr>"
for h in headers:
    html_table += f"<th>{h}</th>"
html_table += "</tr>\n</thead>\n<tbody>\n"
html_table += html_rows
html_table += "</tbody>\n</table>"

os.makedirs("public", exist_ok=True)
with open("public/tabela_desempenho_completo.html", "w", encoding="utf-8") as f:
    f.write(html_table)

print("✅ Tabela completa salva em public/tabela_desempenho_completo.html")
