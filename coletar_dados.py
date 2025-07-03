import requests
from bs4 import BeautifulSoup

URL = "https://www.transfermarkt.com.br/rafael/leistungsdaten/spieler/68097/saison/2024/plus/1"
HEADERS = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", class_="items")
rows = table.find("tbody").find_all("tr")

html_linhas = ""
for row in rows:
    cols = row.find_all("td")
    if not cols:
        continue
    competencia = cols[0].get_text(strip=True)
    jogos = cols[1].get_text(strip=True)
    minutos = cols[-1].get_text(strip=True)
    html_linhas += f"<tr><td>{competencia}</td><td>{jogos}</td><td>{minutos}</td></tr>\n"

html_tabela = f"""<table border="1" style="width: 100%; border-collapse: collapse; text-align: center;">
  <thead style="background-color: #f2f2f2;">
    <tr>
      <th>Competição</th>
      <th>Jogos</th>
      <th>Minutos</th>
    </tr>
  </thead>
  <tbody>
    {html_linhas}
  </tbody>
</table>
"""

import os
os.makedirs("public", exist_ok=True)
with open("public/tabela_desempenho.html", "w", encoding="utf-8") as f:
    f.write(html_tabela)

print("✅ Tabela atualizada com sucesso.")
