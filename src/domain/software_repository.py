from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SoftwareRepository:
    name: str
    owner: str
    url: str
    stars: int
    created_at: datetime
    pushed_at: datetime
    primary_language: str | None
    merged_pull_requests: int
    releases_count: int
    closed_issues: int
    total_issues: int


class SoftwareRepositoryGateway(ABC):
    @abstractmethod
    def get_popular(self, quantity: int) -> list[SoftwareRepository]:
        ...
