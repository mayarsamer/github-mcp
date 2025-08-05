import asyncio
from fastmcp import FastMCP, Client

# Importing all the MCP servers
from github_tools.repo_management import mcp_management
from github_tools.issue_tracking import mcp_issue_tracking
from github_tools.pull_request import mcp_pull_request
from github_tools.branch_management import mcp_branch
from github_tools.github_analysis import mcp_analysis


# Creating the main MCP server
main_mcp = FastMCP("github-mcp-server",
              instructions="""This mcp server provides the tools needed to perform github commands like: 
              1- managing repositories
              2- tracking issues
              3- managing branches
              4- performing analytics
              """)

# Mounting each sub-server with a prefix
main_mcp.mount(mcp_management)
main_mcp.mount(mcp_issue_tracking)
main_mcp.mount(mcp_pull_request)
main_mcp.mount(mcp_branch)
main_mcp.mount(mcp_analysis)

#Optional: to test function to verify mounted tools
async def list_all_tools():
    tools = await main_mcp.get_tools()
    print("Mounted tools:", list(tools.keys()))
    

if __name__ == "__main__":
    main_mcp.run(
        transport="http",
        host="0.0.0.0",
        port=9000
    )
