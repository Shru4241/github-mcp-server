# Technical Decisions

This document explains the major technical decisions made while developing the GitHub MCP Server and the reasoning behind them.

## 1. Why Python?

Python was chosen because it is simple, widely used, and provides strong support for API integration, automation, and AI-related applications. It also provides good support for building MCP servers.

## 2. Why Model Context Protocol (MCP)?

MCP was chosen because it provides a standard way for AI assistants to interact with external tools and services.

In this project, MCP allows an AI assistant or MCP client to interact with GitHub through defined tools instead of directly handling GitHub API requests.

## 3. Why FastMCP?

FastMCP was chosen because it provides a simple way to create MCP tools using Python functions.

It reduces boilerplate code and makes it easier to expose GitHub operations as reusable MCP tools.

## 4. Why GitHub REST API?

The GitHub REST API was chosen because it provides the operations required by this project.

The API allows the server to manage:

- Repositories
- Issues
- Files
- Branches
- Pull Requests

This makes it suitable for building a GitHub automation server.

## 5. Why Requests?

The `requests` library was chosen because it provides a simple and reliable way to send HTTP requests to the GitHub REST API.

It supports the HTTP methods required by this project, including:

- GET
- POST
- PUT
- PATCH
- DELETE

## 6. Why Environment Variables?

The GitHub Personal Access Token is stored in a `.env` file instead of directly inside the Python source code.

`python-dotenv` is used to load the token from the environment.

This approach helps prevent accidentally exposing the GitHub token in the source code.

**Important:** The `.env` file must never be committed to GitHub.

## 7. Why STDIO Communication?

STDIO was chosen because MCP clients can communicate with the server through standard input and output.

This makes the server simple to run locally and suitable for MCP client integration.

## 8. Why Separate MCP Tools?

GitHub operations were divided into separate MCP tools instead of creating one large function.

For example:

- `get_repo_info`
- `create_issue`
- `create_repository`
- `get_repo_files`
- `create_branch`
- `create_pull_request`
- `merge_pull_request`

This makes each operation focused, reusable, and easier for an MCP client to understand and use.

## 9. Why MCP Inspector?

MCP Inspector was chosen to test and verify the MCP server during development.

It allowed each tool to be tested independently before using the server with an actual MCP client.

## 10. Why GitHub REST API Instead of Direct Git Commands?

The GitHub REST API was chosen because the goal of this project is to provide programmatic GitHub operations through MCP tools.

Using the API allows the server to perform GitHub operations without requiring the user to manually execute Git commands.


## 11. Why Support Repository, Issue, File, Branch and Pull Request Operations?

These operations were selected because they represent common GitHub development workflows.

The server can perform a workflow such as:

```text
Create Branch
      ↓
Create / Update File
      ↓
Create Pull Request
      ↓
Review Changes
      ↓
Merge Pull Request
```

It can also manage issues and repositories as part of GitHub project management.

## 12. Why Use a Virtual Environment?

A Python virtual environment was used to isolate the project's dependencies from other Python projects on the system.

This helps avoid dependency conflicts and makes the project easier to reproduce.

## 13. Why requirements.txt?

A `requirements.txt` file was used to keep track of the Python packages required by the project.

The main dependencies are:

- `mcp`
- `requests`
- `python-dotenv`

A new developer can install the dependencies using:

```bash
pip install -r requirements.txt

## Conclusion

The overall architecture was designed to keep the system simple, modular, and easy to extend.

The main design is:

```text
AI Assistant / MCP Client
          ↓
    FastMCP Server
          ↓
      MCP Tools
          ↓
    GitHub REST API
          ↓
   GitHub Resources