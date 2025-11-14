# parsers/openvas.py
import xml.etree.ElementTree as ET

def parse_openvas(xml_file):
    """
    Parsează OpenVAS/GVM .xml
    SEVERITY MAPATĂ EXACT CA LA NESSUS/NMAP
    """
    findings = []
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Găsește toate rezultatele (suportă ambele formate)
        results = root.findall('.//result') or root.findall('.//results/result')
        if not results:
            return findings  # fișier gol

        for result in results:
            finding = {
                "id": f"VULN-{len(findings)+1:03d}",
                "title": result.find('name').text.strip() if result.find('name') is not None else "Unknown",
                "host": result.find('host').text.strip() if result.find('host') is not None else "Unknown",
                "severity": "Informational",  # default
                "description": "",
                "impact": "",
                "recommendation": "",
                "references": [],
                "cvss": 0.0
            }

            # === SEVERITY FIXATĂ CA LA NESSUS/NMAP ===
            severity_elem = result.find('.//severity')
            if severity_elem is not None and severity_elem.text:
                try:
                    cvss = float(severity_elem.text.strip())
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

            # Descriere
            desc = result.find('description')
            if desc is not None and desc.text:
                finding["description"] = desc.text.strip()

            # Recomandare
            solution = result.find('.//solution')
            if solution is not None and solution.text:
                finding["recommendation"] = solution.text.strip()

            # Referințe
            for ref in result.findall('.//ref'):
                ref_type = ref.get('type', '').upper()
                ref_id = ref.get('id', '')
                if ref_type and ref_id:
                    finding["references"].append(f"{ref_type}: {ref_id}")

            findings.append(finding)

        return findings

    except Exception as e:
        print(f"[OpenVAS] Eroare parsare: {e}")
        return []
