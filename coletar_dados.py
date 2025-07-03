import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.transfermarkt.com.br/rafael/leistungsdaten/spieler/68097/saison/2024/plus/1"
HEADERS = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

# Acessa a aba 'gesamt' (desempenho completo)
tabela_div = soup.find("div", id="tab-leistungsdaten-gesamt")
if not tabela_div:
    raise Exception("Tabela de desempenho não encontrada")

table = tabela_div.find("table", class_="items")
thead = table.find("thead")
tbody = table.find("tbody")
rows = tbody.find_all("tr")

# Extrair cabeçalhos
headers = [th.get_text(strip=True) for th in thead.find_all("th")]

# Construir linhas da tabela
html_linhas = ""
for row in rows:
    if "class" in row.attrs and "bg_blau_20" in row["class"]:
        continue  # Ignora subheaders dentro do corpo da tabela
    cols = row.find_all("td")
    if not cols:
        continue
    dados = [td.get_text(strip=True).replace("'", "") for td in cols]
    html_linhas += "<tr>" + "".join(f"<td>{d}</td>" for d in dados) + "</tr>\n"

# Gerar cabeçalho HTML
html_header = "".join(f"<th>{h}</th>" for h in headers)

# HTML final
html_tabela = f"""<table border="1" style="width: 100%; border-collapse: collapse; text-align: center;">
  <thead style="background-color: #f2f2f2;">
    <tr>{html_header}</tr>
  </thead>
  <tbody>
    {html_linhas}
  </tbody>
</table>
"""

os.makedirs("public", exist_ok=True)
with open("public/tabela_desempenho.html", "w", encoding="utf-8") as f:
    f.write(html_tabela)

print("✅ Tabela COMPLETA de desempenho atualizada com sucesso.")
