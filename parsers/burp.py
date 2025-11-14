# parsers/burp.py
import xml.etree.ElementTree as ET
import re

def parse_burp(xml_file):
    """
    Parsează Burp Suite Professional XML export
    Returnează findings cu severity: Critical, High, Moderate, Low, Informational
    """
    findings = []
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Burp: <issues><issue>...
        for issue in root.findall('issue'):
            finding = {
                "id": f"BURP-{issue.find('serialNumber').text}" if issue.find('serialNumber') is not None else f"BURP-{len(findings)+1:03d}",
                "title": issue.find('name').text.strip() if issue.find('name') is not None else "Burp Issue",
                "host": issue.find('host').text.strip() if issue.find('host') is not None else "Unknown",
                "severity": "Informational",
                "description": "",
                "impact": "",
                "remediation": "",
                "references": [],
                "cvss": 0.0
            }

            # === SEVERITY ===
            sev_elem = issue.find('severity')
            if sev_elem is not None and sev_elem.text:
                sev = sev_elem.text.strip().lower()
                sev_map = {
                    "high": "High",
                    "medium": "Moderate",
                    "low": "Low",
                    "information": "Informational",
                    "informational": "Informational"
                }
                finding["severity"] = sev_map.get(sev, "Informational")

            # === DESCRIERE ===
            desc = issue.find('issueBackground') or issue.find('issueDetail')
            if desc is not None and desc.text:
                finding["description"] = re.sub(r'<.*?>', '', desc.text).strip()[:1000]

            # === IMPACT ===
            impact = issue.find('remediationBackground') or issue.find('remediationDetail')
            if impact is not None and impact.text:
                finding["impact"] = re.sub(r'<.*?>', '', impact.text).strip()[:800]

            # === RECOMANDARE ===
            rem = issue.find('remediationBackground')
            if rem is not None and rem.text:
                finding["remediation"] = re.sub(r'<.*?>', '', rem.text).strip()[:800]

            # === REFERINȚE (CWE, CVE) ===
            refs = issue.find('references')
            if refs is not None:
                for ref in refs.findall('reference'):
                    ref_text = ref.text.strip() if ref.text else ""
                    if ref_text:
                        finding["references"].append(ref_text)

            findings.append(finding)

        return findings

    except Exception as e:
        print(f"[Burp Parser] Eroare: {e}")
        return []
