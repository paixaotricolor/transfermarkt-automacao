import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.transfermarkt.com.br/rafael/leistungsdaten/spieler/68097/saison/2024/plus/1"
HEADERS = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

# Tenta localizar a seção da tabela completa (Gesamt)
div = soup.find("div", id="tab-leistungsdaten-gesamt")
table = div.find("table", class_="items") if div else soup.find("table", class_="items")

if not table:
    raise Exception("Tabela não encontrada na página")

# Cabeçalhos desejados (você pode adaptar se quiser menos colunas)
headers = [
    "Competição", "Jogos", "Gols", "Assistências", "Suplente utilizado",
    "Substituições", "Cartões amarelos", "Expulsões (2A)", "Expulsões (R)",
    "Gols sofridos", "Jogos sem sofrer gols", "Minutos jogados"
]

rows = table.find("tbody").find_all("tr")
html_rows = ""

for row in rows:
    tds = row.find_all("td")
    if len(tds) < 4:
        continue  # ignora linhas incompletas ou de separação

    # A competição está no 3º <td> (índice 2)
    competencia_td = tds[2]
    competencia = competencia_td.get_text(strip=True)

    # Dados visíveis a partir da 4ª célula (índice 3)
    dados = [td.get_text(strip=True) for td in tds[3:]]

    # Junta a competição com os demais dados
    linha_completa = [competencia] + dados

    # Garante que a linha tenha exatamente o número de colunas esperado
    linha_completa = linha_completa[:len(headers)]

    # Monta linha HTML
    html_cells = "".join(f"<td>{dado}</td>" for dado in linha_completa)
    html_rows += f"<tr>{html_cells}</tr>\n"

# Monta a tabela HTML
html_table = "<table border='1' style='width:100%;border-collapse:collapse;text-align:center;'>\n<thead><tr>"
html_table += "".join(f"<th>{h}</th>" for h in headers)
html_table += "</tr></thead>\n<tbody>\n"
html_table += html_rows
html_table += "</tbody>\n</table>"

# Salva como HTML
os.makedirs("public", exist_ok=True)
with open("public/tabela_desempenho_completo.html", "w", encoding="utf-8") as f:
    f.write(html_table)

print("✅ Tabela salva com todas as colunas visíveis e alinhadas corretamente.")
