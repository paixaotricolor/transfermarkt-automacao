import os
import requests
import random
from bs4 import BeautifulSoup

# Lista de jogadores (nome, link da tabela de desempenho)
jogadores = [
    ("Jandrei", "https://www.transfermarkt.com.br/jandrei/leistungsdaten/spieler/512344/saison/2024/plus/1"),
    ("Young", "https://www.transfermarkt.com.br/young/leistungsdaten/spieler/894532/saison/2024/plus/1"),
    ("Leandro Mathias", "https://www.transfermarkt.com.br/leandro-mathias/leistungsdaten/spieler/838386/saison/2024/plus/1"),
    ("Alan Franco", "https://www.transfermarkt.com.br/alan-franco/leistungsdaten/spieler/503343/saison/2024/plus/1"),
    # ...adicione os outros aqui
]

# Usa proxies se configurado como secret PROXY_LIST
proxy_list = os.getenv("PROXY_LIST", "").split(",")
def get_random_proxy():
    proxy = random.choice(proxy_list).strip()
    return {"http": proxy, "https": proxy} if proxy else None

def coletar_tabela(jogador, url):
    print(f"🔄 Coletando dados de {jogador}...")

    try:
        response = requests.get(url, proxies=get_random_proxy(), timeout=20, headers={
            "User-Agent": "Mozilla/5.0"
        })
    except Exception as e:
        print(f"❌ Erro ao acessar a página de {jogador}: {e}")
        return

    if response.status_code != 200:
        print(f"❌ Erro HTTP para {jogador}: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Encontra a seção com título "Desempenho 2025"
    section = soup.find("div", {"id": "yw1"})
    if not section:
        print(f"⚠️ Seção de desempenho não encontrada para {jogador}")
        return

    # Localiza a tabela correta
    table = section.find("table", class_="items")
    if not table:
        print(f"⚠️ Tabela não encontrada para {jogador}")
        return

    # Extrai o cabeçalho da tabela
    header_row = table.find("thead").find_all("tr")[-1]
    headers = [th.get_text(strip=True) for th in header_row.find_all("th") if th.get_text(strip=True)]

    # Extrai as linhas de dados
    body_rows = table.find("tbody").find_all("tr", recursive=False)
    dados = []
    for row in body_rows:
        if "class" in row.attrs and "bg_rot_20" in row["class"]:
            continue  # ignora linhas de separação

        cells = []
        for td in row.find_all("td", recursive=False):
            # Remove ícones e imagens
            for tag in td.find_all(["img", "svg", "a"]):
                tag.unwrap()
            text = td.get_text(strip=True)
            if text:
                cells.append(text)
        if cells:
            dados.append(cells)

    if not headers or not dados:
        print(f"⚠️ Dados incompletos para {jogador}")
        return

    # Corrige desalinhamento removendo colunas vazias à esquerda
    while all(row and row[0] == '' for row in dados):
        for row in dados:
            del row[0]
        if headers:
            del headers[0]

    # Geração do HTML
    html = "<html><head><meta charset='UTF-8'>"
    html += """
    <style>
        body { font-family: sans-serif; padding: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: center; }
        th { background-color: #eee; position: sticky; top: 0; z-index: 1; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
    """
    html += "</head><body>"
    html += f"<h2>{jogador} - Desempenho 2025</h2>"
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

# Roda para todos os jogadores
for nome, link in jogadores:
    coletar_tabela(nome, link)
