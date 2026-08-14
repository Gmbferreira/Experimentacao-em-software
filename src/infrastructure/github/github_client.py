# Responsável pela comunicação HTTP com o GitHub.

import os
import requests

class GithubClient:
    GITHUB_GRAPHQL_URL = os.getenv('GITHUB_GRAPHQL_URL')
    

    def __init__(self, token: str| None = None):
        self._token = token or os.getenv('TOKEN_GITHUB_GRAPHQL_URL')
        if not self._token:
            raise ValueError("GITHUB_TOKEN não configurado (verifique o .env)")
    
    def execute(self, query:str, variables: dict | None = None) -> dict:
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type":"application/json",
        }
        body = {"query":query,"variables":variables or {}}
        
        response = requests.post( self.GITHUB_GRAPHQL_URL, json=body, headers=headers, timeout=30)
        response.raise_for_status()
        payload = response.json()
        if "errors" in payload:
            raise RuntimeError(payload["errors"])
        return payload['data']
    
    def get_rate_limit(self) -> dict:
        query = """
        query {
          rateLimit {
            limit
            remaining
            resetAt
          }
        }
        """
        return self.execute(query)["rateLimit"]
           
    