import os

import pytest
from dotenv import load_dotenv

from infrastructure.github.github_client import GithubClient

load_dotenv()


@pytest.mark.integration
def test_execute_rate_limit_against_real_api():
    token = os.getenv("TOKEN_GITHUB_GRAPHQL_URL")
    if not token:
        pytest.skip("TOKEN_GITHUB_GRAPHQL_URL não configurado")

    client = GithubClient(token=token)

    rate_limit = client.get_rate_limit()

    assert "remaining" in rate_limit
    assert "limit" in rate_limit
    assert rate_limit["remaining"] >= 0


@pytest.mark.integration
def test_execute_raises_with_invalid_token():
    client = GithubClient(token="token-invalido-de-proposito")

    with pytest.raises(Exception):
        client.execute("query { viewer { login } }")
