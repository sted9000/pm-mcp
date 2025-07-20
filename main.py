from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from services.slack import SlackService
from services.projects import get_project_names, get_project_by_name
 
# Initialize FastMCP server
mcp = FastMCP("pm-mcp")

@mcp.tool()
def list_projects() -> list[dict[str, Any]]:
    """Returns a list of projects"""
    return get_project_names()

@mcp.tool()
async def project_summary(project_name: str) -> str:
    """Returns a context and instructions for the writing project summary"""
    project = get_project_by_name(project_name)

    if not project:
        return f"Project {project_name} not found"
    
    slack_client = SlackService()
    
    return f"Context: {slack_client.get_all_messages(project['slack_channel'])}\n\nInstructions: Write a project summary that includes three sections: Overview, Project Timeline, and Outcome. Don't elaborate or add fluff. Put in terms for a simi-technical client."


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
