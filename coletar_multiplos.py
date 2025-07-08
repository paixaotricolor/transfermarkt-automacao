import requests
from bs4 import BeautifulSoup
import os

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
    ("Juan Dinenno", "https://www.transfermarkt.com.br/juan-dinenno/leistungsdaten/spieler/288786/saison/2024/plus/1")]

headers = {"User-Agent": "Mozilla/5.0"}

def encontrar_tabela_dados(soup):
    # Busca todas as tabelas com classe 'items'
    tabelas = soup.find_all("table", class_="items")
    for tabela in tabelas:
        h2 = tabela.find_previous("h2")
        if h2 and "Desempenho" in h2.text:
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

        # Cabeçalhos: pega a última linha de <thead> com <th> visíveis (ignora agrupamentos)
        thead_rows = tabela.find("thead").find_all("tr")
        header_cells = thead_rows[-1].find_all("th")
        headers_text = [th.get_text(strip=True) for th in header_cells]

        # Linhas de dados
        rows = tabela.find("tbody").find_all("tr", recursive=False)
        html_rows = ""
        for row in rows:
            cols = row.find_all("td", recursive=False)
            if not cols:
                continue

            row_data = []

            for idx, col in enumerate(cols):
                # Primeira coluna (competição): ignora imagem e pega só o texto
                if idx == 0:
                    texto = col.get_text(strip=True)
                    row_data.append(texto)
                else:
                    row_data.append(col.get_text(strip=True))

            # Preenche com colunas vazias se estiver faltando
            while len(row_data) < len(headers_text):
                row_data.append("")

            html_cells = "".join(f"<td>{d}</td>" for d in row_data)
            html_rows += f"<tr>{html_cells}</tr>\n"

        # Monta a tabela HTML final
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
