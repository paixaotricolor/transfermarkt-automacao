import requests
from bs4 import BeautifulSoup
import os

# Lista de jogadores (nome, url)
JOGADORES = [
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

HEADERS = {"User-Agent": "Mozilla/5.0"}

os.makedirs("public", exist_ok=True)

def coletar_tabela(nome, url):
    print(f"🔄 Coletando dados de {nome}...")
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        div = soup.find("div", id="tab-leistungsdaten-gesamt")
        table = div.find("table", class_="items") if div else None
        if not table:
            print(f"⚠️ Tabela não encontrada para {nome}")
            return

        # Extrair cabeçalhos
        headers = [th.get_text(strip=True) for th in table.find("thead").find_all("th") if th.get_text(strip=True)]

        # Extrair linhas
        html_rows = ""
        for row in table.find("tbody").find_all("tr"):
            cols = row.find_all("td")
            if not cols:
                continue
            # Ignora a primeira coluna (ícone)
            values = [td.get_text(strip=True) for td in cols[1:]]
            html_cells = "".join(f"<td>{v}</td>" for v in values)
            html_rows += f"<tr>{html_cells}</tr>\n"

        # Monta a tabela HTML
        html_table = "<table border='1' style='width:100%;border-collapse:collapse;text-align:center;'>\n<thead>\n<tr>"
        for h in headers[1:]:  # também ignora o cabeçalho da 1ª coluna
            html_table += f"<th>{h}</th>"
        html_table += "</tr>\n</thead>\n<tbody>\n"
        html_table += html_rows
        html_table += "</tbody>\n</table>"

        # Salva o HTML
        filename = f"public/{nome.lower().replace(' ', '_')}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_table)

        print(f"✅ Tabela salva: {filename}")
    except Exception as e:
        print(f"❌ Erro ao processar {nome}: {e}")

# Roda para todos os jogadores
for nome, url in JOGADORES:
    coletar_tabela(nome, url)
