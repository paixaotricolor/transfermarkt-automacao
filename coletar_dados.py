import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.transfermarkt.com.br/rafael/leistungsdaten/spieler/68097/saison/2024/plus/1"
HEADERS = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

# Encontra a tabela na seção Gesamt
div = soup.find("div", id="tab-leistungsdaten-gesamt")
table = div.find("table", class_="items") if div else soup.find("table", class_="items")

if not table:
    raise Exception("Tabela não encontrada na página")

# Define os nomes das colunas manualmente com base na ordem da página
headers = [
    "Competição", "Jogos", "Gols", "Assistências", "Suplente utilizado", 
    "Substituições", "Cartões amarelos", "Expulsões (2A)", "Expulsões (R)", 
    "Gols sofridos", "Jogos sem sofrer gols", "Minutos jogados"
]

# Extrai as linhas da tabela
rows = table.find("tbody").find_all("tr")

html_rows = ""
for row in rows:
    # Primeira célula (competição) é um <th>, o resto são <td>
    th = row.find("th")
    competencia = th.get_text(strip=True) if th else ""
    td_values = [td.get_text(strip=True) for td in row.find_all("td")]

    if not td_values:
        continue  # pula linhas vazias

    all_values = [competencia] + td_values
    html_cells = "".join(f"<td>{v}</td>" for v in all_values)
    html_rows += f"<tr>{html_cells}</tr>\n"

# Monta a tabela HTML
html_table = "<table border='1' style='width:100%;border-collapse:collapse;text-align:center;'>\n<thead><tr>"
for h in headers:
    html_table += f"<th>{h}</th>"
html_table += "</tr></thead>\n<tbody>\n"
html_table += html_rows
html_table += "</tbody>\n</table>"

# Salva o arquivo HTML
os.makedirs("public", exist_ok=True)
with open("public/tabela_desempenho_completo.html", "w", encoding="utf-8") as f:
    f.write(html_table)

print("✅ Tabela final salva com cabeçalhos e dados alinhados.")
