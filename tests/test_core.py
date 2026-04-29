"""Tests for portmap.core module."""

import pytest

from portmap.core import PortInfo


class TestPortInfo:
    """Tests for PortInfo dataclass."""

    def test_to_dict(self):
        """Test conversion to dictionary."""
        port_info = PortInfo(
            port=8080,
            protocol="tcp",
            pid=1234,
            process_name="python",
            command_line="python -m http.server 8080",
        )
        result = port_info.to_dict()

        assert result["port"] == 8080
        assert result["protocol"] == "tcp"
        assert result["pid"] == 1234
        assert result["process_name"] == "python"
        assert result["command_line"] == "python -m http.server 8080"

    def test_to_dict_with_none_values(self):
        """Test conversion with None values."""
        port_info = PortInfo(
            port=443,
            protocol="tcp",
            pid=None,
            process_name=None,
            command_line=None,
        )
        result = port_info.to_dict()

        assert result["port"] == 443
        assert result["pid"] is None
        assert result["process_name"] is None

    def test_port_info_equality(self):
        """Test PortInfo equality."""
        p1 = PortInfo(80, "tcp", 100, "nginx", "/usr/sbin/nginx")
        p2 = PortInfo(80, "tcp", 100, "nginx", "/usr/sbin/nginx")
        assert p1 == p2