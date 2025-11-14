# parsers/openvas.py
import xml.etree.ElementTree as ET

def parse_openvas(xml_file):
    findings = []
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        results = root.findall('.//result') or root.findall('.//results/result')
        if not results:
            return findings

        for result in results:
            finding = {
                "id": f"OPENVAS-{len(findings)+1:03d}",
                "title": result.find('name').text.strip() if result.find('name') is not None else "Unknown",
                "host": result.find('host').text.strip() if result.find('host') is not None else "Unknown",
                "severity": "Informational",
                "description": "",
                "remediation": "",
                "cvss": 0.0
            }

            # SEVERITY
            sev_elem = result.find('.//severity')
            if sev_elem is not None and sev_elem.text:
                try:
                    cvss = float(sev_elem.text.strip())
                    finding["cvss"] = cvss
                    if cvss >= 9.0: finding["severity"] = "Critical"
                    elif cvss >= 7.0: finding["severity"] = "High"
                    elif cvss >= 4.0: finding["severity"] = "Moderate"
                    elif cvss > 0.0: finding["severity"] = "Low"
                except: pass

            desc = result.find('description')
            if desc is not None and desc.text:
                finding["description"] = desc.text.strip()

            sol = result.find('.//solution')
            if sol is not None and sol.text:
                finding["remediation"] = sol.text.strip()

            findings.append(finding)

        return findings
    except Exception as e:
        print(f"[OpenVAS] Eroare: {e}")
        return []
