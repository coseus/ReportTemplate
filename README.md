# Pentest Report Generator

Modern, enterprise-grade reporting platform for penetration testing engagements, built with **Streamlit**, **ReportLab**, and **Python**.

Generate professional PDF and DOCX reports with automated parsing, advanced finding management, executive summaries, remediation tracking, walkthrough sections, charts, and branded corporate layouts.

---

# 🚀 Features

## 📥 Multi-Format Vulnerability Import

Automatically import findings from:

- Nessus (`.nessus` XML)
- OpenVAS / Greenbone XML
- Nmap XML
- CSV
- JSON

The parser automatically extracts:

- Severity
- CVSS score
- CVE references
- Affected hosts
- Descriptions
- Impact
- Recommendations

---

## 🧠 Advanced Findings Management

- Full finding editor
- Severity filtering
- Automatic renumbering (`6.1`, `6.2`, etc.)
- Evidence image support
- Base64 image handling
- Screenshot deduplication
- Code block formatting
- Rich text sections

---

## 📊 Executive & Technical Reporting

Generate complete enterprise-style reports including:

- Executive Summary
- Technical Findings
- Risk Overview
- Attack Path Documentation
- Vulnerability Statistics
- Host-based Summaries
- Remediation Roadmaps
- Detailed Walkthroughs
- Additional Reports Section

---

## 📄 Enterprise PDF & DOCX Export

### PDF Features

- Corporate cover pages
- Automatic Table of Contents
- Optional CONFIDENTIAL watermark
- Custom logo support
- Severity badges
- Per-host vulnerability heatmaps
- Modern formatting
- Section-based structure
- Charts and metrics

### DOCX Features

- Structured findings
- Corporate formatting
- Reusable templates
- Editable deliverables

---

# 🏗️ Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| PDF Engine | ReportLab |
| DOCX Export | python-docx |
| Data Processing | Pandas |
| XML Parsing | lxml |
| Charts | Plotly + Matplotlib |
| Templates | Jinja2 |
| Image Processing | Pillow |

---

# 📂 Project Structure

```bash
ReportTemplate-main/
│
├── app.py                         # Main Streamlit application
├── run.py                         # Runner script
├── launcher.py                    # Launcher helper
├── build_exe.py                   # Build executable utility
├── setup_paths.py                 # Runtime path configuration
│
├── data/
│   └── saved_report.json          # Persisted report state
│
├── report/
│   ├── data_model.py              # Report schema
│   ├── parsers.py                 # Nessus/OpenVAS/Nmap parsers
│   ├── numbering.py               # Findings numbering logic
│   ├── pdf_generator.py           # PDF generation engine
│   ├── docx_generator.py          # DOCX generator
│   ├── html_generator.py          # HTML rendering support
│   ├── utils.py                   # Shared helpers
│   └── sections/                  # Report section templates
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

After startup, open:

```text
http://localhost:8501
```

---

# 🧪 Supported Workflow

```text
Import Scan → Review Findings → Add Evidence → Generate PDF/DOCX
```

Typical workflow:

1. Import scanner output
2. Validate imported findings
3. Add screenshots and code snippets
4. Write executive summary
5. Configure branding and metadata
6. Generate final deliverables

---

# 📸 Screenshots

> Add screenshots here from the Streamlit UI and generated reports.

Example:

```md
![Dashboard](screenshots/dashboard.png)
![Findings](screenshots/findings.png)
![Generated PDF](screenshots/report.png)
```

---

# 🔒 Intended Use

This project is designed for:

- Penetration testers
- Red teams
- Security consultants
- Internal security teams
- Offensive security engagements
- Vulnerability assessment reporting

---

# 🛠️ Future Improvements

Potential roadmap ideas:

- Multi-user authentication
- Client portal
- Dark mode UI
- AI-assisted remediation generation
- CVSS auto-calculation
- Burp Suite import support
- Jira integration
- Markdown export
- Docker deployment
- Multi-language reporting

---

# 📦 Build Executable

The repository already includes:

```bash
build_exe.py
```

This can be extended to package the application into a standalone executable using:

- PyInstaller
- Nuitka
- cx_Freeze

---

# ⭐ Acknowledgements

Built using:

- Streamlit
- ReportLab
- Plotly
- Pandas
- Python ecosystem

---

# 💡 Notes

This project focuses on:

- Professional deliverables
- Corporate reporting standards
- Automation of repetitive reporting tasks
- Flexible extensibility
- Offensive security workflows
