import requests
from bs4 import BeautifulSoup
import os

jogadores = [
    ("Jandrei", "https://www.transfermarkt.com.br/jandrei/leistungsdaten/spieler/512344/saison/2024/plus/1"),
    # adicione o restante dos jogadores aqui...
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def extrair_tabela_desempenho(html):
    soup = BeautifulSoup(html, "html.parser")
    # Encontra a tabela correta com base no título da seção
    for h2 in soup.find_all("h2"):
        if "Desempenho" in h2.get_text():
            table = h2.find_next("table")
            if table:
                return table
    return None

def tabela_para_html_formatada(table):
    thead = table.find("thead")
    tbody = table.find("tbody")

    # Extrair cabeçalhos com suporte a múltiplas linhas
    headers = []
    for row in thead.find_all("tr"):
        cols = [th.get_text(strip=True) for th in row.find_all(["th", "td"])]
        headers.append(cols)

    # Padronizar cabeçalhos finais
    colunas_finais = headers[-1] if headers else []

    # Extrair dados com primeira coluna ignorando ícone (imagem)
    linhas = []
    for row in tbody.find_all("tr"):
        cols = row.find_all("td")
        if not cols:
            continue
        linha = []
        for i, col in enumerate(cols):
            if i == 0:
                # Apenas o texto do nome da competição
                texto = col.get_text(strip=True)
                linha.append(texto)
            else:
                linha.append(col.get_text(strip=True))
        linhas.append(linha)

    # Montar HTML final
    html = "<table>\n<thead><tr>" + "".join(f"<th>{col}</th>" for col in colunas_finais) + "</tr></thead>\n<tbody>\n"
    for linha in linhas:
        html += "<tr>" + "".join(f"<td>{dado}</td>" for dado in linha) + "</tr>\n"
    html += "</tbody>\n</table>"

    return html

def salvar_html(nome, conteudo):
    os.makedirs("public", exist_ok=True)
    caminho = f"public/{nome.lower().replace(' ', '_')}.html"
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"✅ Tabela salva: {caminho}")

for nome, url in jogadores:
    print(f"🔄 Coletando dados de {nome}...")
    try:
        r = requests.get(url, headers=HEADERS)
        tabela = extrair_tabela_desempenho(r.text)
        if not tabela:
            print(f"⚠️ Tabela não encontrada para {nome}")
            continue
        html_formatado = tabela_para_html_formatada(tabela)
        salvar_html(nome, html_formatado)
    except Exception as e:
        print(f"❌ Erro ao processar {nome}: {e}")
