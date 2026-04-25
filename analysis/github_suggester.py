import requests

def suggest_repositories(project_type, language="python", page=1, per_page=10):
    """
    Suggest open-source repositories based on project type.
    
    Args:
        project_type: Type of project (e.g., "web", "ml", "api", "cli")
        language: Programming language filter
        page: Page number for pagination
        per_page: Results per page
    
    Returns:
        List of repository suggestions with name, description, and URL
    """
    suggestions = []
    
    # Map project types to search queries - simplified
    query_map = {
        "web": f"flask django fastapi language:{language}",
        "ml": f"machine-learning scikit-learn language:{language}",
        "api": f"rest-api fastapi flask language:{language}",
        "cli": f"cli command-line language:{language}",
        "game": f"pygame game language:{language}",
        "bot": f"discord-bot telegram-bot language:{language}",
        "data": f"pandas numpy data-science language:{language}"
    }
    
    query = query_map.get(project_type.lower(), f"language:{language}")
    
    # GitHub API search endpoint
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query + " stars:>50",
        "sort": "stars",
        "order": "desc",
        "page": page,
        "per_page": per_page
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "items" not in data or len(data["items"]) == 0:
            return []
        
        for repo in data.get("items", []):
            suggestions.append({
                "name": repo["full_name"],
                "description": repo["description"] or "No description available",
                "url": repo["html_url"],
                "stars": repo["stargazers_count"],
                "language": repo["language"] or "Unknown",
                "topics": repo.get("topics", [])[:3]
            })
    
    except requests.RequestException as e:
        return [{"error": f"GitHub API error: {str(e)}"}]
    
    return suggestions


def get_good_first_issues(repo_name):
    """
    Get good first issues from a specific repository.
    
    Args:
        repo_name: Full repository name (e.g., "owner/repo")
    
    Returns:
        List of beginner-friendly issues
    """
    url = f"https://api.github.com/repos/{repo_name}/issues"
    params = {
        "labels": "good first issue",
        "state": "open",
        "per_page": 5
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        issues = response.json()
        
        return [{
            "title": issue["title"],
            "url": issue["html_url"],
            "labels": [label["name"] for label in issue["labels"]]
        } for issue in issues]
    
    except requests.RequestException:
        return []
