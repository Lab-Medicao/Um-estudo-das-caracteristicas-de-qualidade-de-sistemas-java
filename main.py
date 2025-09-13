import requests
import csv
import os

GITHUB_TOKEN = "REMOVED"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def fetch_top_java_repos(filename='top_java_repos.csv', total=1000):
    repos = []
    per_page = 100
    for page in range(1, (total // per_page) + 1):
        url = f'https://api.github.com/search/repositories?q=language:Java&sort=stars&order=desc&per_page={per_page}&page={page}'
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Erro na página {page}: {response.status_code} - {response.text}")
            break
        data = response.json()
        for item in data.get('items', []):
            repos.append({
                'name': item['full_name'],
                'url': item['html_url'],
                'clone_url': item['clone_url'],
                'stars': item['stargazers_count']
            })
    with open(filename, 'w', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'url', 'clone_url', 'stars'])
        writer.writeheader()
        writer.writerows(repos)
    print(f"Arquivo '{filename}' gerado com {len(repos)} repositórios.")

def main():
    print("== Coletor de Repositórios Java no GitHub ==")
    fetch_top_java_repos()
    print("Arquivo 'top_java_repos.csv' gerado com sucesso.")

if __name__ == "__main__":
    main()
