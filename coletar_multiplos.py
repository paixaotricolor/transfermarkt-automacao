import os
import requests
import random
from bs4 import BeautifulSoup

jogadores = [
    ("Rafael", "https://www.transfermarkt.com.br/rafael/leistungsdaten/spieler/68097/saison/2024/plus/1"),
    ("Jandrei", "https://www.transfermarkt.com.br/jandrei/leistungsdaten/spieler/512344/saison/2024/plus/1"),
    ("Young", "https://www.transfermarkt.com.br/young/leistungsdaten/spieler/894532/saison/2024/plus/1"),
    ("Leandro Mathias", "https://www.transfermarkt.com.br/leandro-mathias/leistungsdaten/spieler/838386/saison/2024/plus/1"),
    ("Alan Franco", "https://www.transfermarkt.com.br/alan-franco/leistungsdaten/spieler/503343/saison/2024/plus/1"),
    ("Ferraresi", "https://www.transfermarkt.com.br/nahuel-ferraresi/leistungsdaten/spieler/466336/saison/2024/plus/1"),
    ("Sabino", "https://www.transfermarkt.com.br/sabino/leistungsdaten/spieler/546033/saison/2024/plus/1"),
    ("Matheus Belém", "https://www.transfermarkt.com.br/matheus-belem/leistungsdaten/spieler/980825/saison/2024/plus/1"),
    ("Arboleda", "https://www.transfermarkt.com.br/robert-arboleda/leistungsdaten/spieler/139867/saison/2024/plus/1"),
    ("Igão", "https://www.transfermarkt.com.br/igao/leistungsdaten/spieler/1223221/saison/2024/plus/1"),
    ("Wendell", "https://www.transfermarkt.com.br/wendell/leistungsdaten/spieler/228433/saison/2024/plus/1"),
    ("Enzo Díaz", "https://www.transfermarkt.com.br/enzo-dias/leistungsdaten/spieler/540458/saison/2024/plus/1"),
    ("Patryck", "https://www.transfermarkt.com.br/patryck/leistungsdaten/spieler/662326/saison/2024/plus/1"),
    ("Moreira", "https://www.transfermarkt.com.br/joao-moreira/leistungsdaten/spieler/929866/saison/2024/plus/1"),
    ("Cédric", "https://www.transfermarkt.com.br/cedric-soares/leistungsdaten/spieler/112988/saison/2024/plus/1"),
    ("Maik", "https://www.transfermarkt.com.br/maik/leistungsdaten/spieler/1027026/saison/2024/plus/1"),
    ("Pablo Maia", "https://www.transfermarkt.com.br/pablo-maia/leistungsdaten/spieler/892089/saison/2024/plus/1"),
    ("Luan", "https://www.transfermarkt.com.br/luan-santos/leistungsdaten/spieler/574904/saison/2024/plus/1"),
    ("Negrucci", "https://www.transfermarkt.com.br/felipe-negrucci/leistungsdaten/spieler/980837/saison/2024/plus/1"),
    ("Luiz Gustavo", "https://www.transfermarkt.com.br/luiz-gustavo/leistungsdaten/spieler/10471/saison/2024/plus/1"),
    ("Marcos Antônio", "https://www.transfermarkt.com.br/marcos-antonio/leistungsdaten/spieler/468301/saison/2024/plus/1"),
    ("Rodriguinho", "https://www.transfermarkt.com.br/rodriguinho/leistungsdaten/spieler/743593/saison/2024/plus/1"),
    ("Bobadilla", "https://www.transfermarkt.com.br/damian-bobadilla/leistungsdaten/spieler/861852/saison/2024/plus/1"),
    ("Alisson", "https://www.transfermarkt.com.br/alisson/leistungsdaten/spieler/229736/saison/2024/plus/1"),
    ("Oscar", "https://www.transfermarkt.com.br/oscar/leistungsdaten/spieler/85314/saison/2024/plus/1"),
    ("Matheus Alves", "https://www.transfermarkt.com.br/matheus-alves/leistungsdaten/spieler/1127813/saison/2024/plus/1"),
    ("Ferreirinha", "https://www.transfermarkt.com.br/ferreirinha/leistungsdaten/spieler/689017/saison/2024/plus/1"),
    ("Lucca", "https://www.transfermarkt.com.br/lucca/leistungsdaten/spieler/1269378/saison/2024/plus/1"),
    ("Lucas Ferreira", "https://www.transfermarkt.com.br/lucas-ferreira/leistungsdaten/spieler/1219849/saison/2024/plus/1"),
    ("Lucas Moura", "https://www.transfermarkt.com.br/lucas-moura/leistungsdaten/spieler/77100/saison/2024/plus/1"),
    ("Henrique Carmo", "https://www.transfermarkt.com.br/henrique-carmo/leistungsdaten/spieler/1009031/saison/2024/plus/1"),
    ("Luciano", "https://www.transfermarkt.com.br/luciano/leistungsdaten/spieler/223560/saison/2024/plus/1"),
    ("Ryan Francisco", "https://www.transfermarkt.com.br/ryan-francisco/leistungsdaten/spieler/1202387/saison/2024/plus/1"),
    ("André Silva", "https://www.transfermarkt.com.br/andre-silva/leistungsdaten/spieler/565232/saison/2024/plus/1"),
    ("Calleri", "https://www.transfermarkt.com.br/jonathan-calleri/leistungsdaten/spieler/284727/saison/2024/plus/1"),
    ("Juan Dinenno", "https://www.transfermarkt.com.br/juan-dinenno/leistungsdaten/spieler/288786/saison/2024/plus/1")
]

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
    section = soup.find("div", {"id": "yw1"})
    if not section:
        print(f"⚠️ Seção de desempenho não encontrada para {jogador}")
        return

    table = section.find("table", class_="items")
    if not table:
        print(f"⚠️ Tabela não encontrada para {jogador}")
        return

    # Extrai os cabeçalhos
    header_row = table.find("thead").find_all("tr")[-1]
    headers = []
    for th in header_row.find_all("th", recursive=False):
        text = th.get_text(separator=" ", strip=True)
        headers.append(text if text else "")

    # Extrai os dados
    body_rows = table.find("tbody").find_all("tr", recursive=False)
    dados = []
    for row in body_rows:
        if "class" in row.attrs and "bg_rot_20" in row["class"]:
            continue
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

    # Corrige desalinhamento: remove colunas vazias à esquerda
    while dados and headers and all(row[0] == '' for row in dados if row):
        for row in dados:
            if row: del row[0]
        if headers: del headers[0]

    # Gera HTML
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

# Executa para todos os jogadores
for nome, link in jogadores:
    coletar_tabela(nome, link)
