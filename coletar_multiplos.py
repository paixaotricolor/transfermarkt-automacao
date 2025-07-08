import os
import requests
from bs4 import BeautifulSoup

# Lista de jogadores (nome, URL)
jogadores = [
    ("Rafael", "https://www.transfermarkt.com.br/rafael/leistungsdaten/spieler/68097/saison/2024/plus/1"),
    ("Jandrei", "https://www.transfermarkt.com.br/jandrei/leistungsdaten/spieler/512344/saison/2024/plus/1"),
    ("Cédric", "https://www.transfermarkt.com.br/cedric-soares/leistungsdaten/spieler/112988/saison/2024/plus/1"),
    ("Maik", "https://www.transfermarkt.com.br/maik/leistungsdaten/spieler/1027026/saison/2024/plus/1"),
    ("Pablo Maia", "https://www.transfermarkt.com.br/pablo-maia/leistungsdaten/spieler/892089/saison/2024/plus/1"),
    ("Luan", "https://www.transfermarkt.com.br/luan-santos/leistungsdaten/spieler/574904/saison/2024/plus/1"),
    ("Negrucci", "https://www.transfermarkt.com.br/felipe-negrucci/leistungsdaten/spieler/980837/saison/2024/plus/1"),
]

# Cabeçalhos personalizados
cabecalhos = [
    "Campeonato", "Jogos", "Gols", "Assistências", "Gols Contra", "Suplente utilizado",
    "Substituições", "Cartões amarelos", "Expulsões (dois amarelos)", "Expulsões (vermelho direto)",
    "Gols de pênalti", "Minutos por gol", "Minutos jogados"
]

# Headers realistas para simular navegador
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

# Função para limpar imagem da primeira coluna
def limpar_imagem_cabecalho(html):
    soup = BeautifulSoup(html, "html.parser")
    section = soup.find("div", class_="responsive-table")
    if not section:
        return None

    table = section.find("table")
    if not table:
        return None

    for td in table.find_all("td"):
        if td.find("img"):
            td.img.decompose()
    return str(table)

# Cria a pasta public se não existir
os.makedirs("public", exist_ok=True)

# Loop por jogador
for nome, url in jogadores:
    print(f"🔄 Coletando dados de {nome}...")
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        tabela_html = limpar_imagem_cabecalho(response.text)
        if not tabela_html:
            print(f"⚠️ Tabela não encontrada para {nome}")
            continue

        # Gera HTML com cabeçalho fixo
        output_html = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{nome} - Tabela de Desempenho</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
                thead th {{ position: sticky; top: 0; background-color: #f9f9f9; z-index: 1; }}
            </style>
        </head>
        <body>
            <h2>Tabela de desempenho - {nome}</h2>
            <table>
                <thead>
                    <tr>{"".join(f"<th>{coluna}</th>" for coluna in cabecalhos)}</tr>
                </thead>
                <tbody>
                    {BeautifulSoup(tabela_html, "html.parser").find("tbody")}
                </tbody>
            </table>
        </body>
        </html>
        """

        filename = f"public/{nome.lower().replace(' ', '_')}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(output_html)
        print(f"✅ Tabela salva em {filename}")

    except Exception as e:
        print(f"❌ Erro ao acessar página de {nome}: {e}")
