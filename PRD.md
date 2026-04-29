# portmap -- Port and Process Viewer

## PRD v0.1.0

**Idea ID:** 100  
**Project Type:** CLI Tool  
**Tech Stack:** Python, psutil, click, rich  
**License:** MIT  

---

## Problem Statement

Diagnosing port conflicts and identifying which process occupies a specific port requires platform-specific commands with different syntax and output formats:
- macOS: `lsof -i`
- Linux: `netstat -tlnp` or `ss`
- Windows: `netstat -ano`

Developers waste time remembering platform-specific flags and parsing inconsistent output. No unified Python CLI exists that provides a consistent interface across platforms with modern features.

---

## Solution Overview

`portmap` provides a unified, cross-platform view of all listening ports and their associated processes using `psutil`. It displays port number, protocol, process name, PID, and command line in a formatted table. Supports filtering by port range or process name, JSON output for scripting, and a watch mode.

---

## Architecture

### Directory Structure

```
portmap/
├── src/
│   └── portmap/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py              # Click CLI interface
│       ├── core.py             # Core port scanning logic
│       ├── formatters.py      # Rich table formatting
│       └── watcher.py         # Watch mode implementation
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_formatters.py
│   └── test_cli.py
├── assets/
│   └── header.svg              # Original SVG header
├── pyproject.toml
├── README.md
├── LICENSE
└── THIRD_PARTY_LICENSES.md
```

### Technology Choices

| Library | Purpose | Rationale |
|---------|---------|-----------|
| `psutil` | Port/process enumeration | Cross-platform, well-maintained |
| `click` | CLI framework | Best Python CLI DX |
| `rich` | Terminal formatting | Beautiful tables, colors |

---

## Feature Specifications

### 1. `portmap list` -- List All Listening Ports

**Description:** Display all listening ports with associated process information.

**CLI Signature:**
```
portmap list [--all] [--sort-by {port|pid|process}] [--protocol {tcp|udp|both}]
```

**Output Columns:** Port, Protocol, Process Name, PID, Command Line

**Acceptance Criteria:**
- [ ] Shows all listening ports on the system
- [ ] Works on macOS, Linux, Windows
- [ ] Sort by port number (default), PID, or process name
- [ ] Filter by protocol (TCP/UDP/both)

---

### 2. `portmap find` -- Find Port Details

**Description:** Find detailed information about a specific port.

**CLI Signature:**
```
portmap find <PORT> [--verbose]
```

**Acceptance Criteria:**
- [ ] Shows process details for specific port
- [ ] Verbose mode shows full command line and working directory
- [ ] Clear error if port not found

---

### 3. `portmap watch` -- Watch Mode

**Description:** Monitor port changes in real-time.

**CLI Signature:**
```
portmap watch [--interval SECONDS] [--alert-on-change]
```

**Acceptance Criteria:**
- [ ] Refreshes port list at specified interval
- [ ] Highlights new/closed ports
- [ ] Optional alert on port state changes

---

### 4. `portmap export` -- Export to JSON

**Description:** Export port data for scripting.

**CLI Signature:**
```
portmap export [--format {json|csv}] [--output FILE]
```

**Acceptance Criteria:**
- [ ] JSON output with structured port/process data
- [ ] CSV output for spreadsheet import
- [ ] stdout output if no file specified

---

## Testing Strategy

| Type | Framework | Scope |
|------|-----------|-------|
| Unit | pytest | core.py functions, formatters |
| Integration | pytest | CLI commands with subprocess |
| Mock | unittest.mock | psutil responses |

---

## CI/CD Pipeline

GitHub Actions:
- Python lint (ruff)
- Python type check (mypy)
- Unit tests (pytest)
- Build verification

---

## Milestones

| Milestone | Scope | Effort |
|-----------|-------|--------|
| M1 | Project scaffold, core scanning, list command | M |
| M2 | Find command, rich formatting | S |
| M3 | Watch mode, export functionality | M |
| M4 | Tests, CI/CD, final polish | M |

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| psutil not available on some platforms | Test on macOS/Linux/Windows CI |
| Permission issues reading process info | Graceful degradation with warning |

---

## Out of Scope

- GUI interface
- Port killing/termination (use `kill` manually)
- DNS resolution (performance concern)

---

## Dependency License Audit

| Dependency | License | Compatible |
|------------|---------|------------|
| psutil | BSD | Yes (MIT-compatible) |
| click | BSD | Yes |
| rich | MIT | Yes |

No GPL/AGPL dependencies.