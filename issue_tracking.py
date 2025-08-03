from fastmcp import FastMCP
import json
import requests
import os
from github import Github, Repository, Issue, AuthenticatedUser, Label, Milestone, Issue
from github.GithubObject import NotSet
from typing import Optional


#create the mcp server using the fastmcp library
mcp_issue_tracking = FastMCP(
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

@mcp_issue_tracking.tool
def create_issue(
    repo_name: str,       
    issue_title: str,
    issue_body: str = NotSet,
    label_name: Optional[list[str]] = NotSet,
    assignee_username: Optional[list[str]] = NotSet
) -> str:
    """
    Creates an issue in the specified repository.

    Args:
        repo_name (str): The name of the repo .
        issue_title (str): Title of the issue
        issue_body (str): Body content of the issue
        label_name Optional[list[str]]: Name of the labels to assign
        assignee_username Optional[list[str]]): GitHub username to assign the issue to

    Returns:
        str: Summary string of the created issue (title and issue number)
    """
    repo = user.get_repo(repo_name)



    issue = repo.create_issue(
        title=issue_title,
        body=issue_body,
        labels=label_name,
        assignee=assignee_username
    )

    return f"Issue created: {issue.title} (#{issue.number})"

@mcp_issue_tracking.tool
def get_issue_from_repo(repo_name: str, issue_number: int):
    """
        Retrieve detailed information about a specific issue from a GitHub repository.

        Args:
            repo_name (str): The full name of the repository (e.g., "owner/repo").
            issue_number (int): The number of the issue to retrieve.

        Returns:
            dict: A dictionary containing the following keys:
                - title (str): The title of the issue.
                - number (int): The issue number.
                - state (str): The current state of the issue ("open" or "closed").
                - labels (List[str]): A list of label names assigned to the issue.
                - body (str): A preview of the issue body (first 200 characters).
                - url (str): The URL to view the issue on GitHub.
        """

    repo = user.get_repo(repo_name)
    issue = repo.get_issue(number=issue_number)
    
    return {
        "title": issue.title,
        "number": issue.number,
        "state": issue.state,
        "labels": [label.name for label in issue.labels],
        "body": issue.body[:200] + ("..." if issue.body and len(issue.body) > 200 else ""),
        "url": issue.html_url
    }


@mcp_issue_tracking.tool
def close_issue(repo_name: str, issue_number: int):
    """
    Close a specific issue in a repository.

    Args:
        repo_name (str): The name of the repo .
        issue_number (int): The issue number to close.

    Returns:
        dict: A confirmation message with the issue number and title.
    """

    repo = user.get_repo(repo_name)
    issue = repo.get_issue(number=issue_number)
    
    issue.edit(state='closed')
    
    return {
        "message": f"Issue #{issue.number} closed.",
        "title": issue.title
    }


@mcp_issue_tracking.tool
def close_all_open_issues(repo_name: str):
    """
    Close all open issues in a given repository.

    Args:
        repo_name (str): The name of the repo .

    Returns:
        dict: A summary of how many issues were closed.
    """

    repo = user.get_repo(repo_name)

    open_issues = repo.get_issues(state='open')
    closed_count = 0

    for issue in open_issues:
        issue.edit(state='closed')
        closed_count += 1

    return {"closed_issues": closed_count}

if __name__ == "__main__":
    mcp_issue_tracking .run(transport="http")
