# main.py – VERSIUNE FINALĂ (RESET 100% FUNCȚIONAL)
import streamlit as st

# ================================================================
# 1. NU INIȚIALIZĂM NIMIC LA ÎNCEPUT (asta era problema!)
# ================================================================
# NU mai pune niciun "if 'xxx' not in st.session_state:" aici sus!

# ================================================================
# 2. IMPORTURI
# ================================================================
from components.general import render as general_tab
from components.scope import render as scope_tab
from components.findings import render as findings_tab
from components.executive import render as executive_tab
from components.poc import render as poc_tab
from components.export import render as export_tab
from components.legal import render as legal_tab
from components.severity import render as severity_tab

# ================================================================
# 3. CONFIG + TITLU
# ================================================================
st.set_page_config(page_title="Raport Pentest", layout="wide")
st.title("PENTEST REPORT GENERATOR")

# ================================================================
# 4. INIȚIALIZARE SIGURĂ – DOAR O DATĂ, DUPĂ CE ȘTIM CĂ NU S-A RESETAT
# ================================================================
def init_session():
    defaults = {
        "findings": [],
        "pocs": [],
        "poc_content": "",
        "overview": "",
        "confidentiality": "",
        "disclaimer": "",
        "severity_ratings": "",
        "contacts": [
            {"name": "Name", "role": "Lead Security Analyst", "email": "security@company.com", "type": "Tester"},
            {"name": "Company", "role": "Client Representative", "email": "client@company.com", "type": "Client"},
            {"name": "Support", "role": "Support Team", "email": "support@company.com", "type": "Support"}
        ]
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Apelez inițializarea doar dacă NU suntem în proces de reset
if not st.session_state.get("_do_full_reset", False):
    init_session()

# ================================================================
# 5. TABURI
# ================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "General Info", "Scope", "Findings", "Executive Summary",
    "PoC", "Export"
])

with tab1: general_tab()
with tab2: scope_tab()
with tab3: findings_tab()
with tab4: executive_tab()
with tab5: poc_tab()
with tab6: export_tab()
