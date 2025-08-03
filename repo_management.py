from fastmcp import FastMCP
import json
import requests
import os
from github import Github, Repository, Issue, AuthenticatedUser


#create the mcp server using the fastmcp library
mcp = FastMCP(
    name="mcp-github",
    instructions="""
        This server is to help you perform actions on github through our LLM
    """,
)
#export the token in the terminal then call it back for security purposes 
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN environment variable not set.")

g = Github(token)

user = g.get_user()



#repository management (creating and deleting repos)
#first tool is creating a repo
@mcp.tool
def create_github_repo(
    name: str,
    description: str = "",
    private: bool = False,
    auto_init: bool = True,
) -> str:
    """
    Create a GitHub repository with the given parameters.
    Returns the URL of the newly created repo.
    """
    repo = user.create_repo(
        name=name,
        description=description or None,
        private=private,
        auto_init=auto_init,
        has_issues=True,
        has_wiki=True,
        allow_squash_merge=True,
        allow_merge_commit=True,
        allow_rebase_merge=True,
        delete_branch_on_merge=True
    )
    return f"✅ Repository '{repo.name}' created successfully at {repo.html_url}"

#second tool is deleting a repo
@mcp.tool
def delete_github_repo(repo_name: str) -> None:
    """
    Deletes the repository owned by user.
    
    Args:
        repo_name (str): Name of the repo to delete.
    
    Raises:
        github.GithubException if repo not found or delete fails.
    """

    repo = user.get_repo(repo_name)  
    
    confirm = input(f"⚠️ Are you sure you want to delete '{repo_name}'? This cannot be undone! (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return
    
    repo.delete()  # This calls the GitHub DELETE /repos/{owner}/{repo} API
    
    print(f"✅ Repository '{repo_name}' deleted successfully.")


#third toold is listing all the current repos
@mcp.tool
def list_github_repos(repo_name: str) -> list[str]:
    """
    Returns a list of repo names for the user.
    
    """

    repos = user.get_repos()
    return [repo.name for repo in repos]




    
    


    

if __name__ == "__main__":
    mcp.run()