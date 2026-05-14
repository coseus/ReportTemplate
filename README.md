# Pentest Report Generator

<p align="center">
  <img src="util/coseus_logo_slim.png" width="180">
</p>

<p align="center">
  <b>Enterprise-grade penetration testing reporting platform built with Python, Streamlit, and ReportLab.</b>
</p>

---

# 📌 Overview

Pentest Report Generator is a modern offensive security reporting platform designed to streamline the creation of professional penetration testing reports.

The platform automates the transformation of vulnerability scanner outputs into fully formatted PDF, DOCX, and HTML deliverables suitable for:

- Penetration testing engagements
- Vulnerability assessments
- Internal security reviews
- Red team operations
- Compliance assessments
- Executive reporting

The application combines:

- Automated vulnerability importing
- Structured finding management
- Rich evidence handling
- Executive dashboards
- Remediation roadmaps
- Detailed attack walkthroughs
- Enterprise-style PDF generation

into a single streamlined workflow.

---

# ✨ Features

## 📥 Multi-Format Vulnerability Import

Automatically import findings from:

- Nessus (`.nessus`)
- OpenVAS / Greenbone XML
- Nmap XML
- CSV
- JSON

The parser automatically extracts:

- Severity
- CVSS
- CVEs
- CWEs
- Affected hosts
- Services & ports
- Recommendations
- Descriptions
- References
- Evidence metadata

---

## 🧠 Advanced Findings Management

- Full manual finding editor
- Severity filtering
- Dynamic finding numbering
- CVSS integration
- Host-based grouping
- Evidence screenshots
- Base64 image support
- Code block formatting
- Rich text descriptions
- Risk categorization
- Technical + Executive reporting modes

---

## 📊 Executive Reporting

Generate executive-focused dashboards and summaries including:

- Severity distribution
- Risk overview
- Total findings metrics
- Risk trend visualization
- Executive summaries
- Critical asset visibility
- Host exposure overview

---

## 🛠️ Technical Reporting

Generate detailed technical deliverables containing:

- Full findings
- Evidence screenshots
- Attack walkthroughs
- Reproduction steps
- Code snippets
- Affected hosts
- Protocol information
- Remediation guidance
- References & CVEs

---

## 📄 Export Formats

Supported export formats:

- PDF
- DOCX
- HTML

---

# 🖼️ Application Screenshots

---

## 🏠 Dashboard / General Information

Main project configuration section containing:

- Client information
- Tester information
- Logo upload
- Executive summary
- Watermark settings

![Dashboard](screenshots/Dashboard.jpg)

---

## 📋 Scope & Assessment Details

Configure:

- Assessment overview
- Scope
- Scope exclusions
- Engagement details
- Client allowances

![Scope](screenshots/Scope.jpg)

---

## 🔎 Findings Management

Import scanner outputs and manage findings.

Features:

- Nessus/OpenVAS/Nmap importing
- Manual findings
- Severity filtering
- Dynamic finding management

![Findings](screenshots/Findings.jpg)

---

## 🧩 Additional Reports

Add custom technical appendices:

- Code snippets
- Output logs
- Custom screenshots
- Extra technical details

![Additional Reports](screenshots/Additional.jpg)

---

## 🧭 Detailed Walkthrough

Create attack-chain walkthroughs with:

- Screenshots
- Exploitation steps
- Code blocks
- Lateral movement evidence

![Detailed Walkthrough](screenshots/Detailed.jpg)

---

## 📈 Executive Summary

Executive reporting dashboard with:

- Severity charts
- Vulnerability metrics
- Risk summaries
- Custom executive text

![Executive Summary](screenshots/Executive.jpg)

---

## 🛡️ Remediation Roadmap

Structured remediation planning:

- Short-term actions
- Medium-term actions
- Long-term actions

![Remediation](screenshots/Remediation.jpg)

---

## 📤 Export System

Generate professional deliverables:

- PDF reports
- DOCX reports
- HTML reports
- Charts & analytics
- Watermark support

![Export 1](screenshots/Export1.jpg)

![Export 2](screenshots/Export2.jpg)

---

# 📑 Generated Report Examples

---

## 📘 Report Cover Page

Professional corporate-style cover page.

![Cover Page](screenshots/CoverReport.jpg)

---

## 📚 Automatic Table of Contents

Automatically generated TOC with section tracking.

![TOC](screenshots/TOCReport.jpg)

---

## 🚨 Vulnerability Findings

Structured vulnerability sections with:

- CVSS
- CWE
- Recommendations
- Impact
- Evidence

![Finding Example](screenshots/Finding1.jpg)

![Finding Example 2](screenshots/Finding2.jpg)

---

## 🖼️ Evidence Integration

Embedded screenshots and proof-of-concept evidence.

![Server EOL](screenshots/ServerEOL.jpg)

![Windows EOL](screenshots/WinEOL.jpg)

---

# 🏗️ Architecture

## Core Components

| Component | Description |
|---|---|
| Streamlit UI | Frontend interface |
| Report Engine | PDF/DOCX/HTML generation |
| Parser Engine | Scanner parsing |
| Data Model | Centralized report structure |
| Charting Module | Executive dashboards |
| Evidence Handler | Image processing |
| Export Pipeline | Final deliverables |

---

# 🧱 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Frontend |
| ReportLab | PDF generation |
| python-docx | DOCX generation |
| Pandas | Data processing |
| Plotly | Interactive charts |
| Matplotlib | Reporting charts |
| Pillow | Image handling |
| Jinja2 | Templates |
| lxml | XML parsing |

---

# 📂 Project Structure

```bash
ReportTemplate-main/
│
├── app.py
├── run.py
├── launcher.py
├── build_exe.py
├── setup_paths.py
│
├── data/
│   └── saved_report.json
│
├── report/
│   ├── data_model.py
│   ├── parsers.py
│   ├── numbering.py
│   ├── pdf_generator.py
│   ├── docx_generator.py
│   ├── html_generator.py
│   ├── utils.py
│   └── sections/
│
├── ui/
│   ├── general_info.py
│   ├── scope_tab.py
│   ├── findings_tab.py
│   ├── executive_summary_tab.py
│   ├── remediation_summary_tab.py
│   ├── detailed_walkthrough_tab.py
│   ├── additional_reports.py
│   ├── export_tab.py
│   └── reset.py
│
└── util/
    ├── charting.py
    ├── cvss_utils.py
    ├── helpers.py
    ├── json_utils.py
    ├── i18n.py
    ├── coseus.ico
    └── coseus_logo_slim.png
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/pentest-report-generator.git
cd pentest-report-generator
```

---

## 2. Create Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# 🧪 Typical Workflow

```text
Import Scan
    ↓
Review Findings
    ↓
Add Evidence
    ↓
Create Executive Summary
    ↓
Generate PDF/DOCX/HTML
```

---

# 🔐 Designed For

- Penetration testers
- Security consultants
- Internal security teams
- Red teams
- Vulnerability management teams
- Offensive security engagements

---

# 🚀 Future Improvements

Planned roadmap ideas:

- Multi-user authentication
- Role-based access
- Docker deployment
- Burp Suite parser
- Nessus API integration
- Jira integration
- AI-assisted remediation
- CVSS auto-scoring
- Multi-language reporting
- Dark/light themes
- Cloud deployment
- Client portals

---

# 📦 Build Standalone Executable

The repository already includes:

```bash
build_exe.py
```

Can be extended using:

- PyInstaller
- Nuitka
- cx_Freeze

---

# 🤝 Contributing

Contributions are welcome.

Potential areas:

- Parser integrations
- Report templates
- UI/UX improvements
- Export optimizations
- Performance enhancements
- Unit testing
- CI/CD pipelines

---

# 📜 License

Recommended licenses:

- MIT
- Apache 2.0
- GPLv3

Example:

```text
MIT License
```

---

# ⭐ Acknowledgements

Built using:

- Python
- Streamlit
- ReportLab
- Plotly
- Pandas
- Matplotlib
- Pillow
- Jinja2

---

# 💡 Notes

This project focuses on:

- Professional offensive security reporting
- Enterprise deliverables
- Automated reporting workflows
- Reusable templates
- Security consultant productivity
- Modern pentest reporting standards

The platform can be used both internally and in commercial consulting environments.
