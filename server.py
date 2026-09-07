import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("GitHub MCP Server")


@mcp.tool()
def get_repo_info(repo: str) -> str:
    """Get basic information about a GitHub repository."""
    url = f"https://api.github.com/repos/{repo}"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return f"Repository not found: {repo}"

    data = response.json()

    return (
        f"Repository: {data['full_name']}\n"
        f"Description: {data['description']}\n"
        f"Stars: {data['stargazers_count']}\n"
        f"Forks: {data['forks_count']}\n"
        f"Language: {data['language']}\n"
        f"URL: {data['html_url']}"
    )


@mcp.tool()
def list_repositories(username: str) -> str:
    """List public GitHub repositories for a user."""
    url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return f"User not found: {username}"

    repositories = response.json()

    if not repositories:
        return "No public repositories found."

    result = []

    for repo in repositories:
        result.append(
            f"{repo['name']} - ⭐ {repo['stargazers_count']} - "
            f"{repo['html_url']}"
        )

    return "\n".join(result)


@mcp.tool()
def get_repo_issues(repo: str) -> str:
    """Get open issues from a GitHub repository."""
    url = f"https://api.github.com/repos/{repo}/issues"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return f"Repository not found: {repo}"

    issues = response.json()

    if not issues:
        return "No open issues found."

    result = []

    for issue in issues:
        result.append(
            f"#{issue['number']} - {issue['title']}\n"
            f"URL: {issue['html_url']}\n"
            f"User: {issue['user']['login']}"
        )

    return "\n\n".join(result)


@mcp.tool()
def create_issue(repo: str, title: str, body: str) -> str:
    """Create a new issue in a GitHub repository."""
    url = f"https://api.github.com/repos/{repo}/issues"

    data = {
        "title": title,
        "body": body
    }

    response = requests.post(
        url,
        headers=HEADERS,
        json=data
    )

    if response.status_code != 201:
        return f"Failed to create issue: {response.text}"

    issue = response.json()

    return (
        f"Issue created successfully!\n"
        f"Number: #{issue['number']}\n"
        f"Title: {issue['title']}\n"
        f"URL: {issue['html_url']}"
    )

@mcp.tool()
def create_repository(name: str, description: str, private: bool = False) -> str:
    """Create a new GitHub repository."""
    url = "https://api.github.com/user/repos"

    data = {
        "name": name,
        "description": description,
        "private": private
    }

    response = requests.post(
        url,
        headers=HEADERS,
        json=data
    )

    if response.status_code != 201:
        return f"Failed to create repository: {response.text}"

    repo = response.json()

    return (
        f"Repository created successfully!\n"
        f"Name: {repo['full_name']}\n"
        f"Private: {repo['private']}\n"
        f"URL: {repo['html_url']}"
    )

@mcp.tool()
def search_repositories(query: str) -> str:
    """Search GitHub repositories."""
    url = "https://api.github.com/search/repositories"

    params = {
        "q": query,
        "per_page": 10
    }

    response = requests.get(
        url,
        headers=HEADERS,
        params=params
    )

    if response.status_code != 200:
        return f"Search failed: {response.text}"

    data = response.json()

    if data["total_count"] == 0:
        return "No repositories found."

    result = []

    for repo in data["items"]:
        result.append(
            f"{repo['full_name']} - ⭐ {repo['stargazers_count']}\n"
            f"Description: {repo['description']}\n"
            f"Language: {repo['language']}\n"
            f"URL: {repo['html_url']}"
        )

    return "\n\n".join(result)

@mcp.tool()
def add_issue_comment(repo: str, issue_number: int, comment: str) -> str:
    """Add a comment to a GitHub issue."""
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"

    data = {
        "body": comment
    }

    response = requests.post(
        url,
        headers=HEADERS,
        json=data
    )

    if response.status_code != 201:
        return f"Failed to add comment: {response.text}"

    result = response.json()

    return (
        f"Comment added successfully!\n"
        f"Issue: #{issue_number}\n"
        f"Comment URL: {result['html_url']}"
    )

@mcp.tool()
def close_issue(repo: str, issue_number: int) -> str:
    """Close a GitHub issue."""
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"

    data = {
        "state": "closed"
    }

    response = requests.patch(
        url,
        headers=HEADERS,
        json=data
    )

    if response.status_code != 200:
        return f"Failed to close issue: {response.text}"

    issue = response.json()

    return (
        f"Issue closed successfully!\n"
        f"Issue: #{issue['number']}\n"
        f"Title: {issue['title']}\n"
        f"URL: {issue['html_url']}"
    )

@mcp.tool()
def get_repo_files(repo: str, path: str = "") -> str:
    """Get files and folders from a GitHub repository."""
    url = f"https://api.github.com/repos/{repo}/contents/{path}"

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code != 200:
        return f"Failed to get repository files: {response.text}"

    items = response.json()

    # If the path points to a single file
    if isinstance(items, dict):
        return (
            f"Name: {items['name']}\n"
            f"Type: {items['type']}\n"
            f"Path: {items['path']}\n"
            f"URL: {items['html_url']}"
        )

    if not items:
        return "No files or folders found."

    result = []

    for item in items:
        result.append(
            f"{item['type'].upper()} - {item['path']}\n"
            f"URL: {item['html_url']}"
        )

    return "\n\n".join(result)


@mcp.tool()
def read_repo_file(repo: str, path: str) -> str:
    """Read the contents of a file from a GitHub repository."""
    url = f"https://api.github.com/repos/{repo}/contents/{path}"

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code != 200:
        return f"Failed to read file: {response.text}"

    data = response.json()

    if data.get("type") != "file":
        return "The specified path is not a file."

    import base64

    content = base64.b64decode(data["content"]).decode("utf-8")

    return (
        f"File: {data['path']}\n"
        f"Size: {data['size']} bytes\n"
        f"URL: {data['html_url']}\n\n"
        f"Content:\n{content}"
    )

@mcp.tool()
def create_or_update_file(
    repo: str,
    path: str,
    content: str,
    message: str,
    branch: str = "main"
) -> str:
    """Create a new file or update an existing file in a GitHub repository."""
    import base64

    url = f"https://api.github.com/repos/{repo}/contents/{path}"

    # Check if the file already exists
    get_response = requests.get(
        url,
        headers=HEADERS
    )

    data = {
    "message": message,
    "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
    "branch": branch
}

    # If the file exists, GitHub requires its current SHA
    if get_response.status_code == 200:
        existing_file = get_response.json()
        data["sha"] = existing_file["sha"]

    response = requests.put(
        url,
        headers=HEADERS,
        json=data
    )

    if response.status_code not in [200, 201]:
        return f"Failed to create or update file: {response.text}"

    result = response.json()

    action = "updated" if get_response.status_code == 200 else "created"

    return (
        f"File {action} successfully!\n"
        f"Path: {result['content']['path']}\n"
        f"Commit: {result['commit']['sha']}\n"
        f"URL: {result['content']['html_url']}"
    )

@mcp.tool()
def create_pull_request(
    repo: str,
    title: str,
    body: str,
    head: str,
    base: str = "main"
) -> str:
    """Create a pull request in a GitHub repository."""
    url = f"https://api.github.com/repos/{repo}/pulls"

    data = {
        "title": title,
        "body": body,
        "head": head,
        "base": base
    }

    response = requests.post(
        url,
        headers=HEADERS,
        json=data
    )

    if response.status_code != 201:
        return f"Failed to create pull request: {response.text}"

    pull_request = response.json()

    return (
        f"Pull request created successfully!\n"
        f"Number: #{pull_request['number']}\n"
        f"Title: {pull_request['title']}\n"
        f"URL: {pull_request['html_url']}"
    )

@mcp.tool()
def merge_pull_request(
    repo: str,
    pull_number: int,
    merge_method: str = "merge"
) -> str:
    """Merge a GitHub pull request."""
    url = f"https://api.github.com/repos/{repo}/pulls/{pull_number}/merge"

    data = {
        "merge_method": merge_method
    }

    response = requests.put(
        url,
        headers=HEADERS,
        json=data
    )

    if response.status_code != 200:
        return f"Failed to merge pull request: {response.text}"

    result = response.json()

    if result.get("merged"):
        return (
            f"Pull request merged successfully!\n"
            f"PR: #{pull_number}\n"
            f"Message: {result.get('message')}"
        )

    return (
        f"Pull request was not merged.\n"
        f"Message: {result.get('message')}"
    )

@mcp.tool()
def create_branch(repo: str, branch_name: str, from_branch: str = "main") -> str:
    """Create a new branch in a GitHub repository."""
    # Get the SHA of the source branch
    ref_url = f"https://api.github.com/repos/{repo}/git/ref/heads/{from_branch}"

    response = requests.get(
        ref_url,
        headers=HEADERS
    )

    if response.status_code != 200:
        return f"Failed to get source branch: {response.text}"

    source_sha = response.json()["object"]["sha"]

    # Create the new branch
    create_url = f"https://api.github.com/repos/{repo}/git/refs"

    data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": source_sha
    }

    response = requests.post(
        create_url,
        headers=HEADERS,
        json=data
    )

    if response.status_code != 201:
        return f"Failed to create branch: {response.text}"

    return (
        f"Branch created successfully!\n"
        f"Branch: {branch_name}\n"
        f"Based on: {from_branch}"
    )

@mcp.tool()
def delete_repo_file(
    repo: str,
    path: str,
    message: str,
    branch: str = "main"
) -> str:
    """Delete a file from a GitHub repository."""
    url = f"https://api.github.com/repos/{repo}/contents/{path}"

    response = requests.get(
        url,
        headers=HEADERS,
        params={"ref": branch}
    )

    if response.status_code != 200:
        return f"Failed to find file: {response.text}"

    file_data = response.json()

    data = {
        "message": message,
        "sha": file_data["sha"],
        "branch": branch
    }

    response = requests.delete(
        url,
        headers=HEADERS,
        json=data
    )

    if response.status_code != 200:
        return f"Failed to delete file: {response.text}"

    return (
        f"File deleted successfully!\n"
        f"Path: {path}\n"
        f"Branch: {branch}"
    )


if __name__ == "__main__":
    print("GitHub MCP Server started", file=sys.stderr, flush=True)
    mcp.run()