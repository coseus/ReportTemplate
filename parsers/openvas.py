# parsers/openvas.py
import xml.etree.ElementTree as ET

def parse_openvas(uploaded_file):
    """
    Primește un Streamlit UploadedFile
    Citește conținutul ca bytes → parsează cu fromstring
    """
    findings = []
    try:
        # 1. Citește tot conținutul ca bytes
        file_bytes = uploaded_file.getvalue()
        if not file_bytes:
            return findings

        # 2. Parsează direct din bytes
        root = ET.fromstring(file_bytes)

        # 3. Găsește toate rezultatele
        results = root.findall('.//result') or root.findall('.//results/result')
        if not results:
            return findings  # raport gol

        for result in results:
            finding = {
                "id": f"OPENVAS-{len(findings)+1:03d}",
                "title": "Unknown",
                "host": "Unknown",
                "severity": "Informational",
                "description": "",
                "remediation": "",
                "cvss": 0.0
            }

            # Titlu
            name_elem = result.find('name')
            if name_elem is not None and name_elem.text:
                finding["title"] = name_elem.text.strip()[:150]

            # Host
            host_elem = result.find('host')
            if host_elem is not None and host_elem.text:
                finding["host"] = host_elem.text.strip()

            # Severitate (CVSS)
            sev_elem = result.find('.//severity')
            if sev_elem is not None and sev_elem.text:
                try:
                    cvss = float(sev_elem.text.strip())
                    finding["cvss"] = cvss
                    if cvss >= 9.0: finding["severity"] = "Critical"
                    elif cvss >= 7.0: finding["severity"] = "High"
                    elif cvss >= 4.0: finding["severity"] = "Moderate"
                    elif cvss > 0.0: finding["severity"] = "Low"
                except:
                    pass

            # Descriere
            desc_elem = result.find('description')
            if desc_elem is not None and desc_elem.text:
                finding["description"] = desc_elem.text.strip()[:1000]

            # Recomandare
            sol_elem = result.find('.//solution')
            if sol_elem is not None and sol_elem.text:
                finding["remediation"] = sol_elem.text.strip()[:800]

            findings.append(finding)

        return findings

    except Exception as e:
        print(f"[OpenVAS Parser] Eroare: {e}")
        return []
