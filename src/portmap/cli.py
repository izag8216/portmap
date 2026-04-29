"""Click CLI interface for portmap."""

import json
import sys
from typing import Optional

import click
from rich.console import Console

from . import __version__
from .core import PortInfo, find_port, get_listening_ports
from .formatters import format_csv, format_json, format_port_table
from .watcher import PortWatcher


console = Console()


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Portmap - Port and Process Viewer."""
    pass


@main.command()
@click.option(
    "--sort-by",
    type=click.Choice(["port", "pid", "process"]),
    default="port",
    help="Sort order",
)
@click.option(
    "--protocol",
    type=click.Choice(["tcp", "udp", "both"]),
    default="both",
    help="Protocol filter",
)
def list(sort_by: str, protocol: str) -> None:
    """List all listening ports."""
    ports = get_listening_ports()

    # Filter by protocol
    if protocol != "both":
        ports = [p for p in ports if p.protocol == protocol]

    # Sort
    if sort_by == "pid":
        ports.sort(key=lambda x: x.pid or 0)
    elif sort_by == "process":
        ports.sort(key=lambda x: x.process_name or "")

    # Display
    table = format_port_table(ports)
    console.print(table)
    console.print(f"\n[dim]{len(ports)} ports shown[/dim]")


@main.command()
@click.argument("port", type=int)
@click.option("--verbose", "-v", is_flag=True, help="Show full command line")
def find(port: int, verbose: bool) -> None:
    """Find details for a specific port."""
    results = find_port(port)

    if not results:
        console.print(f"[red]No process found listening on port {port}[/red]")
        sys.exit(1)

    table = format_port_table(results)
    console.print(table)

    if verbose:
        for info in results:
            if info.command_line:
                console.print(f"\n[bold]Full Command:[/bold]")
                console.print(f"  {info.command_line}")


@main.command()
@click.option(
    "--interval",
    type=float,
    default=2.0,
    help="Seconds between checks",
)
@click.option("--alert-on-change", is_flag=True, help="Alert when ports change")
def watch(interval: float, alert_on_change: bool) -> None:
    """Watch for port changes in real-time."""
    console.print(f"[cyan]Watching ports every {interval}s...[/cyan]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")

    def on_change(added: list[PortInfo], removed: list[PortInfo]) -> None:
        if added:
            ports_str = ", ".join(str(p.port) for p in added)
            console.print(f"[green]+ Opened: {ports_str}[/green]")
        if removed:
            ports_str = ", ".join(str(p.port) for p in removed)
            console.print(f"[red]- Closed: {ports_str}[/red]")

    watcher = PortWatcher(interval=interval, on_change=on_change if alert_on_change else None)

    try:
        watcher.watch()
    except KeyboardInterrupt:
        console.print("\n[dim]Stopped watching[/dim]")


@main.command()
@click.option("--format", "output_format", type=click.Choice(["json", "csv"]), default="json")
@click.option("--output", "-o", type=click.Path(), help="Output file (stdout if not specified)")
def export(output_format: str, output: Optional[str]) -> None:
    """Export port data to JSON or CSV."""
    ports = get_listening_ports()

    if output_format == "json":
        content = format_json(ports)
    else:
        content = format_csv(ports)

    if output:
        with open(output, "w") as f:
            f.write(content)
        console.print(f"[green]Exported to {output}[/green]")
    else:
        console.print(content)


if __name__ == "__main__":
    main()