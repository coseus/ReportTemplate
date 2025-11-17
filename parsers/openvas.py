# parsers/openvas.py
import xml.etree.ElementTree as ET

def parse_openvas(uploaded_file):
    findings = []
    try:
        file_bytes = uploaded_file.getvalue()
        if not file_bytes:
            return findings

        root = ET.fromstring(file_bytes)
        # Găsește toate <error> (în acest format, rezultatele sunt în <error>)
        errors = root.findall('.//error') or root.findall('.//results/error')
        if not errors:
            return findings

        for error in errors:
            finding = {
                "id": f"OPENVAS-{len(findings)+1:03d}",
                "title": "Unknown Vulnerability",
                "host": "Unknown",
                "severity": "Informational",
                "description": "",
                "remediation": "",
                "cvss": 0.0
            }

            # === HOST ===
            host_elem = error.find('host')
            if host_elem is not None and host_elem.text:
                finding["host"] = host_elem.text.strip()

            # === TITLU (din <nvt><name>) ===
            nvt_elem = error.find('.//nvt')
            if nvt_elem is not None:
                name_elem = nvt_elem.find('name')
                if name_elem is not None and name_elem.text:
                    finding["title"] = name_elem.text.strip()

                oid = nvt_elem.get('oid', '')
                if oid:
                    finding["title"] = f"{finding['title']} (OID: {oid})"

            # === DESCRIERE ===
            desc_elem = error.find('description')
            if desc_elem is not None and desc_elem.text:
                finding["description"] = desc_elem.text.strip()[:1000]

            # === REMEDIATION (din <nvt><solution>) ===
            sol_elem = nvt_elem.find('solution') if nvt_elem is not None else None
            if sol_elem is not None and sol_elem.text:
                finding["remediation"] = sol_elem.text.strip()[:800]

            # === SEVERITY + CVSS ===
            sev_elem = error.find('severity')
            if sev_elem is not None and sev_elem.text:
                try:
                    cvss = float(sev_elem.text.strip())
                    finding["cvss"] = cvss
                    if cvss >= 9.0:
                        finding["severity"] = "Critical"
                    elif cvss >= 7.0:
                        finding["severity"] = "High"
                    elif cvss >= 4.0:
                        finding["severity"] = "Moderate"
                    elif cvss > 0.0:
                        finding["severity"] = "Low"
                except:
                    pass

            # === CVSS_BASE (fallback) ===
            if finding["cvss"] == 0.0:
                cvss_base_elem = nvt_elem.find('cvss_base') if nvt_elem is not None else None
                if cvss_base_elem is not None and cvss_base_elem.text:
                    try:
                        cvss = float(cvss_base_elem.text.strip())
                        finding["cvss"] = cvss
                        if cvss >= 9.0:
                            finding["severity"] = "Critical"
                        elif cvss >= 7.0:
                            finding["severity"] = "High"
                        elif cvss >= 4.0:
                            finding["severity"] = "Moderate"
                        elif cvss > 0.0:
                            finding["severity"] = "Low"
                    except:
                        pass

            findings.append(finding)

        return findings
    except Exception as e:
        print(f"[OpenVAS Parser] Eroare: {e}")
        return []
