"""Rich table formatting for portmap."""

from typing import Optional

from rich.console import Console
from rich.table import Table

from .core import PortInfo


def format_port_table(
    ports: list[PortInfo],
    console: Optional[Console] = None,
) -> Table:
    """
    Format port information as a Rich table.

    Args:
        ports: List of PortInfo objects.
        console: Rich Console instance.

    Returns:
        Rich Table ready for rendering.
    """
    table = Table(title="[bold cyan]Listening Ports[/bold cyan]")
    table.add_column("Port", style="bold green", justify="right")
    table.add_column("Protocol", style="dim")
    table.add_column("PID", justify="right")
    table.add_column("Process", style="yellow")
    table.add_column("Command", style="dim")

    for port_info in ports:
        pid_str = str(port_info.pid) if port_info.pid else "-"
        proc_str = port_info.process_name if port_info.process_name else "-"
        cmd_str = port_info.command_line if port_info.command_line else "-"
        # Truncate long command lines
        if len(cmd_str) > 50:
            cmd_str = cmd_str[:47] + "..."

        table.add_row(
            str(port_info.port),
            port_info.protocol.upper(),
            pid_str,
            proc_str,
            cmd_str,
        )

    return table


def format_json(ports: list[PortInfo]) -> str:
    """
    Format port information as JSON.

    Args:
        ports: List of PortInfo objects.

    Returns:
        JSON string.
    """
    import json

    return json.dumps(
        {"ports": [p.to_dict() for p in ports]},
        indent=2,
    )


def format_csv(ports: list[PortInfo]) -> str:
    """
    Format port information as CSV.

    Args:
        ports: List of PortInfo objects.

    Returns:
        CSV string.
    """
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Port", "Protocol", "PID", "Process", "Command"])

    for port_info in ports:
        writer.writerow([
            port_info.port,
            port_info.protocol,
            port_info.pid or "",
            port_info.process_name or "",
            port_info.command_line or "",
        ])

    return output.getvalue()