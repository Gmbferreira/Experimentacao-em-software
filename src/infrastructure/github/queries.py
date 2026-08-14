SEARCH_POPULAR_REPOSITORIES = """
query($searchQuery: String!, $first: Int!, $after: String) {
  search(query: $searchQuery, type: REPOSITORY, first: $first, after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        name
        url
        stargazerCount
        createdAt
        pushedAt
        primaryLanguage { name }
        owner { login }
        mergedPRs: pullRequests(states: MERGED) { totalCount }
        releases { totalCount }
        closedIssues: issues(states: CLOSED) { totalCount }
        totalIssues: issues { totalCount }
      }
    }
  }
}
"""