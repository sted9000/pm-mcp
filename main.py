from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from services.slack import SlackService
from services.projects import get_project_names, get_project_by_name
from services.meetings import get_meeting_notes
from datetime import datetime
import yaml

with open('writing_instructions.yaml', 'r') as file:
    writing_instructions = yaml.safe_load(file)

 
# Initialize FastMCP server
mcp = FastMCP("pm-mcp")

@mcp.tool()
def list_projects() -> list[dict[str, Any]]:
    """Returns a list of projects"""
    return get_project_names()


@mcp.tool()
def project_summary(project_name: str) -> str:
    """
    Returns a data and instructions needed for writing a project summary.
    
    Note this is not a prerequisite for the project update tool.
    """
    project = get_project_by_name(project_name)

    if not project:
        return f"Project {project_name} not found"
    
    slack_client = SlackService()

    try:    
        messages = slack_client.get_all_messages(project['slack_channel'])

        if not messages:
            return f"No messages found for project {project_name}"
        
        return f"Context: {messages}\n\nInstructions: {writing_instructions['project_summary']}"
    
    except Exception as e:
        return f"Error fetching messages: {str(e)}"
    

@mcp.tool()
def project_updates(project_name: str, start_date: datetime, end_date: datetime) -> str:
    """
    Returns the data and instructions needed for writing a project update.
    
    Note this is not a prerequisite for the project summary tool.
    """
    project = get_project_by_name(project_name)
    
    if not project:
        return f"Project {project_name} not found"
    
    slack_client = SlackService()
    
    try:
        messages = slack_client.get_all_messages(
            channel_id=project['slack_channel'],
            oldest=start_date,
            latest=end_date
        )

        meeting_notes = get_meeting_notes(project['meeting_directory'])

        if not messages:
            return f"No messages found between {start_date} and {end_date}"
        
        return f"Context:\n\n- Slack Messages: {messages}\n- Meeting Notes: {meeting_notes};\n\nInstructions: {writing_instructions['project_update']}"
    except Exception as e:
        return f"Error fetching messages: {str(e)}"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
