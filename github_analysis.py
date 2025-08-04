from fastmcp import FastMCP
import os
from github import Github, Repository, Issue, AuthenticatedUser, Label, Milestone, Issue
from github.GithubObject import NotSet
from typing import Optional
from datetime import datetime
from collections import defaultdict


mcp_analysis= FastMCP(
    name="mcp_analysis",
    instructions="""
        This server is to help you perform actions on github 
    """,
)
 
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN environment variable not set.")

g = Github(token)
user = g.get_user()

@mcp_analysis.tool
def get_repo_key_metrics(repo_name: str) -> dict:
    """
    Retrieve key metrics for a GitHub repository.

    Args:
        repo_name (str): name of the repository

    Returns:
        dict: Key metrics including stars, forks, watchers, open issues, etc.
    """
    repo = user.get_repo(repo_name)
    
    return {
        "name": repo.full_name,
        "description": repo.description,
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
        "watchers": repo.watchers_count,
        "subscribers": repo.subscribers_count,
        "open_issues": repo.open_issues_count,
        "size_kb": repo.size,
        "language": repo.language,
        "created_at": repo.created_at.isoformat(),
        "updated_at": repo.updated_at.isoformat(),
        "default_branch": repo.default_branch,
    }


#-------------------------------------------------------------------------------------------------



@mcp_analysis.tool
def top_contributors(repo_name: str, start_date: str, end_date: str) -> dict:

    """
    Calculate top contributors by commits, pull requests, and issues within a timeframe.

    Args:
        repo_name (str): the repo name 
        start_date (str): Start date in ISO format (e.g. "2024-01-01T00:00:00").
        end_date (str): End date in ISO format (e.g. "2024-12-31T23:59:59").

    Returns:
        dict: Mapping of usernames to their counts of commits, PRs, and issues.
    """

    repo = user.get_repo(repo_name)
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)

    contributors = defaultdict(lambda: {"commits": 0, "pull_requests": 0, "issues": 0})

    # Count commits per author in timeframe
    for commit in repo.get_commits(since=start_dt, until=end_dt):
        author = commit.author.login if commit.author else "Unknown"
        contributors[author]["commits"] += 1

    # Count pull requests per user in timeframe
    for pr in repo.get_pulls(state="all", sort="created", direction="asc"):
        if pr.created_at >= start_dt and pr.created_at <= end_dt:
            author = pr.user.login if pr.user else "Unknown"
            contributors[author]["pull_requests"] += 1

    # Count issues per creator in timeframe (exclude PRs because issues includes them)
    for issue in repo.get_issues(state="all", since=start_dt):
        if issue.created_at <= end_dt and not issue.pull_request:
            author = issue.user.login if issue.user else "Unknown"
            contributors[author]["issues"] += 1

    return dict(contributors)


#-------------------------------------------------------------------------------------------

if __name__ == "__main__":
    mcp_analysis.run(transport="http")