# parsers/openvas.py
import xml.etree.ElementTree as ET

def parse_openvas(uploaded_file):
    findings = []
    try:
        root = ET.fromstring(uploaded_file.getvalue())

        # Găsește TOATE rezultatele reale (nu doar error!)
        results = root.findall('.//result') + root.findall('.//results/result')
        
        for result in results:
            # === HOST ===
            host_elem = result.find('host')
            host = host_elem.text.strip() if host_elem is not None and host_elem.text else "Unknown"

            # === TITLU + OID ===
            name_elem = result.find('name')
            title = name_elem.text.strip() if name_elem is not None and name_elem.text else "Unknown"
            nvt = result.find('nvt')
            oid = nvt.get('oid', '') if nvt is not None else ''
            if oid:
                title = f"{title} (OID: {oid})"

            # === SEVERITY DIN <severity> (valoare reală, nu -3) ===
            severity = "Informational"
            cvss = 0.0
            sev_elem = result.find('severity')
            if sev_elem is not None and sev_elem.text:
                try:
                    cvss_val = float(sev_elem.text.strip())
                    if cvss_val > 0:  # Ignoră -3, -1 etc.
                        cvss = cvss_val
                        if cvss >= 9.0: severity = "Critical"
                        elif cvss >= 7.0: severity = "High"
                        elif cvss >= 4.0: severity = "Moderate"
                        elif cvss > 0.0: severity = "Low"
                except:
                    pass

            # === FALLBACK: <nvt><cvss_base> (dacă severity e 0 sau negativ) ===
            if cvss == 0.0:
                cvss_base_elem = nvt.find('cvss_base') if nvt is not None else None
                if cvss_base_elem is not None and cvss_base_elem.text:
                    try:
                        cvss = float(cvss_base_elem.text.strip())
                        if cvss >= 9.0: severity = "Critical"
                        elif cvss >= 7.0: severity = "High"
                        elif cvss >= 4.0: severity = "Moderate"
                        elif cvss > 0.0: severity = "Low"
                    except:
                        pass

            # === DESCRIERE ===
            desc_elem = result.find('description')
            description = desc_elem.text.strip()[:1200] if desc_elem is not None and desc_elem.text else ""

            # === REMEDIATION ===
            sol_elem = nvt.find('solution') if nvt is not None else None
            remediation = sol_elem.text.strip()[:1000] if sol_elem is not None and sol_elem.text else "No specific solution provided."

            findings.append({
                "id": f"OPENVAS-{len(findings)+1:03d}",
                "title": title,
                "host": host,
                "severity": severity,
                "cvss": round(cvss, 1),
                "description": description,
                "remediation": remediation,
                "code": "",
                "images": [],
                "references": []
            })

        return findings

    except Exception as e:
        print(f"[OpenVAS Parser] Eroare: {e}")
        return []
