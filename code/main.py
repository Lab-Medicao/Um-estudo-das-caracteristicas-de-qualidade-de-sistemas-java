import time
import csv
import requests
from tqdm import tqdm
from utils.utils import get_github_token

GRAPHQL_URL = "https://api.github.com/graphql"
MAX_REPOS = 1000
BATCH_SIZE = 25
MAX_RETRIES = 5

def make_graphql_request(query, variables, headers, max_retries=MAX_RETRIES):
    """
    Faz uma requisição GraphQL ao GitHub com retries e backoff exponencial.
    """
    for attempt in range(max_retries):
        response = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables}, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                raise Exception(f"[ERRO] {data['errors']}")
            return data

        wait_time = 2 ** attempt
        print(f"Erro {response.status_code}, retry em {wait_time}s...")
        time.sleep(wait_time)

    raise Exception(f"Falha após {max_retries} tentativas: {response.text}")


def fetch_repositories(total, batch_size):
    """
    Busca os repositórios mais populares em Java com paginação.
    """
    token = get_github_token()
    headers = {"Authorization": f"Bearer {token}"}

    query = """
    query($after: String, $batch_size: Int!) {
      search(query: "language:Java sort:stars-desc", type: REPOSITORY, first: $batch_size, after: $after) {
        pageInfo {
          endCursor
          hasNextPage
        }
        edges {
          node {
            ... on Repository {
              name
              owner { login }
              url
              stargazerCount
              createdAt
              pushedAt
              updatedAt
              primaryLanguage { name }
              releases {
                totalCount
              }
              defaultBranchRef {
                target {
                  ... on Commit {
                    history {
                      totalCount
                    }
                  }
                }
              }
              languages(first: 10) {
                edges {
                  size
                  node {
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
    """

    repos = []
    after_cursor = None

    with tqdm(total=total, desc="Coletando repositórios", unit="repo") as pbar:
        while len(repos) < total:
            variables = {"after": after_cursor, "batch_size": batch_size}
            result = make_graphql_request(query, variables, headers)

            search = result["data"]["search"]
            for edge in search["edges"]:
                node = edge["node"]
                
                from datetime import datetime
                created_date = datetime.fromisoformat(node["createdAt"].replace('Z', '+00:00'))
                age_years = (datetime.now().astimezone() - created_date).days / 365.25
                
                total_size = sum(edge["size"] for edge in node["languages"]["edges"])
                
                repos.append({
                    # "name": f"{node['owner']['login']}/{node['name']}",
                    "name": node["name"],
                    "owner": node["owner"]["login"],
                    "url": node["url"],
                    "stars": node["stargazerCount"],
                    "created_at": node["createdAt"],
                    "pushed_at": node["pushedAt"],
                    "updated_at": node["updatedAt"],
                    "language": node["primaryLanguage"]["name"] if node["primaryLanguage"] else None,
                    "releases_count": node["releases"]["totalCount"],
                    "commits_count": node["defaultBranchRef"]["target"]["history"]["totalCount"] if node["defaultBranchRef"] else 0,
                    "age_years": round(age_years, 2),
                    "size_bytes": total_size
                })
                pbar.update(1)

                if len(repos) >= total:
                    break

            if not search["pageInfo"]["hasNextPage"]:
                break

            after_cursor = search["pageInfo"]["endCursor"]

    return repos


def save_to_csv(repos, filename="top_java_repos.csv"):
    """
    Salva os repositórios em um arquivo CSV.
    """
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "owner", "url", "stars", "created_at", "pushed_at", "updated_at", 
                       "language", "releases_count", "commits_count", "age_years", "size_bytes"]
        )
        writer.writeheader()
        writer.writerows(repos)


def main():
    print("== Coletor de Repositórios Java no GitHub ==")
    start_time = time.time()

    repos = fetch_repositories(total=MAX_REPOS, batch_size=BATCH_SIZE)
    save_to_csv(repos)

    end_time = time.time()
    elapsed = end_time - start_time

    print(f"Arquivo 'top_java_repos.csv' gerado com {len(repos)} repositórios.")
    print(f"✅ Tempo total de execução: {elapsed:.2f} segundos")



if __name__ == "__main__":
    main()
