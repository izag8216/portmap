# portmap

<!-- Header SVG: assets/header.svg -->

<p align="center">
  <img src="assets/header.svg" alt="portmap" width="400"/>
</p>

<!-- Badges -->
<p align="center">

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![PyPI](https://img.shields.io/badge/pypi-v0.1.0-blue.svg)

</p>

---

**portmap** is a unified, cross-platform port and process viewer. No more remembering `lsof -i` vs `netstat -tlnp` vs `netstat -ano` -- one CLI works everywhere.

## Features

- **Cross-platform** -- Works on macOS, Linux, and Windows
- **Rich terminal output** -- Colorized tables with sortable columns
- **Watch mode** -- Monitor port changes in real-time with alerts
- **Structured export** -- JSON or CSV for scripting
- **No dependencies outside stdlib + psutil** -- Lightweight and fast

## Installation

### Via pip

```bash
pip install portmap
```

### Via Homebrew

```bash
brew install portmap
```

### Via source

```bash
git clone https://github.com/izag8216/portmap.git
cd portmap
pip install -e .
```

## Quick Start

### List all listening ports

```bash
portmap list
```

### Find a specific port

```bash
portmap find 8080
portmap find 3000 --verbose
```

### Watch for port changes

```bash
portmap watch --interval 2 --alert-on-change
```

### Export to JSON/CSV

```bash
portmap export --format json --output ports.json
portmap export --format csv --output ports.csv
```

## Usage

```
portmap list [--sort-by {port|pid|process}] [--protocol {tcp|udp|both}]
portmap find <PORT> [--verbose]
portmap watch [--interval SECONDS] [--alert-on-change]
portmap export [--format {json|csv}] [--output FILE]
```

## License

MIT License - see [LICENSE](LICENSE) for details.