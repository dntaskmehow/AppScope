import argparse
import sys
from .config import ScopeConfig
from .auditor import GitHubAuditor
from .scanner import CredentialScanner
from .reporter import ScopeReporter

def main():
    parser = argparse.ArgumentParser(description="AppScope: GitHub App & Repo Security Auditor.")
    parser.add_argument("--org", required=True, help="Target GitHub Organization.")
    parser.add_argument("--token", default=None, help="GitHub Personal Access Token.")
    parser.add_argument("--path", default=".", help="Local path to scan for leaked PEMs/secrets.")

    args = parser.parse_args()

    config = ScopeConfig(
        github_token=args.token,
        target_org=args.org,
        scan_path=args.path
    )

    try:
        print(f"[*] Auditing organization {config.target_org} and scanning local files at {config.scan_path}...")
        auditor = GitHubAuditor(config)
        audit_results = auditor.audit_organization()
        
        scanner = CredentialScanner()
        scan_results = scanner.scan_directory(config.scan_path)

        ScopeReporter.print_report(audit_results, scan_results)
    except Exception as e:
        print(f"[!] Execution Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
