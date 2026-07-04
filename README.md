# Pattern of Life Analyzer (Browser Triage)

## Overview
The **Pattern of Life Analyzer** is an automated Digital Forensics and Incident Response (DFIR) script designed to extract and format web browsing history from live Windows machines. The tool dynamically locates, copies, and parses hidden SQLite databases across the Chromium ecosystem to generate court-ready CSV timelines.

## Forensic Value
During an investigation, establishing a user's "Pattern of Life" is critical for proving intent, discovering data exfiltration, or identifying the source of a malware infection. This tool allows investigators to bypass SQLite "database locked" errors by generating a live forensic copy of the artifacts before querying them.

**Supported Browsers:**
* Google Chrome
* Microsoft Edge
* Brave Browser

## Usage
1. Download the script to a forensic USB drive or local environment.
2. Execute the script natively in a Windows environment.
```bash
python chrome_triage.py
```
3. The script will automatically generate a timestamped `Forensic_Web_History_Report.csv` in the root directory.

## Example Output (CSV Format)

The extracted CSV report automatically maps the 1601 Webkit timestamps to human-readable formats and organizes the data for immediate ingest into SIEMs (like Splunk) or Excel.

| Browser | Timestamp | Visit Count | URL | Page Title |
| :--- | :--- | :--- | :--- | :--- |
| Google Chrome | 2026-01-21 12:34:04 | 2 | https://my.wgu.edu/ | WGU Student Portal |
| Microsoft Edge | 2026-01-20 09:15:22 | 1 | https://nmap.org/ | Nmap: the Network Mapper |

## Author
**Robert Turley (liton)** *Cybersecurity & DFIR Student*
