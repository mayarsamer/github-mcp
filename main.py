import asyncio
from fastmcp import FastMCP, Client

# Importing all the MCP servers
from issue_tracking import mcp_issue_tracking
from pull_request import mcp_pull_request
from branch_management import mcp_branch
from github_analysis import mcp_analysis


# Creating the main MCP server
main_mcp = FastMCP(name="MainAppLive")

# Mounting each sub-server with a prefix
main_mcp.mount(mcp_issue_tracking, prefix="dynamic")
main_mcp.mount(mcp_pull_request, prefix="dashboard")
main_mcp.mount(mcp_branch, prefix="model")
main_mcp.mount(mcp_analysis, prefix="user")

#Optional: to test function to verify mounted tools
async def list_all_tools():
    tools = await main_mcp.get_tools()
    print("Mounted tools:", list(tools.keys()))
    

if __name__ == "__main__":
    asyncio.run(list_all_tools())  #justto test
    main_mcp.run(transport="http")
