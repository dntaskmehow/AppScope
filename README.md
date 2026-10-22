

<div align="center">
  <img src="https://raw.githubusercontent.com/dntaskmehow/AppScope/main/assets/appscope-mark.svg" alt="AppScope" width="120" />
  <h1>AppScope</h1>
  <p><strong>GitHub App privilege audit and supply-chain credential leakage scanner</strong></p>

  <p>
    <a href="https://github.com/dntaskmehow/AppScope/actions"><img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" /></a>
    <a href="https://opensource.org/licenses/MIT"><img alt="MIT License" src="https://img.shields.io/badge/License-MIT-green.svg" /></a>
    <a href="https://github.com/dntaskmehow/AppScope"><img alt="GitHub App Security" src="https://img.shields.io/badge/Focus-GitHub%20App%20Security-0f172a?logo=github&logoColor=white" /></a>
    <a href="https://github.com/dntaskmehow/AppScope"><img alt="Language: Python" src="https://img.shields.io/badge/Language-Python-100%25-3776AB?logo=python&logoColor=white" /></a>
  </p>

  <p>
    <img alt="Stack" src="https://img.shields.io/badge/Stack-requests%20%7C%20pydantic%20%7C%20rich%20%7C%20PyJWT%20%7C%20cryptography-0f172a?logo=python&logoColor=white" />
  </p>
</div>

AppScope is a lightweight security audit tool for GitHub organizations and local repositories. It helps engineers answer two practical questions quickly:

- Which repositories grant elevated permissions that deserve review?
- Are private keys or exposed GitHub tokens sitting in a working tree or checked-in assets?

It is designed for GitHub maintainers, security reviewers, and developers who need a fast signal before a broader review begins.

## Why AppScope exists

Modern GitHub workflows frequently mix administrative access, automation, and local development environments. A repository can end up with:

- broad repository permissions granted to automation or app integrations,
- private keys accidentally committed to source control,
- leaked GitHub tokens embedded in config files, scripts, or generated artifacts.

AppScope makes those risks visible in a single, CLI-first workflow.

## At a glance

- Checks GitHub organization repositories for admin/push access exposure.
- Scans local directories for private keys and common GitHub token patterns.
- Produces readable terminal output using Rich tables.
- Runs as a Python CLI with minimal setup.
- Focuses on actionable findings rather than noisy output.

## Key capabilities

### GitHub organization audit

AppScope queries the GitHub API for a target organization and flags repositories that currently grant `admin` or `push` permissions. These are reported as higher-risk repositories that should be reviewed for least-privilege and lifecycle hygiene.

### Local credential scanning

The scanner walks a directory tree and inspects files for:

- PEM private key headers such as `-----BEGIN PRIVATE KEY-----`
- common GitHub token patterns, including `ghp_`, `github_pat_`, and `ghs_` token formats

Files matching these patterns are reported with severity levels and file paths.

### Clear reporting

Findings are printed to the terminal in compact tables so they are easy to triage during incident response or pre-merge review.

## How it works

```text
GitHub org -> repository permission audit -> findings
      |
      +-> local directory scan -> PEM / secret detection -> findings
                                      |
                                      +-> formatted CLI report
```

The tool is intentionally minimal: it inspects the target org via the GitHub REST API and scans the working directory for sensitive material without requiring a full platform or service deployment.

## Installation

From a local clone of the repository:

```bash
python -m pip install -e .
```

This installs the `appscope` CLI entry point defined in `pyproject.toml`.

## Quick start

```bash
appscope --org <your-org> --token <github-token> --path .
```

Example:

```bash
appscope --org acme-platform --token ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx --path .
```

If you are only auditing a local directory and do not have a token, you can still run the local scan path with an organization name:

```bash
appscope --org acme-platform --path .
```

## Usage

```bash
appscope --help
```

### Supported arguments

- `--org`: target GitHub organization to audit
- `--token`: optional GitHub token used for authenticated API requests
- `--path`: local directory to scan; defaults to the current directory

## What AppScope checks

The project currently focuses on the following items:

- repositories with high-privilege `admin` or `push` permissions,
- private key material stored in repository content,
- common GitHub token patterns embedded in local files.

This is a focused audit tool, not a general-purpose security platform.

## Technical details

AppScope is implemented in Python 3.10+ and uses:

- `requests` for GitHub API calls
- `pydantic` for configuration models
- `rich` for terminal reporting
- `PyJWT` and `cryptography` as dependencies for broader security tooling work

The scanner intentionally skips `.git` paths and reads files with UTF-8 fallback behavior to reduce noise when scanning local worktrees.

## Example output

```text
[*] Auditing organization acme-platform and scanning local files at ....

GitHub Organization Repository Privilege Audit
Repository     Risk Level                Details
-----------   -----------------------   -----------------------------------------------------------
internal-app   High Privilege Exposure   Repository grants push/admin permissions. Permissions: {...}

Local Credential Leakage Scan (.pem / Tokens)
File Path                 Artifact Type                                      Severity
----------------------   ------------------------------------------------  --------
.env                     Exposed GitHub Token / Installation Secret         HIGH
app.private-key.pem      GitHub App Private Key (.pem)                     CRITICAL
```

## Security and responsible use

AppScope is intended for authorized security auditing and internal review. Use it only against GitHub organizations, repositories, and directories you are explicitly permitted to assess.

Do not run it against third-party systems without consent, and avoid using it to exfiltrate credentials or access data outside the scope of a legitimate review.

## Contributing

Contributions are welcome. The project is intentionally compact, so the best improvements usually fit one of these areas:

- broader secret detection coverage,
- clearer reporting and output formatting,
- safer GitHub API permission checks,
- improved docs and examples.

To validate the current behavior locally:

```bash
PYTHONPATH=src python -m pytest -q
```

## License

This project declares MIT licensing in `pyproject.toml`.

## Project status

AppScope is a focused security audit utility for GitHub org and local repository hygiene. It is best understood as a practical scanning and review tool rather than a replacement for a full enterprise security suite.

---

<div align="center">
  <p><em>Designed for fast, actionable visibility into GitHub privilege exposure and credential leakage.</em></p>
</div>
