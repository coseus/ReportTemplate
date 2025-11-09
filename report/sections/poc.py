# report/sections/poc.py
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import streamlit as st

def add_poc(pdf, poc_list):
    if not poc_list:
        return

    pdf.story.append(Paragraph("Proof of Concept", pdf.styles['Heading1']))
    pdf.story.append(Spacer(1, 0.4*inch))

    for idx, poc in enumerate(poc_list):
        title = poc.get("title", f"PoC {idx+1}")
        code = poc.get("code", "")
        images = poc.get("images", [])

        # === TITLU POC ===
        pdf.story.append(Paragraph(f"{title}", pdf.styles['Heading2']))
        pdf.story.append(Spacer(1, 0.25*inch))

        # === CODE BLOCK – TERMINAL STYLE (EXACT CA FINDINGS) ===
        if code:
            pdf.story.append(Paragraph("Terminal", ParagraphStyle(
                'Label', fontName='DejaVu-Bold', fontSize=11, textColor=colors.HexColor("#2E4057")
            )))
            pdf.story.append(Spacer(1, 0.1*inch))

            # Fundal negru + text verde + bordură + colțuri rotunjite
            code_html = f"""
            <font name="DejaVu" size=9 color="#c9d1d9">
            {code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}
            </font>
            """
            code_para = Paragraph(code_html, pdf.styles['Code'])
            code_table = Table([[code_para]], colWidths=6.5*inch)
            code_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0d1117")),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#30363d")),
                ('ROUNDEDCORNERS', (0,0), (-1,-1), 6),
                ('LEFTPADDING', (0,0), (-1,-1), 15),
                ('RIGHTPADDING', (0,0), (-1,-1), 15),
                ('TOPPADDING', (0,0), (-1,-1), 12),
                ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ]))
            pdf.story.append(code_table)
            pdf.story.append(Spacer(1, 0.3*inch))

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
