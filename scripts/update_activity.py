import os
import sys
import json
import urllib.request
import re

GITHUB_USERNAME = "KingDarBoja"
MAX_ITEMS = 6

def get_recent_activity():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    headers = {
        "User-Agent": f"Activity-Updater-{GITHUB_USERNAME}",
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"
    
    # 1. Fetch public events from GitHub REST API
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/events/public?per_page=100"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            events = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error fetching GitHub events: {e}")
        return []

    contributions = []
    seen = set()

    for event in events:
        event_type = event.get("type")
        repo_name = event.get("repo", {}).get("name", "")
        repo_url = f"https://github.com/{repo_name}"
        created_at = event.get("created_at", "")[:10]

        # Ignore activities in own profile repo
        if repo_name.lower() == f"{GITHUB_USERNAME}/{GITHUB_USERNAME}".lower():
            continue

        item = None
        if event_type == "PullRequestEvent":
            action = event.get("payload", {}).get("action")
            pr = event.get("payload", {}).get("pull_request", {})
            pr_title = pr.get("title", "Pull Request")
            pr_url = pr.get("html_url", repo_url)
            merged = pr.get("merged", False)
            icon = "🟣" if merged else "🟢"
            status = "Merged PR" if merged else f"{action.capitalize()} PR"
            key = f"PR-{pr_url}"
            if key not in seen:
                seen.add(key)
                item = f"- {icon} **{status}**: [{pr_title}]({pr_url}) in [`{repo_name}`]({repo_url}) <sub>`{created_at}`</sub>"

        elif event_type == "PushEvent":
            commits = event.get("payload", {}).get("commits", [])
            if commits:
                commit_msg = commits[0].get("message", "").split("\n")[0]
                commit_sha = commits[0].get("sha", "")[:7]
                commit_url = f"{repo_url}/commit/{commits[0].get('sha')}"
                key = f"Push-{repo_name}-{created_at}"
                if key not in seen:
                    seen.add(key)
                    item = f"- 🔨 **Pushed commit**: [{commit_msg}]({commit_url}) to [`{repo_name}`]({repo_url}) <sub>`{created_at}`</sub>"

        elif event_type == "IssuesEvent":
            action = event.get("payload", {}).get("action")
            issue = event.get("payload", {}).get("issue", {})
            issue_title = issue.get("title", "Issue")
            issue_url = issue.get("html_url", repo_url)
            key = f"Issue-{issue_url}"
            if key not in seen:
                seen.add(key)
                item = f"- ⚠️ **{action.capitalize()} Issue**: [{issue_title}]({issue_url}) in [`{repo_name}`]({repo_url}) <sub>`{created_at}`</sub>"

        elif event_type == "ReleaseEvent":
            release = event.get("payload", {}).get("release", {})
            release_name = release.get("name") or release.get("tag_name", "Release")
            release_url = release.get("html_url", repo_url)
            key = f"Release-{release_url}"
            if key not in seen:
                seen.add(key)
                item = f"- 🚀 **Published Release**: [{release_name}]({release_url}) in [`{repo_name}`]({repo_url}) <sub>`{created_at}`</sub>"

        if item:
            contributions.append(item)
            if len(contributions) >= MAX_ITEMS:
                break

    return contributions

def update_readme(activity_lines):
    readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- START_SECTION:activity -->"
    end_tag = "<!-- END_SECTION:activity -->"

    pattern = re.compile(f"{re.escape(start_tag)}.*?{re.escape(end_tag)}", re.DOTALL)
    
    if not activity_lines:
        activity_block = f"{start_tag}\n<!-- Recent activity will be populated by GitHub Actions -->\n*Contributions and pull requests across open source repositories will appear here.*\n{end_tag}"
    else:
        formatted_activity = "\n".join(activity_lines)
        activity_block = f"{start_tag}\n{formatted_activity}\n{end_tag}"

    if pattern.search(content):
        new_content = pattern.sub(activity_block, content)
    else:
        new_content = content + f"\n\n## 🔭 Recent Open Source Activity\n{activity_block}\n"

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README.md updated with recent activity.")

if __name__ == "__main__":
    activities = get_recent_activity()
    update_readme(activities)
