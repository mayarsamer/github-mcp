from fastmcp import FastMCP
import json
import requests
import os
from github import Github, Repository, Issue, AuthenticatedUser
from github.GithubObject import NotSet


mcp_management = FastMCP(
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



#repository management (creating and deleting repos)
#first tool is creating a repo
@mcp_management.tool
def create_github_repo(
    name: str,
    private: bool = NotSet
) -> str:
    """
    Create a GitHub repository with the given parameters.
    Returns the URL of the newly created repo.
    """
    repo = user.create_repo(
        name=name,
        private=private
    )
    return f"✅ Repository '{repo.name}' created successfully at {repo.html_url}"


#---------------------------------------------------------------------------------------------------


#second tool is deleting a repo
@mcp_management.tool
def delete_github_repo(repo_name: str) -> None:
    """
    Deletes the repository owned by user.
    
    Args:
        repo_name (str): Name of the repo to delete.
    
    Raises:
        github.GithubException if repo not found or delete fails.
    """

    repo = user.get_repo(repo_name)  
    
    #confirm = input(f"⚠️ Are you sure you want to delete '{repo_name}'? This cannot be undone! (yes/no): ").strip().lower()
    #if confirm != "yes":
    #    print("Deletion cancelled.")
    
    repo.delete()  # This calls the GitHub DELETE /repos/{owner}/{repo} API
    
    return f"✅ Repository '{repo_name}' deleted successfully."


#---------------------------------------------------------------------------------------------------


#third toold is listing all the current repos
@mcp_management.tool
def list_github_repos() -> list[str]:
    """
    Returns a list of repo names for the user.
    
    """

    repos = user.get_repos()
    return [repo.name for repo in repos]



if __name__ == "__main__":
    mcp_management.run(transport="http")