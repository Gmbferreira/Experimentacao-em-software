from datetime import datetime

from domain.software_repository import SoftwareRepository, SoftwareRepositoryGateway
from infrastructure.github.github_client import GithubClient
from infrastructure.github.queries import SEARCH_POPULAR_REPOSITORIES


class GithubRepositoryGateway(SoftwareRepositoryGateway):
    PAGE_SIZE = 10
    SEARCH_QUERY = "stars:>1 sort:stars-desc"

    def __init__(self, client: GithubClient):
        self._client = client

    def get_popular(self, quantity: int) -> list[SoftwareRepository]:
        results: list[SoftwareRepository] = []
        cursor = None

        while len(results) < quantity:
            page_size = min(self.PAGE_SIZE, quantity - len(results))
            data = self._client.execute(
                SEARCH_POPULAR_REPOSITORIES,
                {"searchQuery": self.SEARCH_QUERY, "first": page_size, "after": cursor},
            )

            search = data["search"]
            for node in search["nodes"]:
                results.append(self._map_to_repository(node))

            if not search["pageInfo"]["hasNextPage"]:
                break
            cursor = search["pageInfo"]["endCursor"]

        return results

    def _map_to_repository(self, node: dict) -> SoftwareRepository:
        return SoftwareRepository(
            name=node["name"],
            owner=node["owner"]["login"],
            url=node["url"],
            stars=node["stargazerCount"],
            created_at=datetime.fromisoformat(node["createdAt"].replace("Z", "+00:00")),
            pushed_at=datetime.fromisoformat(node["pushedAt"].replace("Z", "+00:00")),
            primary_language=node["primaryLanguage"]["name"] if node["primaryLanguage"] else None,
            merged_pull_requests=node["mergedPRs"]["totalCount"],
            releases_count=node["releases"]["totalCount"],
            closed_issues=node["closedIssues"]["totalCount"],
            total_issues=node["totalIssues"]["totalCount"],
        )
