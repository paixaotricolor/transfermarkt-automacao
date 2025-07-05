import requests
from bs4 import BeautifulSoup
import os

jogadores = [
    ("Jandrei", "https://www.transfermarkt.com.br/jandrei/leistungsdaten/spieler/512344/saison/2024/plus/1"),
    ("Young", "https://www.transfermarkt.com.br/young/leistungsdaten/spieler/894532/saison/2024/plus/1"),
    ("Leandro Mathias", "https://www.transfermarkt.com.br/leandro-mathias/leistungsdaten/spieler/838386/saison/2024/plus/1"),
    ("Alan Franco", "https://www.transfermarkt.com.br/alan-franco/leistungsdaten/spieler/503343/saison/2024/plus/1"),
    # Adicione os demais aqui
]

headers = {"User-Agent": "Mozilla/5.0"}

def encontrar_tabela_dados(soup):
    tabelas = soup.find_all("table", class_="items")
    for tabela in tabelas:
        legenda = tabela.find_previous("h2")
        if legenda and "Desempenho" in legenda.get_text():
            return tabela
    return None

for nome, url in jogadores:
    print(f"🔄 Coletando dados de {nome}...")
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        tabela = encontrar_tabela_dados(soup)
        if not tabela:
            print(f"⚠️ Tabela de desempenho não encontrada para {nome}")
            continue

        # Cabeçalhos
        header_cells = tabela.find("thead").find_all("th")
        headers_text = [th.get_text(strip=True) for th in header_cells]

        # Linhas de dados
        rows = tabela.find("tbody").find_all("tr")
        html_rows = ""
        for row in rows:
            cols = row.find_all("td")
            if not cols:
                continue
            row_data = []
            for idx, col in enumerate(cols):
                if idx == 0:
                    texto = col.get_text(strip=True)
                    row_data.append(texto)
                else:
                    row_data.append(col.get_text(strip=True))
            html_cells = "".join(f"<td>{dado}</td>" for dado in row_data)
            html_rows += f"<tr>{html_cells}</tr>\n"

        # Monta a tabela final
        html_table = "<table border='1' style='width:100%;border-collapse:collapse;text-align:center;'>\n"
        html_table += "<thead><tr>" + "".join(f"<th>{h}</th>" for h in headers_text) + "</tr></thead>\n"
        html_table += "<tbody>\n" + html_rows + "</tbody>\n</table>"

        os.makedirs("public", exist_ok=True)
        filename = f"public/{nome.lower().replace(' ', '_')}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_table)

        print(f"✅ Tabela salva em {filename}")

    except Exception as e:
        print(f"❌ Erro ao processar {nome}: {e}")
