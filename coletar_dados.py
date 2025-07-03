import requests
from bs4 import BeautifulSoup

# URL da página do Transfermarkt com os dados
URL = "https://www.transfermarkt.com.br/rafael/leistungsdaten/spieler/68097/saison/2024/plus/1"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Faz a requisição à página
response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

# Encontra a tabela dos dados
table = soup.find("table", class_="items")
rows = table.find("tbody").find_all("tr")

# Monta as linhas HTML com os dados desejados
html_linhas = ""
for row in rows:
    cols = row.find_all("td")
    if not cols:
        continue
    competencia = cols[0].get_text(strip=True)
    jogos = cols[1].get_text(strip=True)
    minutos = cols[-1].get_text(strip=True)
    
    html_linhas += f"<tr><td>{competencia}</td><td>{jogos}</td><td>{minutos}</td></tr>\n"

# Monta a tabela completa em HTML
html_tabela = f"""
<table border="1">
  <thead>
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

# Salva o conteúdo da tabela em um arquivo HTML simples
with open("tabela_desempenho.html", "w", encoding="utf-8") as f:
    f.write(html_tabela)

print("Tabela HTML salva com sucesso!")
