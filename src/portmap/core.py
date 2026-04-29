"""Core port scanning functionality."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PortInfo:
    """Information about a listening port."""

    port: int
    protocol: str
    pid: Optional[int]
    process_name: Optional[str]
    command_line: Optional[str]

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export."""
        return {
            "port": self.port,
            "protocol": self.protocol,
            "pid": self.pid,
            "process_name": self.process_name,
            "command_line": self.command_line,
        }


def get_listening_ports() -> list[PortInfo]:
    """
    Get all listening ports with associated process information.

    Returns:
        List of PortInfo objects for all listening ports.
    """
    import psutil

    ports: list[PortInfo] = []

    for conn in psutil.net_connections(kind="inet"):
        if conn.status == "LISTEN":
            proc = None
            proc_name: Optional[str] = None
            cmd_line: Optional[str] = None

            if conn.pid:
                try:
                    proc = psutil.Process(conn.pid)
                    proc_name = proc.name()
                    try:
                        cmd_line = " ".join(proc.cmdline())
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        cmd_line = None
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    pass

            # Determine protocol
            proto = "tcp" if conn.type == 1 else "udp"

            ports.append(
                PortInfo(
                    port=conn.laddr.port if conn.laddr else 0,
                    protocol=proto,
                    pid=conn.pid,
                    process_name=proc_name,
                    command_line=cmd_line,
                )
            )

    # Sort by port number
    ports.sort(key=lambda x: x.port)
    return ports


def find_port(port: int) -> list[PortInfo]:
    """
    Find information about a specific port.

    Args:
        port: Port number to search for.

    Returns:
        List of PortInfo objects matching the port.
    """
    import psutil

    results: list[PortInfo] = []

    for conn in psutil.net_connections(kind="inet"):
        if conn.laddr and conn.laddr.port == port:
            proc = None
            proc_name: Optional[str] = None
            cmd_line: Optional[str] = None

            if conn.pid:
                try:
                    proc = psutil.Process(conn.pid)
                    proc_name = proc.name()
                    try:
                        cmd_line = " ".join(proc.cmdline())
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        cmd_line = None
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    pass

            proto = "tcp" if conn.type == 1 else "udp"

            results.append(
                PortInfo(
                    port=port,
                    protocol=proto,
                    pid=conn.pid,
                    process_name=proc_name,
                    command_line=cmd_line,
                )
            )

    return results