# app.py (ULTRA-SAFE stable sync version)

from __future__ import annotations

import json
import os
import streamlit as st

import setup_paths

from ui.reset import render_global_reset_button
from ui.general_info import render_general_info
from ui.scope_tab import render_scope_tab
from ui.findings_tab import render_findings_tab
from ui.additional_reports import render_additional_reports
from ui.executive_summary_tab import render_executive_summary_tab
from ui.export_tab import render_export_tab
from ui.detailed_walkthrough_tab import render_detailed_walkthrough_tab
from ui.remediation_summary_tab import render_remediation_summary_tab

SAVE_FILE = "data/saved_report.json"


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="PenTest Report Generator",
    page_icon="util/coseus.ico",
    layout="wide",
)


# ---------------------------------------------------------
# DEFAULT REPORT STRUCTURE
# ---------------------------------------------------------
DEFAULT_REPORT_DATA = {
    "client": "",
    "project": "",
    "tester": "",
    "contact": "",
    "contacts": [],
    "date": "",
    "version": "1.0",
    "theme_hex": "#ED863D",
    "watermark_enabled": False,
    "logo_b64": "",
    "report_language": "en",
    "include_charts": True,
    "executive_summary": "",
    "assessment_overview": "",
    "assessment_details": "",
    "scope": "",
    "scope_exclusions": "",
    "client_allowances": "",
    "findings": [],
    "overall_risk": "Informational",
    "attack_path": [],
    "additional_reports": [],
    "detailed_walkthrough": [],
    "remediation_short": [],
    "remediation_medium": [],
    "remediation_long": [],
    "vuln_summary_counts": {},
    "vuln_summary_total": 0,
    "vuln_by_host": {},
    "sections": {},
    "section_1_0_confidentiality_and_legal": "",
    "section_1_1_confidentiality_statement": "",
    "section_1_2_disclaimer": "",
    "section_1_3_contact_information": "",
}


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def _merge_defaults(data: dict | None) -> dict:
    merged = DEFAULT_REPORT_DATA.copy()
    if isinstance(data, dict):
        merged.update(data)
    return merged


def load_saved_report() -> dict:
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return _merge_defaults(data)
        except Exception:
            return DEFAULT_REPORT_DATA.copy()
    return DEFAULT_REPORT_DATA.copy()


def save_report_data():
    try:
        os.makedirs("data", exist_ok=True)
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(
                st.session_state["report_data"],
                f,
                indent=2,
                ensure_ascii=False,
                default=str,
            )
    except Exception as e:
        st.error(f"Save failed: {e}")


def reset_all():
    st.session_state["report_data"] = DEFAULT_REPORT_DATA.copy()
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    st.success("All data cleared.")
    st.rerun()


def _safe_run_tab(render_func, report_data: dict) -> dict:
    """
    Runs a tab renderer safely.
    - If renderer returns a dict, use it.
    - If renderer returns None, keep existing report_data.
    - Always keep session_state synced.
    """
    try:
        result = render_func(report_data)
        if isinstance(result, dict):
            report_data = result
    except Exception as e:
        st.error(f"Tab error: {e}")
    st.session_state["report_data"] = report_data
    return report_data


# ---------------------------------------------------------
# INITIALIZE SESSION
# ---------------------------------------------------------
if "report_data" not in st.session_state or not isinstance(st.session_state["report_data"], dict):
    st.session_state["report_data"] = load_saved_report()
else:
    st.session_state["report_data"] = _merge_defaults(st.session_state["report_data"])


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    render_global_reset_button()


# ---------------------------------------------------------
# MAIN UI HEADER
# ---------------------------------------------------------
report_data = st.session_state["report_data"]

col_logo, col_titlu = st.columns([1, 4])

with col_logo:
    st.image("util/coseus_logo_slim.png", width=150)

with col_titlu:
    st.markdown(
        "<h3 style='margin: 12px 0 0 0;'>Pentest Report Generator</h3>",
        unsafe_allow_html=True,
    )

st.markdown("---")


# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    [
        "General Info",
        "Scope & Details",
        "Findings",
        "Additional Reports",
        "Detailed Walkthrough",
        "Executive Summary",
        "Remediation Summary",
        "Export",
    ]
)

with tab1:
    report_data = _safe_run_tab(render_general_info, report_data)

with tab2:
    report_data = _safe_run_tab(render_scope_tab, report_data)

with tab3:
    report_data = _safe_run_tab(render_findings_tab, report_data)

with tab4:
    report_data = _safe_run_tab(render_additional_reports, report_data)

with tab5:
    report_data = _safe_run_tab(render_detailed_walkthrough_tab, report_data)

with tab6:
    report_data = _safe_run_tab(render_executive_summary_tab, report_data)

with tab7:
    report_data = _safe_run_tab(render_remediation_summary_tab, report_data)

with tab8:
    report_data = _safe_run_tab(render_export_tab, report_data)


# ---------------------------------------------------------
# FINAL SAVE
# ---------------------------------------------------------
st.session_state["report_data"] = report_data
save_report_data()