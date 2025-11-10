# main.py
import streamlit as st

# === OPRIRE DEBUG + WARNING-URI ===
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('deprecation.showImageFormat', False)
st.set_option('client.showErrorDetails', False)  # ascunde detalii erori

# === SILENȚIOZĂ COMPLETĂ (OPRIT DEBUG) ===
import logging
logging.getLogger("watchdog").setLevel(logging.WARNING)
logging.getLogger("streamlit").setLevel(logging.ERROR)

# ================================================================
# 1. NU INIȚIALIZĂM NIMIC LA ÎNCEPUT
# ================================================================
from components.general import render as general_tab
from components.scope import render as scope_tab
from components.findings import render as findings_tab
from components.executive import render as executive_tab
from components.poc import render as poc_tab
from components.export import render as export_tab

st.set_page_config(page_title="Raport Pentest", layout="wide")
st.title("PENTEST REPORT GENERATOR")

# ================================================================
# 2. INIȚIALIZARE DOAR DACĂ NU SUNTEM ÎN RESET
# ================================================================
def init_defaults():
    if "findings" not in st.session_state:
        st.session_state.findings = []
    if "pocs" not in st.session_state:
        st.session_state.pocs = []
    if "contacts" not in st.session_state:
        st.session_state.contacts = [
            {"name": "Name", "role": "Lead Security Analyst", "email": "security@company.com", "type": "Tester"},
            {"name": "Company", "role": "Client Representative", "email": "client@company.com", "type": "Client"},
            {"name": "Support", "role": "Support Team", "email": "support@company.com", "type": "Support"}
        ]

# APELEAZĂ INIȚIALIZAREA DOAR DACĂ NU SUNTEM ÎN PROCES DE RESET
if not st.session_state.get("performing_reset", False):
    init_defaults()

# ================================================================
# 3. TABURI
# ================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "General Info", "Scope", "Findings", "Executive Summary", "PoC", "Export"
])

with tab1: general_tab()
with tab2: scope_tab()
with tab3: findings_tab()
with tab4: executive_tab()
with tab5: poc_tab()
with tab6: export_tab()
