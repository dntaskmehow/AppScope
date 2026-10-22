import os
import re
from pathlib import Path
from typing import List, Dict, Any

class CredentialScanner:
    PEM_PATTERN = re.compile(r'-----BEGIN RSA PRIVATE KEY-----|-----BEGIN PRIVATE KEY-----')
    SECRET_PATTERN = re.compile(r'(ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{82}|ghs_[a-zA-Z0-9]{36})')

    @staticmethod
    def scan_directory(directory: str) -> List[Dict[str, Any]]:
        findings = []
        root_path = Path(directory).resolve()

        for path in root_path.rglob("*"):
            if path.is_file() and ".git" not in path.parts:
                try:
                    content = path.read_text(encoding="utf-8", errors="ignore")
                    if CredentialScanner.PEM_PATTERN.search(content):
                        findings.append({
                            "file": str(path.relative_to(root_path)),
                            "type": "GitHub App Private Key (.pem)",
                            "severity": "CRITICAL"
                        })
                    if CredentialScanner.SECRET_PATTERN.search(content):
                        findings.append({
                            "file": str(path.relative_to(root_path)),
                            "type": "Exposed GitHub Token / Installation Secret",
                            "severity": "HIGH"
                        })
                except Exception:
                    continue

        return findings
