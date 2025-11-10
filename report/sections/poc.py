# report/sections/poc.py
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import streamlit as st

def add_poc(pdf, pocs):
    if not pocs:
        return

    pdf.story.append(Paragraph("Steps to Reproduce", pdf.styles['Heading1']))
    pdf.story.append(Spacer(1, 0.4*inch))

    for idx, poc in enumerate(pocs, 1):
        title = poc.get("title", f"PoC {idx+1}")
        code = poc.get("code", "")
        images = poc.get("images", [])

        # === TITLU POC ===
        pdf.story.append(Paragraph(f"{title}", pdf.styles['Heading2']))
        pdf.story.append(Spacer(1, 0.25*inch))

        # === CODE BLOCK – TERMINAL STYLE (EXACT CA FINDINGS) ===
        if code:
            terminal_style = ParagraphStyle(
                            name='Terminal',
                            parent=pdf.styles['Code'],
                            fontName='Courier',
                            fontSize=9,
                            leading=12
                        )
            code_text = poc["code"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            pdf.story.append(Paragraph(f"<font name='Courier'>{code_text}</font>", terminal_style))
            pdf.story.append(Spacer(1, 0.4*inch))

        # === IMAGINI POC ===
        if images:
            pdf.story.append(Paragraph("Screenshots", ParagraphStyle(
                'Label', fontName='DejaVu-Bold', fontSize=11, textColor=colors.HexColor("#2E4057")
            )))
            pdf.story.append(Spacer(1, 0.1*inch))

            img_data = []
            row = []
            for img_b64 in images:
                from reportlab.lib.utils import ImageReader
                import io, base64
                img_bytes = base64.b64decode(img_b64.split(',')[1])
                img = ImageReader(io.BytesIO(img_bytes))
                row.append(Image(img, width=3*inch, height=2*inch))
                if len(row) == 2:
                    img_data.append(row)
                    row = []
            if row:
                img_data.append(row)

            img_table = Table(img_data, colWidths=3.2*inch)
            img_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ]))
            pdf.story.append(img_table)
            pdf.story.append(Spacer(1, 0.2*inch))

        # === SPAȚIU MARE ÎNTRE POC-uri ===
        pdf.story.append(Spacer(1, 0.6*inch))
        pdf.story.append(Paragraph("<hr/>", pdf.styles['Normal']))
        pdf.story.append(Spacer(1, 0.6*inch))
