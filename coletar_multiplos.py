import requests
from bs4 import BeautifulSoup
import os

HEADERS = {"User-Agent": "Mozilla/5.0"}
os.makedirs("public", exist_ok=True)

with open("jogadores.txt", encoding="utf-8") as f:
    linhas = f.readlines()

for linha in linhas:
    if not linha.strip():
        continue
    try:
        nome, url = [parte.strip() for parte in linha.split(",", 1)]
    except ValueError:
        print(f"⚠️ Linha inválida: {linha}")
        continue

    print(f"⏳ Processando {nome}...")
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        div = soup.find("div", id="tab-leistungsdaten-gesamt")
        table = div.find("table", class_="items") if div else soup.find("table", class_="items")
        if not table:
            raise Exception("Tabela não encontrada")

        header_cells = table.find("thead").find_all("th")
        headers = [th.get_text(strip=True) for th in header_cells]

        html_rows = ""
        for row in table.find("tbody").find_all("tr"):
            cols = row.find_all("td")
            if not cols:
                continue
            nome_competicao = cols[0].find(text=True, recursive=False)
            values = [nome_competicao.strip() if nome_competicao else ""] + [td.get_text(strip=True) for td in cols[1:]]
            html_cols = "".join(f"<td>{v}</td>" for v in values)
            html_rows += f"<tr>{html_cols}</tr>\n"

        html_table = "<table border='1' style='width:100%;border-collapse:collapse;text-align:center;'>\n<thead><tr>"
        html_table += "".join(f"<th>{h}</th>" for h in headers)
        html_table += "</tr></thead>\n<tbody>\n"
        html_table += html_rows
        html_table += "</tbody>\n</table>"

        filename = f"public/{nome.lower().replace(' ', '_')}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_table)

        print(f"✅ {nome} salvo em {filename}")

    except Exception as e:
        print(f"❌ Erro ao processar {nome}: {e}")

print("🏁 Finalizado.")
