import requests
import json
import csv
import time
from datetime import datetime, timezone
import statistics


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ENDPOINT = "https://api.github.com/graphql"
BATCH_SIZE = 10                   
TOTAL_ALVO = 100                  

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN.strip()}",
    "Content-Type": "application/json"
}


query = """
query getTopRepositories($cursor: String, $first: Int!) {
  search(query: "stars:>10000 sort:stars-desc", type: REPOSITORY, first: $first, after: $cursor) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        nameWithOwner
        stargazerCount
        createdAt
        url
        mergedPRs: pullRequests(states: MERGED) {
          totalCount
        }
        releases {
          totalCount
        }
      }
    }
  }
}
"""

def executar_query(query, variables=None, tentativas=5):
    payload = {"query": query, "variables": variables or {}}
    for tentativa in range(tentativas):
        try:
            response = requests.post(ENDPOINT, json=payload, headers=headers, timeout=25)
            if response.status_code == 200:
                return response.json()
            elif response.status_code in [502, 503, 504]:
                tempo_espera = (tentativa + 1) * 3
                print(f"  [Aviso] GitHub ocupado ({response.status_code}). Aguardando {tempo_espera}s... (Tentativa {tentativa+1}/{tentativas})")
                time.sleep(tempo_espera)
            else:
                raise Exception(f"Erro na requisição ({response.status_code}): {response.text}")
        except requests.exceptions.RequestException as e:
            tempo_espera = (tentativa + 1) * 3
            print(f"  [Aviso] Falha de conexão: {e}. Aguardando {tempo_espera}s...")
            time.sleep(tempo_espera)
            
    raise Exception(f"Falha após {tentativas} tentativas. O GitHub não respondeu a tempo.")


repositorios = []
cursor = None
data_atual = datetime.now(timezone.utc)
numero_lote = 1

print(f"Iniciando coleta de {TOTAL_ALVO} repositórios em lotes de {BATCH_SIZE} itens...\n")

while len(repositorios) < TOTAL_ALVO:
    
    itens_restantes = TOTAL_ALVO - len(repositorios)
    tamanho_atual = min(BATCH_SIZE, itens_restantes)
    
    print(f"-> Buscando lote #{numero_lote:02d} ({tamanho_atual} itens)...", end=" ")
    
    variaveis = {"first": tamanho_atual, "cursor": cursor}
    resultado = executar_query(query, variaveis)
    
    search_data = resultado["data"]["search"]
    nodes = search_data["nodes"]
    repositorios.extend(nodes)
    
    page_info = search_data["pageInfo"]
    cursor = page_info["endCursor"]
    
    print(f"Concluído! Total acumulado: {len(repositorios)}/{TOTAL_ALVO}")
    numero_lote += 1
    
    if not page_info["hasNextPage"] or len(repositorios) >= TOTAL_ALVO:
        break
    
    time.sleep(1)

repositorios = repositorios[:TOTAL_ALVO]

dados_processados = []
idades = []
prs_lista = []
releases_lista = []

for repo in repositorios:
    nome = repo["nameWithOwner"]
    estrelas = repo["stargazerCount"]
    data_criacao = datetime.fromisoformat(repo["createdAt"].replace("Z", "+00:00"))
    
    # RQ01
    idade_anos = round((data_atual - data_criacao).days / 365.25, 2)
    
    # RQ02
    prs_aceitas = repo["mergedPRs"]["totalCount"]
    
    # RQ03
    total_releases = repo["releases"]["totalCount"]
    
    idades.append(idade_anos)
    prs_lista.append(prs_aceitas)
    releases_lista.append(total_releases)
    
    dados_processados.append({
        "nome": nome,
        "estrelas": estrelas,
        "idade_anos": idade_anos,
        "data_criacao": repo["createdAt"],
        "prs_aceitas": prs_aceitas,
        "releases": total_releases,
        "url": repo["url"]
    })

#CSV
nome_arquivo = f"repositorios_{TOTAL_ALVO}.csv"
with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=dados_processados[0].keys())
    writer.writeheader()
    writer.writerows(dados_processados)

print(f"\n[SUCESSO] {len(dados_processados)} repositórios salvos em '{nome_arquivo}'!\n")

#Estatistica
print("=" * 55)
print(f"       RESUMO ESTATÍSTICO ({TOTAL_ALVO} REPOSITÓRIOS)")
print("=" * 55)

print(f"\n[RQ 01 - IDADE (anos)]")
print(f"  - Mediana: {statistics.median(idades):.2f} anos")
print(f"  - Média:   {statistics.mean(idades):.2f} anos")
print(f"  - Mínimo:  {min(idades):.2f} anos")
print(f"  - Máximo:  {max(idades):.2f} anos")

print(f"\n[RQ 02 - PRs ACEITAS]")
print(f"  - Mediana: {statistics.median(prs_lista):.0f} PRs")
print(f"  - Média:   {statistics.mean(prs_lista):.2f} PRs")
print(f"  - Mínimo:  {min(prs_lista)} PRs")
print(f"  - Máximo:  {max(prs_lista):,} PRs".replace(",", "."))

print(f"\n[RQ 03 - RELEASES]")
print(f"  - Mediana: {statistics.median(releases_lista):.0f} releases")
print(f"  - Média:   {statistics.mean(releases_lista):.2f} releases")
print(f"  - Mínimo:  {min(releases_lista)} releases")
print(f"  - Máximo:  {max(releases_lista):,} releases".replace(",", "."))
print(f"  - Repositórios com 0 releases: {releases_lista.count(0)} ({releases_lista.count(0)}%)")
print("=" * 55)