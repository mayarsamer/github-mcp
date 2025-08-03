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
    issue_body: str = "",
    label_name: Optional[str] = None,
    assignee_username: Optional[str] = None,
    milestone_title: Optional[str] = None
) -> str:
    """
    Creates an issue in the specified repository.

    Args:
        repo_name (str): The name of the repo .
        issue_title (str): Title of the issue
        issue_body (str): Body content of the issue
        label_name (Optional[str]): Name of the label to assign
        assignee_username (Optional[str]): GitHub username to assign the issue to
        milestone_title (Optional[str]): Title of the milestone to associate

    Returns:
        str: Summary string of the created issue (title and issue number)
    """
    repo = g.get_repo(repo_name)

    labels = []
    if label_name:
        labels.append(repo.get_label(label_name))

    milestone = None
    if milestone_title:
        milestone = repo.create_milestone(milestone_title)

    issue = repo.create_issue(
        title=issue_title,
        body=issue_body,
        labels=labels,
        assignee=assignee_username,
        milestone=milestone
    )

    return f"Issue created: {issue.title} (#{issue.number})"

@mcp_issue_tracking.tool
def get_issue_from_repo(repo_name: str, issue_number: int):
    """
    Get a specific issue from a GitHub repository.

    Args:
        repo_name (str): The name of the repo.
        issue_number (int): The number of the issue to retrieve.

    Returns:
        dict: A dictionary containing issue title and number.
    """

    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_number)

    return {
        "title": issue.title,
        "number": issue.number
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

    repo = g.get_repo(repo_name)
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

    repo = g.get_repo(repo_name)

    open_issues = repo.get_issues(state='open')
    closed_count = 0

    for issue in open_issues:
        issue.edit(state='closed')
        closed_count += 1

    return {"closed_issues": closed_count}

if __name__ == "__main__":
    mcp_issue_tracking .run(transport="http")
