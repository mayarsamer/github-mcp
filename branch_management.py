from fastmcp import FastMCP
import os
from github import Github, Repository, Issue, AuthenticatedUser, Label, Milestone, Issue
from github.GithubObject import NotSet
from typing import Optional


mcp_branch= FastMCP(
    name="mcp-github",
    instructions="""
        This server is to help you perform actions on github 
    """,
)
 
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN environment variable not set.")

g = Github(token)
user = g.get_user()

@mcp_branch.tool
def list_branches_in_repo(repo_name: str):

    """
    List all branches in a given GitHub repository.

    Args:
        repo_name (str): The name of the repository (e.g., "PyGithub/PyGithub").

    Returns:
        list: A list of branch names available in the repository.
    """
    repo = user.get_repo(repo_name)
    branches = repo.get_branches()
    return [branch.name for branch in branches]

    
#---------------------------------------------------------------------------------------------------


@mcp_branch.tool
def get_default_branch(repo_name: str):
    """
    Get the default branch of a GitHub repository.

    Args:
        repo_name (str): name of repository 

    Returns:
        dict: A dictionary containing the default branch name and a short SHA of its latest commit.
    """

    repo = user.get_repo(repo_name)
    default_branch_name = repo.default_branch
    branch = repo.get_branch(default_branch_name)

    return {
        "name": branch.name,
        "latest_commit_sha": branch.commit.sha[:7],
    }

    

if __name__ == "__main__":
    mcp_branch.run(transport="http")
