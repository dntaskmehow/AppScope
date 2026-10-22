import requests
from typing import List, Dict, Any
from .config import ScopeConfig

class GitHubAuditor:
    def __init__(self, config: ScopeConfig):
        self.config = config
        self.session = requests.Session()
        if config.github_token:
            self.session.headers.update({
                "Authorization": f"Bearer {config.github_token}",
                "Accept": "vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            })

    def audit_organization(self) -> List[Dict[str, Any]]:
        findings = []
        url = f"https://api.github.com/orgs/{self.config.target_org}/repos"
        
        try:
            resp = self.session.get(url, timeout=self.config.timeout)
            if resp.status_code != 200:
                return [{"repo": "N/A", "risk": "API Error", "details": f"Failed to query org: HTTP {resp.status_code}"}]
            
            repos = resp.json()
            for repo in repos:
                name = repo.get("name")
                permissions = repo.get("permissions", {})
                if permissions.get("admin") or permissions.get("push"):
                    findings.append({
                        "repo": name,
                        "risk": "High Privilege Exposure",
                        "details": f"Repository grants push/admin permissions. Permissions: {permissions}"
                    })
        except Exception as e:
            findings.append({"repo": "Connection", "risk": "Exception", "details": str(e)})

        return findings
