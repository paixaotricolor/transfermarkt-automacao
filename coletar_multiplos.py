import os
import requests
from bs4 import BeautifulSoup

jogadores = [
    # Formato: (nome, link, é_goleiro)
    ("Luiz Gustavo", "https://www.transfermarkt.com.br/luiz-gustavo/leistungsdaten/spieler/10471/saison/2024/plus/1", False),
    ("Marcos Antônio", "https://www.transfermarkt.com.br/marcos-antonio/leistungsdaten/spieler/468301/saison/2024/plus/1", False),
    ("Rodriguinho", "https://www.transfermarkt.com.br/rodriguinho/leistungsdaten/spieler/743593/saison/2024/plus/1", False),
    ("Bobadilla", "https://www.transfermarkt.com.br/damian-bobadilla/leistungsdaten/spieler/861852/saison/2024/plus/1", False),
    ("Alisson", "https://www.transfermarkt.com.br/alisson/leistungsdaten/spieler/229736/saison/2024/plus/1", False),
    ("Oscar", "https://www.transfermarkt.com.br/oscar/leistungsdaten/spieler/85314/saison/2024/plus/1", False),
    ("Matheus Alves", "https://www.transfermarkt.com.br/matheus-alves/leistungsdaten/spieler/1127813/saison/2024/plus/1", False),
    ("Ferreirinha", "https://www.transfermarkt.com.br/ferreirinha/leistungsdaten/spieler/689017/saison/2024/plus/1", False),
    ("Lucca", "https://www.transfermarkt.com.br/lucca/leistungsdaten/spieler/1269378/saison/2024/plus/1", False),
    ("Lucas Ferreira", "https://www.transfermarkt.com.br/lucas-ferreira/leistungsdaten/spieler/1219849/saison/2024/plus/1", False),
    ("Lucas Moura", "https://www.transfermarkt.com.br/lucas-moura/leistungsdaten/spieler/77100/saison/2024/plus/1", False),
    ("Henrique Carmo", "https://www.transfermarkt.com.br/henrique-carmo/leistungsdaten/spieler/1009031/saison/2024/plus/1", False),
    ("Luciano", "https://www.transfermarkt.com.br/luciano/leistungsdaten/spieler/223560/saison/2024/plus/1", False),
    ("Ryan Francisco", "https://www.transfermarkt.com.br/ryan-francisco/leistungsdaten/spieler/1202387/saison/2024/plus/1", False),
    ("André Silva", "https://www.transfermarkt.com.br/andre-silva/leistungsdaten/spieler/565232/saison/2024/plus/1", False),
    ("Calleri", "https://www.transfermarkt.com.br/jonathan-calleri/leistungsdaten/spieler/284727/saison/2024/plus/1", False),
    ("Juan Dinenno", "https://www.transfermarkt.com.br/juan-dinenno/leistungsdaten/spieler/288786/saison/2024/plus/1", False)
]

HEADERS_GOLEIRO = [
    "campeonato", "jogos", "gols", "gols contra", "suplente utilizado", "substituições",
    "cartões amarelos", "expulsões (dois amarelos)", "expulsões (vermelho direto)",
    "gols sofridos", "jogos sem gols sofridos", "minutos jogados"
]

HEADERS_LINHA = [
    "campeonato", "jogos", "gols", "assistências", "gols contra",
    "suplente utilizado", "substituições", "cartões amarelos",
    "expulsões (dois amarelos)", "expulsões (vermelho direto)",
    "gols de pênalti", "minutos por gol", "minutos jogados"
]

def extrair_tabela(html, is_goleiro):
    soup = BeautifulSoup(html, "html.parser")
    section = soup.find("div", class_="responsive-table")
    if not section:
        return None

    table = section.find("table")
    if not table:
        return None

    tbody = table.find("tbody")
    rows = tbody.find_all("tr", recursive=False)

    html_rows = ""
    for row in rows:
        cols = row.find_all("td", recursive=False)
        if not cols:
            continue

        # Remove a primeira coluna (ícone/campeonato)
        dados = [td.get_text(strip=True) for td in cols[1:]]
        html_cells = "".join(f"<td>{dado}</td>" for dado in dados)
        html_rows += f"<tr>{html_cells}</tr>\n"

    headers = HEADERS_GOLEIRO if is_goleiro else HEADERS_LINHA
    html_head = "".join(f"<th>{coluna}</th>" for coluna in headers)
    return f"<table>\n<thead><tr>{html_head}</tr></thead>\n<tbody>\n{html_rows}</tbody>\n</table>"

def coletar_dados(jogadores):
    os.makedirs("public", exist_ok=True)

    for nome, url, is_goleiro in jogadores:
        print(f"🔄 Coletando dados de {nome}...")
        try:
            response = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }, timeout=20)
            response.raise_for_status()
        except Exception as e:
            print(f"❌ Erro ao acessar página de {nome}: {e}")
            continue

        tabela_html = extrair_tabela(response.text, is_goleiro)
        if not tabela_html:
            print(f"⚠️ Tabela não encontrada para {nome}")
            continue

        titulo = "goleiro" if is_goleiro else "jogador de linha"
        output_html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{nome} - Tabela de Desempenho ({titulo})</title>
  <style>
    body {{ font-family: Arial, sans-serif; padding: 20px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
    thead th {{ position: sticky; top: 0; background-color: #f9f9f9; z-index: 1; }}
  </style>
</head>
<body>
  <h2>Tabela de desempenho ({titulo}) - {nome}</h2>
  {tabela_html}
</body>
</html>"""

    filename = f"public/{nome.lower().replace(' ', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output_html)

    print(f"✅ Tabela salva em {filename}")
    print(f"⏳ Aguardando 20 segundos antes de coletar o próximo jogador...\n")
    time.sleep(20)

if __name__ == "__main__":
    coletar_dados(jogadores)
