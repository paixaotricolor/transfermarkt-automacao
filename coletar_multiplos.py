import requests
from bs4 import BeautifulSoup
import os
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}

def gerar_slug(nome):
    return re.sub(r"[^\w]+", "-", nome.strip().lower())

def extrair_tabela(nome, url):
    print(f"🔄 Coletando dados de {nome}...")
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    div = soup.find("div", id="tab-leistungsdaten-gesamt")
    table = div.find("table", class_="items") if div else None
    if not table:
        print(f"⚠️ Tabela não encontrada para {nome}")
        return

    headers = [th.get_text(strip=True) for th in table.find("thead").find_all("th") if th.get_text(strip=True)]
    
    html_rows = ""
    for row in table.find("tbody").find_all("tr"):
        cols = row.find_all("td")
        if not cols:
            continue

        # Captura a 1ª coluna com o nome da competição (ignora ícone de imagem)
        nome_competicao = cols[0].get_text(strip=True)
        demais_dados = [td.get_text(strip=True) for td in cols[1:]]

        dados = [nome_competicao] + demais_dados
        html_cells = "".join(f"<td>{dado}</td>" for dado in dados)
        html_rows += f"<tr>{html_cells}</tr>\n"

    html_table = "<table border='1' style='width:100%;border-collapse:collapse;text-align:center;'>\n"
    html_table += "<thead><tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead>\n"
    html_table += f"<tbody>\n{html_rows}</tbody>\n</table>"

    os.makedirs("public", exist_ok=True)
    slug = gerar_slug(nome)
    with open(f"public/{slug}.html", "w", encoding="utf-8") as f:
        f.write(html_table)
    print(f"✅ Tabela salva em public/{slug}.html")

def main():
    with open("jogadores.txt", encoding="utf-8") as f:
        linhas = f.readlines()

    for linha in linhas:
        if "," in linha:
            nome, url = linha.strip().split(",", 1)
            extrair_tabela(nome.strip(), url.strip())

if __name__ == "__main__":
    main()
