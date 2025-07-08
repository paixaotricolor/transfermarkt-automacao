import os
import random
import requests
from bs4 import BeautifulSoup

# Lista fixa de cabeçalhos
HEADERS_FIXOS = [
    "Campeonato",
    "Jogos",
    "Gols",
    "Gols sofridos",
    "Suplente utilizado",
    "Substituições",
    "Cartões amarelos",
    "Expulsões (dois amarelos)",
    "Expulsões (vermelho direto)",
    "Gols sofridos",
    "Jogos sem gols sofridos",
    "Minutos jogados"
]

# Lista de jogadores (nome + link)
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

# Função para obter lista de proxies do secret
def carregar_proxies():
    proxies_env = os.getenv("PROXY_LIST", "")
    proxies = [p.strip() for p in proxies_env.split(",") if p.strip()]
    return proxies

# Função para escolher um proxy aleatório
def escolher_proxy(proxies):
    if not proxies:
        return None
    proxy = random.choice(proxies)
    return {
        "http": proxy,
        "https": proxy
    }

# Função principal
def coletar_tabela(nome, url, proxies):
    print(f"🔄 Coletando dados de {nome}...")

    try:
        response = requests.get(url, proxies=escolher_proxy(proxies), timeout=20)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Erro ao acessar página de {nome}: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Tabela de desempenho 2025
    table = soup.find("table", class_="items")
    if not table:
        print(f"⚠️ Tabela de desempenho não encontrada para {nome}")
        return

    # Extrai dados
    body_rows = table.find("tbody").find_all("tr", recursive=False)
    rows = []
    for row in body_rows:
        cols = row.find_all(["th", "td"], recursive=False)
        row_data = [col.get_text(strip=True) for col in cols]
        if len(row_data) == len(HEADERS_FIXOS):
            rows.append(row_data)

    if not rows:
        print(f"⚠️ Nenhuma linha de dados válida para {nome}")
        return

    # Gera HTML
    html = "<html><head><meta charset='UTF-8'><style>"
    html += "table { border-collapse: collapse; width: 100%; }"
    html += "th, td { border: 1px solid #999; padding: 8px; text-align: center; }"
    html += "thead th { position: sticky; top: 0; background: #eee; }"
    html += "</style></head><body>"
    html += f"<h2>Tabela de desempenho de {nome}</h2><table><thead><tr>"

    for h in HEADERS_FIXOS:
        html += f"<th>{h}</th>"
    html += "</tr></thead><tbody>"

    for row in rows:
        html += "<tr>" + "".join(f"<td>{d}</td>" for d in row) + "</tr>"

    html += "</tbody></table></body></html>"

    os.makedirs("public", exist_ok=True)
    filename = f"public/{nome.lower().replace(' ', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Tabela salva em {filename}")


if __name__ == "__main__":
    proxies = carregar_proxies()
    for nome, url in jogadores:
        coletar_tabela(nome, url, proxies)
