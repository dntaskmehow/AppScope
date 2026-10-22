from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table

console = Console()

class ScopeReporter:
    @staticmethod
    def print_report(audit_findings: List[Dict[str, Any]], scan_findings: List[Dict[str, Any]]):
        if audit_findings:
            table1 = Table(title="[bold cyan]GitHub Organization Repository Privilege Audit[/bold cyan]")
            table1.add_column("Repository", style="cyan")
            table1.add_column("Risk Level", style="yellow")
            table1.add_column("Details", style="white")

            for f in audit_findings:
                table1.add_row(f["repo"], f["risk"], f["details"])
            console.print(table1)

        if scan_findings:
            table2 = Table(title="[bold red]Local Credential Leakage Scan (.pem / Tokens)[/bold red]")
            table2.add_column("File Path", style="magenta")
            table2.add_column("Artifact Type", style="yellow")
            table2.add_column("Severity", style="bold red")

            for s in scan_findings:
                table2.add_row(s["file"], s["type"], s["severity"])
            console.print(table2)

        if not audit_findings and not scan_findings:
            console.print("[green]? No repository privilege anomalies or leaked private keys detected.[/green]")
