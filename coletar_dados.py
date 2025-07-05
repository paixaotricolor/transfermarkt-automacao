import requests
from bs4 import BeautifulSoup
import os

# Carrega a lista de jogadores e URLs
with open("jogadores.txt", "r", encoding="utf-8") as f:
    jogadores = [linha.strip().split(", ") for linha in f if linha.strip()]

# Cria a pasta de saída
os.makedirs("public", exist_ok=True)

for nome, url in jogadores:
    print(f"🔍 Coletando dados de {nome}...")

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    div = soup.find("div", id="tab-leistungsdaten-gesamt")
    table = div.find("table", class_="items") if div else soup.find("table", class_="items")
    if not table:
        print(f"❌ Tabela não encontrada para {nome}")
        continue

    thead = table.find("thead")
    tbody = table.find("tbody")
    headers_html = "".join(f"<th>{th.get_text(strip=True)}</th>" for th in thead.find_all("th"))

    html_rows = ""
    for row in tbody.find_all("tr"):
        cols = row.find_all("td")
        if not cols:
            continue

        # Primeira coluna (nome da competição) pode ter imagem + texto
        nome_competicao = cols[0].get_text(strip=True)
        outras_colunas = [td.get_text(strip=True) for td in cols[1:]]

        html_cols = f"<td>{nome_competicao}</td>" + "".join(f"<td>{c}</td>" for c in outras_colunas)
        html_rows += f"<tr>{html_cols}</tr>\n"

    tabela_html = f"""
    <table border="1" style="width:100%;border-collapse:collapse;text-align:center;">
        <thead style="background-color:#f2f2f2;"><tr>{headers_html}</tr></thead>
        <tbody>{html_rows}</tbody>
    </table>
    """

    nome_arquivo = nome.strip().lower().replace(" ", "_") + ".html"
    with open(os.path.join("public", nome_arquivo), "w", encoding="utf-8") as f:
        f.write(tabela_html)

    print(f"✅ Tabela salva como public/{nome_arquivo}")

print("🏁 Coleta finalizada.")
