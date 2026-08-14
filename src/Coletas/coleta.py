import requests
import json
import os
from datetime import datetime, timezone

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ENDPOINT = "https://api.github.com/graphql"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

query = """
query getTopRepositories($cursor: String) {
  search(query: "stars:>10000 sort:stars-desc", type: REPOSITORY, first: 10, after: $cursor) {
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

def executar_query(query, variables=None):
    payload = {"query": query, "variables": variables or {}}
    response = requests.post(ENDPOINT, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro na requisição ({response.status_code}): {response.text}")

print("Iniciando coleta de dados (RQ01 + RQ02 + RQ03)...")
resultado = executar_query(query)

repositorios = resultado["data"]["search"]["nodes"]
data_atual = datetime.now(timezone.utc)

print(f"\nColetados {len(repositorios)} repositórios com sucesso!\n")

for repo in repositorios:
    nome = repo["nameWithOwner"]
    estrelas = repo["stargazerCount"]
    data_criacao = datetime.fromisoformat(repo["createdAt"].replace("Z", "+00:00"))
    
    # RQ01:
    idade_anos = (data_atual - data_criacao).days / 365.25
    
    # RQ02: 
    prs_aceitas = repo["mergedPRs"]["totalCount"]
    
    # RQ03: 
    total_releases = repo["releases"]["totalCount"]
    
    print(f"Repositório: {nome}")
    print(f"  - Estrelas: {estrelas:,}".replace(",", "."))
    print(f"  - Idade (RQ01): ~{idade_anos:.1f} anos")
    print(f"  - PRs Aceitas (RQ02): {prs_aceitas:,}".replace(",", "."))
    print(f"  - Total de Releases (RQ03): {total_releases:,}".replace(",", "."))
    print("-" * 40)