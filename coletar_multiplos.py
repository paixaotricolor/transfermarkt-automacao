import os
import requests
import random
from bs4 import BeautifulSoup

# Lista de jogadores (nome, link da tabela de desempenho)
jogadores = [
    ("Rafael", "https://www.transfermarkt.com.br/rafael/leistungsdaten/spieler/68097/saison/2024/plus/1"),
    ("Jandrei", "https://www.transfermarkt.com.br/jandrei/leistungsdaten/spieler/512344/saison/2024/plus/1"),
    ("Young", "https://www.transfermarkt.com.br/young/leistungsdaten/spieler/894532/saison/2024/plus/1"),
    # ...adicione os outros jogadores aqui
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

# Traduções personalizadas de cabeçalhos
mapa_cabecalhos = {
    "Wettbewerb": "Campeonato",
    "Spiele": "Jogos",
    "Tore": "Gols",
    "Gegentore": "Gols sofridos",
    "Ein": "Suplente utilizado",
    "Aus": "Substituições",
    "Gelbe Karten": "Cartões amarelos",
    "Gelb-Rote Karten": "Expulsões (dois amarelos)",
    "Rote Karten": "Expulsões (vermelho direto)",
    "Zu-Null-Spiele": "Jogos sem gols sofridos",
    "Minuten": "Minutos jogados"
}

def coletar_tabela(jogador, url):
    print(f"🔄 Coletando dados de {jogador}...")

    try:
        headers = {"User-Agent": random.choice(user_agents)}
        response = requests.get(url, timeout=20, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Erro ao acessar a página de {jogador}: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    section = soup.find("div", {"id": "yw1"})
    if not section:
        print(f"⚠️ Seção de desempenho não encontrada para {jogador}")
        return

    table = section.find("table", class_="items")
    if not table:
        print(f"⚠️ Tabela não encontrada para {jogador}")
        return

    # Cabeçalhos
    header_row = table.find("thead").find_all("tr")[-1]
    headers = [th.get_text(strip=True) for th in header_row.find_all("th") if th.get_text(strip=True)]
    headers = [mapa_cabecalhos.get(h, h) for h in headers]

    # Linhas de dados
    body_rows = table.find("tbody").find_all("tr", recursive=False)
    dados = []
    for row in body_rows:
        if "class" in row.attrs and "bg_rot_20" in row["class"]:
            continue  # ignora linha de separação

        cells = []
        for td in row.find_all("td", recursive=False):
            for tag in td.find_all(["img", "svg", "a"]):
                tag.unwrap()
            text = td.get_text(strip=True)
            cells.append(text)
        if cells:
            dados.append(cells)

    if not headers or not dados:
        print(f"⚠️ Dados incompletos para {jogador}")
        return

    # Corrige desalinhamento de colunas extras à esquerda
    while all(row and row[0] == '' for row in dados):
        for row in dados:
            del row[0]
        if headers:
            del headers[0]

    # Geração do HTML
    html = "<html><head><meta charset='UTF-8'>"
    html += """<style>
        body { font-family: sans-serif; padding: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: center; }
        th { background-color: #eee; position: sticky; top: 0; z-index: 1; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>"""
    html += "</head><body>"
    html += f"<h2>{jogador} - Desempenho 2024</h2>"
    html += "<table><thead><tr>"
    for h in headers:
        html += f"<th>{h}</th>"
    html += "</tr></thead><tbody>"
    for row in dados:
        html += "<tr>" + "".join(f"<td>{d}</td>" for d in row) + "</tr>"
    html += "</tbody></table></body></html>"

    os.makedirs("public", exist_ok=True)
    filename = f"public/{jogador.lower().replace(' ', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Tabela salva em {filename}")


# Executa para todos os jogadores
for nome, link in jogadores:
    coletar_tabela(nome, link)
