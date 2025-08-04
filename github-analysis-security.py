from fastmcp import FastMCP
import os
from github import Github, Repository, Issue, AuthenticatedUser, Label, Milestone, Issue
from github.GithubObject import NotSet
from typing import Optional


mcp_Analysis_Security= FastMCP(
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

@mcp_Analysis_Security.tool