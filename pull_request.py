from fastmcp import FastMCP
import os
from github import Github, Repository, Issue, AuthenticatedUser, Label, Milestone, Issue
from github.GithubObject import NotSet
from typing import Optional


mcp_pull_request = FastMCP(
    name="mcpPRs",
    instructions="""
        This server is to help you perform actions on github 
    """,
)
 
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN environment variable not set.")

g = Github(token)
user = g.get_user()


#------------------------------------------------------------------------------------------

@mcp_pull_request.tool
def create_pull_request(
    repo_name: str,
    base_branch: str,
    head_branch: str,
    pr_title: str,
    pr_body: str = NotSet
) -> dict:
    """
    Create a new pull request in the specified GitHub repository.

    Args:
        repo_name (str): repository name .
        base_branch (str): The branch you want to merge into (usually "main" or "master").
        head_branch (str): The branch containing the proposed changes.
        pr_title (str): Title of the pull request.
        pr_body (str, optional): Description/body of the pull request.

    Returns:
        dict: Dictionary containing the pull request title, number, state, and URL.
    """
    repo = user.get_repo(repo_name)
    pr = repo.create_pull(
        base=base_branch,
        head=head_branch,
        title=pr_title,
        body=pr_body
    )

    return {
        "title": pr.title,
        "number": pr.number,
        "state": pr.state,
        "url": pr.html_url
    }



#---------------------------------------------------------------------------------------------------

@mcp_pull_request.tool
def get_pull_request_details(repo_name: str, pr_number: int) -> dict:

    """
    Get details of a specific pull request from the repository.

    Args:
        repo_name (str): name of the repo 
        pr_number (int): Pull request number

    Returns:
        dict: Information about the pull request (title, state, user, base, head, etc.)
    """

    repo = user.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    return {
        "title": pr.title,
        "state": pr.state,
        "user": pr.user.login,
        "created_at": str(pr.created_at),
        "updated_at": str(pr.updated_at),
        "base_branch": pr.base.ref,
        "head_branch": pr.head.ref,
        "body": pr.body,
        "merged": pr.merged,
        "mergeable_state": pr.mergeable_state,
    }



#--------------------------------------------------------------------------------------------------------

@mcp_pull_request.tool
def list_open_pull_requests(repo_name: str):

    """
    List all open pull requests for a given GitHub repository.

    Args:
        repo_name (str): the name of the repository

    Returns:
        list: A list of dictionaries containing title, number, and URL for each open pull request.
    """

    repo = user.get_repo(repo_name)
    pulls = repo.get_pulls(state="open")
    
    return [
        {
            "title": pr.title,
            "number": pr.number,
            "url": pr.html_url
        }
        for pr in pulls
    ]


#--------------------------------------------------------------------------------------------------------


@mcp_pull_request.tool
def list_recently_updated_prs(repo_name: str):
    """
    List PRs sorted by most recently updated.
    """
    repo = user.get_repo(repo_name)
    pulls = repo.get_pulls(state="open", sort="updated", direction="desc")
    return [{"title": pr.title, "updated_at": str(pr.updated_at), "url": pr.html_url} for pr in pulls]


#--------------------------------------------------------------------------------------------------------


@mcp_pull_request.tool
def list_pr_comments(repo_name: str, pr_number: int):
    """
    Lists all review comments on a pull request.

    Args:
        repo_name (str): Repository in the form "owner/repo"
        pr_number (int): The pull request number

    Returns:
        List[str]: A list of comment bodies
    """
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    comments = pr.get_comments()
    
    return [comment.body for comment in comments]


#--------------------------------------------------------------------------------------------------------


@mcp_pull_request.tool
def close_all_pull_request(repo_name):

    """
    Close all open pull requests in the given repository.
    """
    repo = user.get_repo(repo_name)
    open_pulls = repo.get_pulls(state='open')
    
    for pr in open_pulls:
        pr.edit(state="closed")
        print(f"Closed PR #{pr.number}: {pr.title}")


if __name__ == "__main__":
    mcp_pull_request.run(transport="http")