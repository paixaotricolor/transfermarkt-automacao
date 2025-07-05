import requests
from bs4 import BeautifulSoup
import os

# Lista embutida com nome + link
jogadores = [
    ("Jandrei", "https://www.transfermarkt.com.br/jandrei/leistungsdaten/spieler/512344/saison/2024/plus/1"),
    ("Young", "https://www.transfermarkt.com.br/young/leistungsdaten/spieler/894532/saison/2024/plus/1"),
    ("Leandro Mathias", "https://www.transfermarkt.com.br/leandro-mathias/leistungsdaten/spieler/838386/saison/2024/plus/1"),
    ("Alan Franco", "https://www.transfermarkt.com.br/alan-franco/leistungsdaten/spieler/503343/saison/2024/plus/1"),
    # Adicione o restante dos jogadores aqui
]

headers = {"User-Agent": "Mozilla/5.0"}

for nome, url in jogadores:
    print(f"🔄 Coletando dados de {nome}...")

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Localiza a div da tabela "Desempenho"
        div = soup.find("div", id="tab-leistungsdaten-gesamt")
        if not div:
            print(f"⚠️ Seção de desempenho não encontrada para {nome}")
            continue

        table = div.find("table", class_="items")
        if not table:
            print(f"⚠️ Tabela de desempenho não encontrada para {nome}")
            continue

        # Extrai os cabeçalhos da tabela
        header_cells = table.find("thead").find_all("th")
        headers_text = [th.get_text(strip=True) for th in header_cells]

        # Extrai as linhas de dados
        rows = table.find("tbody").find_all("tr")
        html_rows = ""

        for row in rows:
            cols = row.find_all("td")
            if not cols:
                continue

            values = []
            for idx, col in enumerate(cols):
                if idx == 0:
                    values.append(col.get_text(strip=True))  # Pega só o nome da competição
                else:
                    values.append(col.get_text(strip=True))

            html_cells = "".join(f"<td>{v}</td>" for v in values)
            html_rows += f"<tr>{html_cells}</tr>\n"

        # Monta a tabela HTML com cabeçalho fixo
        html_table = "<table border='1' style='width:100%;border-collapse:collapse;text-align:center;'>\n"
        html_table += "<thead><tr>"
        for h in headers_text:
            html_table += f"<th>{h}</th>"
        html_table += "</tr></thead>\n<tbody>\n"
        html_table += html_rows
        html_table += "</tbody>\n</table>"

        # Salva o HTML
        os.makedirs("public", exist_ok=True)
        filename = f"public/{nome.lower().replace(' ', '_')}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_table)

        print(f"✅ Tabela salva em {filename}")

    except Exception as e:
        print(f"❌ Erro ao processar {nome}: {e}")
