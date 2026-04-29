"""Tests for portmap.formatters module."""

import json

from portmap.core import PortInfo
from portmap.formatters import format_csv, format_json, format_port_table


class TestFormatPortTable:
    """Tests for format_port_table function."""

    def test_creates_table_with_ports(self):
        """Test table creation with port data."""
        ports = [
            PortInfo(
                port=8080,
                protocol="tcp",
                pid=1234,
                process_name="python",
                command_line="python -m http.server",
            )
        ]
        table = format_port_table(ports)

        assert table is not None
        assert table.title == "[bold cyan]Listening Ports[/bold cyan]"

    def test_creates_table_with_empty_list(self):
        """Test table creation with no ports."""
        ports = []
        table = format_port_table(ports)

        assert table is not None


class TestFormatJson:
    """Tests for format_json function."""

    def test_json_output_structure(self):
        """Test JSON output has correct structure."""
        ports = [
            PortInfo(
                port=3000,
                protocol="tcp",
                pid=5678,
                process_name="node",
                command_line="node app.js",
            )
        ]
        result = format_json(ports)
        data = json.loads(result)

        assert "ports" in data
        assert len(data["ports"]) == 1
        assert data["ports"][0]["port"] == 3000
        assert data["ports"][0]["protocol"] == "tcp"

    def test_json_with_empty_list(self):
        """Test JSON with empty port list."""
        result = format_json([])
        data = json.loads(result)

        assert data["ports"] == []


class TestFormatCsv:
    """Tests for format_csv function."""

    def test_csv_has_header(self):
        """Test CSV includes header row."""
        ports = []
        result = format_csv(ports)

        assert "Port" in result
        assert "Protocol" in result
        assert "PID" in result

    def test_csv_with_data(self):
        """Test CSV includes data rows."""
        ports = [
            PortInfo(
                port=22,
                protocol="tcp",
                pid=100,
                process_name="sshd",
                command_line="/usr/sbin/sshd",
            )
        ]
        result = format_csv(ports)

        assert "22" in result
        assert "sshd" in result
        assert "tcp" in result