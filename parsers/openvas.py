# parsers/openvas.py
import xml.etree.ElementTree as ET

def parse_openvas(uploaded_file):
    findings = []
    try:
        file_bytes = uploaded_file.getvalue()
        if not file_bytes:
            return findings

        root = ET.fromstring(file_bytes)
        results = root.findall('.//result') or root.findall('.//results/result')
        if not results:
            return findings

        for result in results:
            # === TITLU COMPLET (NVT name + OID) ===
            name_elem = result.find('name')
            title = "Unknown Vulnerability"
            if name_elem is not None and name_elem.text:
                title = name_elem.text.strip()
            
            nvt_elem = result.find('.//nvt')
            oid = nvt_elem.get('oid', '') if nvt_elem is not None else ''
            if oid:
                title = f"{title} (OID: {oid})"

            # === HOST ===
            host_elem = result.find('host')
            host = host_elem.text.strip() if host_elem is not None and host_elem.text else "Unknown"

            # === SEVERITY ===
            severity = "Informational"
            cvss = 0.0
            sev_elem = result.find('.//severity')
            if sev_elem is not None and sev_elem.text:
                try:
                    cvss = float(sev_elem.text.strip())
                    if cvss >= 9.0: severity = "Critical"
                    elif cvss >= 7.0: severity = "High"
                    elif cvss >= 4.0: severity = "Moderate"
                    elif cvss > 0.0: severity = "Low"
                except:
                    pass

            # === DESCRIERE + DETALII ===
            desc_elem = result.find('description')
            description = desc_elem.text.strip()[:1500] if desc_elem is not None and desc_elem.text else ""

            # === RECOMANDARE ===
            sol_elem = result.find('.//solution')
            remediation = sol_elem.text.strip()[:1000] if sol_elem is not None and sol_elem.text else ""

            # === REFERINȚE (CVE, BID, etc.) ===
            references = []
            for ref in result.findall('.//ref'):
                ref_type = ref.get('type', '').upper()
                ref_id = ref.get('id', '')
                if ref_type and ref_id:
                    references.append(f"{ref_type}: {ref_id}")

            findings.append({
                "id": f"OPENVAS-{len(findings)+1:03d}",
                "title": title,
                "host": host,
                "severity": severity,
                "cvss": cvss,
                "description": description,
                "remediation": remediation,
                "code": "",  # OpenVAS nu are cod
                "images": [],
                "references": references
            })

        return findings

    except Exception as e:
        print(f"[OpenVAS Parser] Eroare: {e}")
        return []
