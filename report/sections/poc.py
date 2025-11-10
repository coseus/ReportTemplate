# report/sections/poc.py
from reportlab.platypus import Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import base64
import io

def add_poc(pdf, pocs=None):
    pocs = pocs or []
    if not pocs:
        return

    pdf.story.append(Paragraph("Proof of Concept", pdf.styles['Heading1']))
    pdf.story.append(Spacer(1, 0.6 * inch))

    for idx, poc in enumerate(pocs, 1):
        title = poc.get("title", "Untitled PoC")
        pdf.story.append(Paragraph(f"PoC {idx}: {title}", pdf.styles['Heading2']))
        pdf.story.append(Spacer(1, 0.3 * inch))

        if poc.get("description"):
            pdf.story.append(Paragraph(poc["description"], pdf.styles['Normal']))
            pdf.story.append(Spacer(1, 0.4 * inch))

        if poc.get("code"):
            code_text = poc["code"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            pdf.story.append(Paragraph(f"<font name='Courier'>{code_text}</font>", pdf.styles['Code']))
            pdf.story.append(Spacer(1, 0.5 * inch))

        if poc.get("images"):
            image_flowables = []
            for img_b64 in poc["images"]:
                try:
                    img_data = base64.b64decode(img_b64.split(',', 1)[1])
                    img = Image(io.BytesIO(img_data), width=3 * inch, height=2 * inch)
                    image_flowables.append(img)
                except Exception:
                    image_flowables.append(Paragraph("[Image failed]", pdf.styles['Normal']))

            if image_flowables:
                rows = [image_flowables[i:i+2] for i in range(0, len(image_flowables), 2)]
                table = Table(rows, colWidths=[3.2 * inch, 3.2 * inch])
                table.setStyle(TableStyle([
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('LEFTPADDING', (0,0), (-1,-1), 10),
                    ('RIGHTPADDING', (0,0), (-1,-1), 10),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 15),
                ]))
                pdf.story.append(table)
                pdf.story.append(Spacer(1, 0.4 * inch))

        pdf.story.append(PageBreak())
