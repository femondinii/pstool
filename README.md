# PSTool

Pentest Socket Toolkit: a Python command line tool for TCP/UDP port scanning and SSH connections, built as a hands-on project to practice network programming and offensive security fundamentals.

![Python](https://img.shields.io/badge/python-3.x-blue)
![Status](https://img.shields.io/badge/status-educational-yellow)

## About

PSTool was built to apply core networking and pentesting concepts in Python, including socket programming, TCP and UDP scanning, and SSH client communication. It is an educational project intended for learning and practice, not a production security tool.

## Legal Notice

This tool is intended for educational purposes only. Scanning or accessing systems without explicit authorization is illegal in most jurisdictions. Use PSTool only on systems you own or have explicit permission to test, such as personal lab environments or authorized CTF platforms. The author assumes no responsibility for misuse of this tool.

## Features

- TCP port scanning (single port or port range)
- UDP port scanning (single port or port range)
- Interactive SSH client
- Formatted CLI output using tables and color
- Scan summary with elapsed time and results count

## Tech Stack

- Python 3
- paramiko (SSH protocol implementation)
- rich (terminal output formatting)
- argparse (CLI argument parsing)

## Installation

Requirements: Python 3.8 or higher.

```bash
git clone https://github.com/femondinii/pstool.git
cd pstool

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -e .
```

This installs the `pstool` command in your virtual environment.

## Usage

Check version:

```bash
pstool --version
```

TCP scan (single port or range):

```bash
pstool tcp 192.168.1.1 --port 80
pstool tcp 192.168.1.1 --ports 8000-8100
```

UDP scan (single port or range):

```bash
pstool udp 192.168.1.1 --port 53
pstool udp 192.168.1.1 --ports 8000-8100
```

Note: use either `--port` or `--ports`, not both.

SSH client:

```bash
pstool ssh 192.168.1.1 -u username -p password
```

This opens an interactive shell where you can run remote commands. Type `exit` or `quit` to close the session.

### Example output

```
PSTool 1.0.0
Pentest Socket Toolkit

Target: 192.168.1.1
Protocol: TCP
Ports: 8000-8100

                Scan Results
+-------------+--------+---------+
| PORT        | STATE  | SERVICE |
+-------------+--------+---------+
| 8080/tcp    | open   | http    |
+-------------+--------+---------+

2 open port(s) found
101 port(s) scanned
Scan completed in 1.85 seconds
```

## Project Structure

```
pstool/
├── main.py           # Entry point and CLI (argparse)
├── scanner/           # Scanning logic (TCP, UDP, SSH)
├── models/             # Data models
├── utils/               # Utility functions
├── pyproject.toml       # Project configuration and dependencies
└── README.md
```

## Roadmap

- Export results to JSON or CSV
- More detailed service and banner detection
- Support for multiple targets in a single scan
- Automated tests
- Standalone executable packaging

## Author

Developed by [femondinii](https://github.com/femondinii) as a study project in Python, networking, and penetration testing.
