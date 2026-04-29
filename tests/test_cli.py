"""Tests for portmap.cli module."""

import pytest
from click.testing import CliRunner

from portmap.cli import main


class TestCLI:
    """Tests for CLI commands."""

    def test_main_help(self):
        """Test main help command."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "Portmap" in result.output

    def test_version_flag(self):
        """Test version flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])

        assert result.exit_code == 0


class TestListCommand:
    """Tests for list command."""

    def test_list_help(self):
        """Test list command help."""
        runner = CliRunner()
        result = runner.invoke(main, ["list", "--help"])

        assert result.exit_code == 0


class TestFindCommand:
    """Tests for find command."""

    def test_find_help(self):
        """Test find command help."""
        runner = CliRunner()
        result = runner.invoke(main, ["find", "--help"])

        assert result.exit_code == 0


class TestWatchCommand:
    """Tests for watch command."""

    def test_watch_help(self):
        """Test watch command help."""
        runner = CliRunner()
        result = runner.invoke(main, ["watch", "--help"])

        assert result.exit_code == 0


class TestExportCommand:
    """Tests for export command."""

    def test_export_help(self):
        """Test export command help."""
        runner = CliRunner()
        result = runner.invoke(main, ["export", "--help"])

        assert result.exit_code == 0