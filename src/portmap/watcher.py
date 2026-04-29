"""Watch mode for portmap."""

import time
from typing import Callable, Optional

from .core import PortInfo, get_listening_ports


class PortWatcher:
    """Watch for port changes over time."""

    def __init__(
        self,
        interval: float = 2.0,
        on_change: Optional[Callable[[list[PortInfo], list[PortInfo]], None]] = None,
    ):
        """
        Initialize the watcher.

        Args:
            interval: Seconds between checks.
            on_change: Callback when ports change (added, removed).
        """
        self.interval = interval
        self.on_change = on_change
        self._previous_ports: set[int] = set()

    def watch(self, duration: Optional[float] = None) -> None:
        """
        Start watching for port changes.

        Args:
            duration: Optional duration in seconds (None = forever).
        """
        start_time = time.time()

        while True:
            current_ports = get_listening_ports()
            current_port_nums = {p.port for p in current_ports}

            if self._previous_ports:
                added = current_port_nums - self._previous_ports
                removed = self._previous_ports - current_port_nums

                if added or removed:
                    if self.on_change:
                        added_info = [p for p in current_ports if p.port in added]
                        removed_info = [
                            PortInfo(
                                port=p,
                                protocol="",
                                pid=None,
                                process_name=None,
                                command_line=None,
                            )
                            for p in removed
                        ]
                        self.on_change(added_info, removed_info)

            self._previous_ports = current_port_nums

            if duration and (time.time() - start_time) >= duration:
                break

            time.sleep(self.interval)