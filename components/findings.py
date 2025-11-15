# components/findings.py
import streamlit as st
import xml.etree.ElementTree as ET
import base64
from collections import Counter

def render():
    st.subheader("Technical Findings")

    # === INIȚIALIZARE FINDINGS ===
    if "findings" not in st.session_state:
        st.session_state.findings = []

    # === CONTOR LIVE ===
    total = len(st.session_state.findings)
    sev_count = Counter(f.get("severity", "Unknown") for f in st.session_state.findings)
    st.markdown(
        f"**Total Findings: {total}** | "
        f"Critical: {sev_count['Critical']} | "
        f"High: {sev_count['High']} | "
        f"Moderate: {sev_count['Moderate']} | "
        f"Low: {sev_count['Low']} | "
        f"Informational: {sev_count['Informational']}"
    )

    # === TABURI ===
    tab1, tab2 = st.tabs(["Add / Edit Manual", "Import Nessus / Nmap / OpenVAS / Burp"])

    # ===================================================================
    # TAB 1: ADD MANUAL + EDIT + DELETE
    # ===================================================================
    with tab1:
        with st.expander("Add New Finding", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                fid = st.text_input("ID", "VULN-001", key="add_id")
                title = st.text_input("Title", key="add_title")
                host = st.text_input("Host / IP", "192.168.1.10", key="add_host")
            with col2:
                severity = st.selectbox(
                    "Severity",
                    ["Critical", "High", "Moderate", "Low", "Informational"],
                    key="add_sev"
                )
                cvss = st.number_input("CVSS Score", 0.0, 10.0, 0.0, 0.1, key="add_cvss")

            description = st.text_area("Description", height=100, key="add_desc")
            remediation = st.text_area("Remediation", height=100, key="add_rem")
            code = st.text_area("Proof of Concept (Code)", height=120, key="add_code", placeholder="curl -X POST ...")

            uploaded_images = st.file_uploader(
                "Upload Screenshots (PNG/JPG)",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=True,
                key="add_images"
            )
            images_b64 = []
            for img in uploaded_images:
                img_bytes = img.read()
                b64 = base64.b64encode(img_bytes).decode()
                images_b64.append(f"data:{img.type};base64,{b64}")

            if st.button("Add Finding", type="primary"):
                st.session_state.findings.append({
                    "id": fid,
                    "title": title,
                    "host": host,
                    "severity": severity,
                    "cvss": cvss,
                    "description": description,
                    "remediation": remediation,
                    "code": code,
                    "images": images_b64
                })
                st.success("Finding added!")
                st.rerun()

        # === LISTĂ FINDINGS ===
# === LISTĂ FINDINGS (înlocuiește blocul cu asta) ===
        # === LISTĂ FINDINGS ===
            if st.session_state.findings:
                st.markdown("### Current Findings")
                for i, f in enumerate(st.session_state.findings):
                    # GENEREAZĂ CHEIE UNICĂ CU id(f) + i
                    unique_key = f"del_{id(f)}_{i}_{st.session_state.findings[i].get('id', '')}"
                    with st.expander(f"**{f['id']}** - {f['title']} | {f['host']} | {f['severity']}"):
                        col_del, col_edit = st.columns([1, 6])
                        with col_del:
                            if st.button("Delete", key=unique_key):
                                st.session_state.findings.pop(i)
                                st.rerun()
                        with col_edit:
                            st.caption("Click to expand for details")
            else:
                st.info("No findings yet.")

    # ===================================================================
    # TAB 2: IMPORT NESSUS / NMAP / OPENVAS / BURP
    # ===================================================================
    with tab2:
        st.subheader("Import Nessus / Nmap / OpenVAS / Burp")

        # === FILTRU SEVERITY UNIFICAT ===
        severity_options = ["Informational", "Low", "Moderate", "High", "Critical"]
        min_severity = st.selectbox(
            "Minimum Severity to Import",
            options=severity_options,
            index=2,
            key="import_min_severity"
        )
        severity_order = {"Critical": 4, "High": 3, "Moderate": 2, "Low": 1, "Informational": 0}
        min_level = severity_order.get(min_severity, 0)

        # === UPLOADER ===
        uploaded_file = st.file_uploader(
            "Încarcă raport (.nessus, .xml pentru Nmap/OpenVAS/Burp)",
            type=["nessus", "xml"],
            key="import_file"
        )

        if uploaded_file and st.button("Importă Raport", type="primary"):
            with st.spinner("Se procesează raportul..."):
                imported = 0
                current_findings = st.session_state.findings
                file_ext = uploaded_file.name.split(".")[-1].lower()

                try:
                    if file_ext == "nessus":
                        root = ET.parse(uploaded_file).getroot()
                        for report_item in root.findall(".//ReportItem"):
                            plugin_id = report_item.get("pluginID")
                            host_elem = report_item.find("../host") or report_item.find("host")
                            host = host_elem.text if host_elem is not None else "Unknown"
                            sev = int(report_item.get("severity", 0))

                            nessus_sev_map = {0: "Informational", 1: "Low", 2: "Moderate", 3: "High", 4: "Critical"}
                            severity = nessus_sev_map.get(sev, "Unknown")
                            if severity_order.get(severity, 0) < min_level:
                                continue

                            plugin_name = report_item.find("plugin_name")
                            plugin_name = plugin_name.text if plugin_name is not None else "Unknown"
                            desc = report_item.find("description")
                            sol = report_item.find("solution")
                            cvss_elem = report_item.find("cvss3_base_score")

                            new_finding = {
                                "id": f"NESSUS-{plugin_id}",
                                "title": plugin_name,
                                "host": host,
                                "severity": severity,
                                "cvss": float(cvss_elem.text) if cvss_elem is not None and cvss_elem.text else 0.0,
                                "description": (desc.text[:500] + "...") if desc is not None and desc.text else "",
                                "remediation": sol.text if sol is not None and sol.text else "",
                                "code": "",
                                "images": []
                            }
                            if not any(f["id"] == new_finding["id"] for f in current_findings):
                                current_findings.append(new_finding)
                                imported += 1

                    elif file_ext == "xml":
                        file_content = uploaded_file.read()
                        root = ET.fromstring(file_content)

                        # === DETECT BURP ===
                        if root.tag == "issues" or root.find(".//issue") is not None:
                            from parsers.burp import parse_burp
                            all_findings = parse_burp(uploaded_file)
                            for f in all_findings:
                                if severity_order.get(f.get("severity", "Informational"), 0) >= min_level:
                                    if not any(ex["title"] == f["title"] and ex["host"] == f["host"] for ex in current_findings):
                                        current_findings.append(f)
                                        imported += 1

                        # === DETECT OPENVAS ===
                        elif root.find(".//result") is not None or root.find(".//results/result") is not None:
                            from parsers.openvas import parse_openvas
                            all_findings = parse_openvas(uploaded_file)  # ACUM PRIMEȘTE FIȘIERUL CORECT
                            for f in all_findings:
                                sev = f.get("severity", "Informational")
                                if severity_order.get(sev, 0) >= min_level:
                                    if not any(ex["title"] == f["title"] and ex["host"] == f["host"] for ex in current_findings):
                                        current_findings.append(f)
                                        imported += 1

                        # === DETECT NMAP ===
                        elif root.find(".//host") is not None and root.find(".//port") is not None:
                            for host in root.findall(".//host"):
                                addr = host.find("address").get("addr")
                                for port in host.findall(".//port"):
                                    if port.find("state").get("state") == "open":
                                        portid = port.get("portid")
                                        service = port.find("service")
                                        svc_name = service.get("name", "unknown") if service is not None else "unknown"
                                        if severity_order["Informational"] >= min_level:
                                            new_finding = {
                                                "id": f"NMAP-{addr}:{portid}",
                                                "title": f"Open Port {portid} ({svc_name})",
                                                "host": addr,
                                                "severity": "Informational",
                                                "cvss": 0.0,
                                                "description": f"Port {portid} open on {addr}",
                                                "remediation": "Close if not required",
                                                "code": "",
                                                "images": []
                                            }
                                            if not any(f["id"] == new_finding["id"] for f in current_findings):
                                                current_findings.append(new_finding)
                                                imported += 1

                    # === FINALIZARE ===
                    st.session_state.findings = current_findings
                    if imported > 0:
                        st.success(f"Importate **{imported}** findings (≥ {min_severity})!")
                    else:
                        st.info(f"Nicio vulnerabilitate ≥ **{min_severity}** sau toate deja importate.")
                    st.rerun()

                except Exception as e:
                    st.error(f"Eroare la import: {e}")
                    st.code(str(e)[:1000])
