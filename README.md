# GitHub MCP Server

A Python-based Model Context Protocol (MCP) server that allows AI assistants and MCP clients to interact with GitHub through tools.

The server uses the GitHub REST API and provides tools for repository management, issue management, file operations, branches, and pull requests.

## 🏗️ Architecture

```text
                         User
                          |
                          v
                 AI Assistant / MCP Client
                          |
                          v
                  GitHub MCP Server
                     (FastMCP)
                          |
                          v
                   MCP Tool Selection
                          |
             +------------+------------+
             |            |            |
             v            v            v
       Repository       Issues       Files
          Tools          Tools        Tools
             |            |            |
             +------------+------------+
                          |
             +------------+------------+
             |                         |
             v                         v
        Branches                 Pull Requests
          Tools                      Tools
             |                         |
             +------------+------------+
                          |
                          v
                  GitHub REST API
                          |
                          v
                  GitHub Repositories
                          |
                          v
                  API Response / Data
                          |
                          v
                 GitHub MCP Server
                          |
                          v
                   Final Response
                          |
                          v
                         User

                         
```

## Features

- Get GitHub repository information
- List a user's repositories
- Get open issues from a repository
- Create GitHub issues
- Create GitHub repositories
- Search GitHub repositories
- Add comments to issues
- Close GitHub issues
- List repository files and folders
- Read repository file contents
- Create or update repository files
- Create GitHub branches
- Create pull requests
- Merge pull requests
- Delete repository files

## Technologies Used

- Python
- Model Context Protocol (MCP)
- FastMCP
- GitHub REST API
- Requests
- python-dotenv
- MCP Inspector

## Installation

### 1. Clone the repository

git clone https://github.com/Shru4241/github-mcp-server.git

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_personal_access_token
```

Replace `your_github_personal_access_token` with your own GitHub Personal Access Token.

**Never share your GitHub token or commit the `.env` file to GitHub.**

## Running the Server

Activate the virtual environment and run:

```powershell
python server.py
```

The MCP server uses STDIO communication and waits for an MCP client to connect.

## MCP Inspector

You can test the server using MCP Inspector.

Use:

```powershell
npx @modelcontextprotocol/inspector@latest
```

Then configure the server with:

**Command:**

```text
C:\path\to\github-mcp-server\venv\Scripts\python.exe
```

**Arguments:**

```text
C:\path\to\github-mcp-server\server.py
```

**Working Directory:**

```text
C:\path\to\github-mcp-server
```

## Available Tools

| Tool | Description |
|---|---|
| `get_repo_info` | Get repository information |
| `list_repositories` | List repositories for a user |
| `get_repo_issues` | Get open issues |
| `create_issue` | Create a new issue |
| `create_repository` | Create a GitHub repository |
| `search_repositories` | Search GitHub repositories |
| `add_issue_comment` | Add a comment to an issue |
| `close_issue` | Close an issue |
| `get_repo_files` | List repository files and folders |
| `read_repo_file` | Read a repository file |
| `create_or_update_file` | Create or update a repository file |
| `create_branch` | Create a new branch |
| `create_pull_request` | Create a pull request |
| `merge_pull_request` | Merge a pull request |
| `delete_repo_file` | Delete a repository file |

## Project Structure

```text
github-mcp-server/
│
├── server.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

> **Note:** `.env` contains your GitHub token and must not be uploaded to GitHub.

## Example Workflow

The server can perform a complete GitHub development workflow:

```text
Create Branch
      ↓
Create / Update File
      ↓
Commit Changes
      ↓
Create Pull Request
      ↓
Merge Pull Request
```

## Author

Created as a Python-based GitHub MCP Server project.