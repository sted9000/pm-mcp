# PM-MCP (Project Management Model Context Protocol)

A local Model Context Protocol (MCP) server that provides project management tools and integrations for AI assistants. This server is meant to provide two pieces of context to the LLM (and then let the LLM do the heavy lifting):
1. Context about the project (slack messages, git commits, google docs, etc.)
2. Writing instructions for the LLM to write a specified type of documents (e.g. a project summary, meeting agenda, onboarding guide, etc.)

## Principles
- **Low Config**: Just tell the LLM what project yo are working on
- **Extensible**: Add more 3rd party integrations and document types as needed.
- **Client as the Work Horse**: The server should be a tool for the LLM get context and then get out of the way and let the LLM do what it is good at.

## Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) (Python package manager)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/sted9000/pm-mcp.git
cd pm-mcp
```

2. Install dependencies:
```bash
uv pip install -e .
```

3. Configure your services:
   - Copy `config.yaml.example` to `config.yaml` (if not already present)
   - Add your Slack API token and other service credentials

## Claude Desktop Installation

To use PM-MCP with Claude Desktop, follow these steps:

1. Make sure you have Claude Desktop installed on your system

2. Open your Claude Desktop configuration file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/claude/claude_desktop_config.json`

3. Add the PM-MCP server to your configuration:

```json
{
  "mcpServers": {
    "pm-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/pm-mcp",
        "run",
        "pm-mcp"
      ]
    }
  }
}
```

4. Replace `/path/to/pm-mcp` with the actual path to your pm-mcp directory

5. Restart Claude Desktop to load the new MCP server

## Usage

Once installed, PM-MCP provides the following tools in Claude:

### Available Tools

- **`list_projects`**: Returns a list of all configured projects
- **`project_summary`**: Generates a summary for a specific project including:
  - Overview
  - Project Timeline
  - Outcome

### Example Usage

In Claude, you can use these tools by asking:

- "List all my projects"
- "Give me a summary of the [project name] project"

## Configuration

The `config.yaml` file should contain:

```yaml
slack:
  token: "your-slack-bot-token"

projects:
  - name: "Project Name"
    slack_channel: "channel-id"
    # Additional project configuration
```

## Development

To add new tools or services, create a new module in the `services/` directory and register tools using the `@mcp.tool()` decorator in `main.py`.

## TODO

### Documents/Tools to Add
- [ ] Onboarding guide generator
- [ ] Weekly summary generator

### Services/Connections to Add
- [ ] GitHub integration (commit history)
- [ ] Google Docs integration
- [ ] Meeting transcriptions integration

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.