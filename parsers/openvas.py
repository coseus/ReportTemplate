# parsers/openvas.py
import xml.etree.ElementTree as ET
from datetime import datetime

def parse_openvas(xml_file):
    """
    Parsează fișierul OpenVAS .xml și returnează o listă de findings
    Compatibil cu OpenVAS 21+, GVM 22+
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        findings = []
        report = root.find('.//report')
        if not report:
            return findings  # raport gol

        # Informații generale
        host_list = []
        for host_elem in report.findall('.//host'):
            ip = host_elem.text.strip() if host_elem.text else "Unknown"
            host_list.append(ip)

        # Vulnerabilități
        for result in report.findall('.//result'):
            vuln = {
                "id": f"VULN-{len(findings)+1:03d}",
                "title": "OpenVAS Finding",
                "host": "Multiple",
                "severity": "Informational",
                "description": "",
                "impact": "",
                "recommendation": "",
                "references": [],
                "cvss": 0.0
            }

            # Nume vulnerabilitate
            name_elem = result.find('name')
            if name_elem is not None and name_elem.text:
                vuln["title"] = name_elem.text.strip()[:100]

            # Host
            host_elem = result.find('host')
            if host_elem is not None and host_elem.text:
                vuln["host"] = host_elem.text.strip()

            # Severitate (NVT → threat)
            threat_elem = result.find('.//threat')
            if threat_elem is not None and threat_elem.text:
                threat = threat_elem.text.strip().lower()
                if "high" in threat:
                    vuln["severity"] = "High"
                elif "medium" in threat:
                    vuln["severity"] = "Moderate"
                elif "low" in threat:
                    vuln["severity"] = "Low"

            # CVSS
            cvss_elem = result.find('.//nvt/cvss_base')
            if cvss_elem is not None and cvss_elem.text:
                try:
                    vuln["cvss"] = float(cvss_elem.text)
                    if vuln["cvss"] >= 9.0:
                        vuln["severity"] = "Critical"
                    elif vuln["cvss"] >= 7.0:
                        vuln["severity"] = "High"
                    elif vuln["cvss"] >= 4.0:
                        vuln["severity"] = "Moderate"
                    elif vuln["cvss"] >= 0.1:
                        vuln["severity"] = "Low"
                except:
                    pass

            # Descriere
            desc_elem = result.find('description')
            if desc_elem is not None and desc_elem.text:
                vuln["description"] = desc_elem.text.strip()

            # Impact
            impact_elem = result.find('.//nvt/impact')
            if impact_elem is not None and impact_elem.text:
                vuln["impact"] = impact_elem.text.strip()

            # Recomandare
            solution_elem = result.find('.//nvt/solution')
            if solution_elem is not None and solution_elem.text:
                vuln["recommendation"] = solution_elem.text.strip()

            # Referințe (CVE, BID, etc.)
            refs = []
            for ref in result.findall('.//nvt/ref'):
                ref_type = ref.get('type', '').upper()
                ref_id = ref.get('id', '')
                if ref_type and ref_id:
                    refs.append(f"{ref_type}: {ref_id}")
            if refs:
                vuln["references"] = refs

            findings.append(vuln)

        return findings

    except Exception as e:
        print(f"[OpenVAS Parser] Eroare: {e}")
        return []
