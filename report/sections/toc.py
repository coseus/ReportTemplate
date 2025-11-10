# report/sections/toc.py – DOAR ADAUGĂ ASTA SUS (după importuri)
def add_toc(pdf, findings=None, pocs=None, **kwargs):
    findings = findings or []
    pocs = pocs or []
    
    pdf.story.append(Paragraph("Table of Contents", pdf.styles['Heading1']))
    pdf.story.append(Spacer(1, 0.5 * inch))

    data = [["Page", "Section"]]

    # === SECȚIUNI FIXE ===
    fixed = [
        "1 Cover Page",
        "2 Table of Contents",
        "3 Legal Disclaimer & Contact",
        "4 Assessment Overview",
        "4 Scope of Testing",
        "4 Severity Ratings",
        "5 Executive Summary",
        "6 Technical Findings",
        "7 Proof of Concept"   # ← ACUM APARE ÎN TOC!
    ]
    for sec in fixed:
        page, text = sec.split(" ", 1)
        data.append([Paragraph(page, pdf.styles['Normal']), Paragraph(text, pdf.styles['Normal'])])

    # === 6.1, 6.2... Findings ===
    order = {"Critical": 0, "High": 1, "Moderate": 2, "Low": 3, "Informational": 4}
    sorted_findings = sorted(findings, key=lambda f: order.get(f.get("severity", ""), 5))
    for i, f in enumerate(sorted_findings, 1):
        fid = f.get("id", "VULN")
        title = f.get("title", "")
        short = title if len(title) <= 55 else title[:52] + "..."
        colored = f"<font color='#dc2626'>{fid}</font> - {short}"
        data.append(["", Paragraph(f"  6.{i} {colored}", pdf.styles['Normal'])])

    # === 7.1, 7.2... POC-urile tale ===
    for i, poc in enumerate(pocs, 1):
        title = poc.get("title", f"PoC {i}")
        short = title if len(title) <= 60 else title[:57] + "..."
        data.append(["", Paragraph(f"  7.{i} {short}", pdf.styles['Normal'])])

    # === TABEL TOC ===
    table = Table(data, colWidths=[0.9*inch, 5.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('FONTSIZE', (0,1), (-1,-1), 10.5),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    pdf.story.append(table)
    pdf.story.append(Spacer(1, 0.5*inch))
