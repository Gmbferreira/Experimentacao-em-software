from dotenv import load_dotenv

load_dotenv()

import pandas as pd

from application.use_cases.get_popular_repositories import GetPopularRepositories
from infrastructure.github.github_client import GithubClient
from infrastructure.github.github_repository import GithubRepositoryGateway


def main():
    client = GithubClient()
    gateway = GithubRepositoryGateway(client)
    use_case_get_popular_repositories = GetPopularRepositories(gateway)

    repositories = use_case_get_popular_repositories.execute(100)

    df = pd.DataFrame([repo.__dict__ for repo in repositories])
    output_path = "data/raw/repositories_100.csv"
    df.to_csv(output_path, index=False)

    print(f"Salvos {len(repositories)} repositórios em {output_path}")


if __name__ == "__main__":
    main()
