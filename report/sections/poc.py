# report/sections/poc.py
from reportlab.platypus import Paragraph, Spacer, PageBreak, Image, KeepInFrame
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import os
import io
from PIL import Image as PILImage

def add_poc(pdf, poc_list=None, **kwargs):
    if not poc_list:
        poc_list = []

    pdf.story.append(Paragraph("Proof of Concept & Steps to Reproduce", pdf.styles['Heading1']))
    pdf.story.append(Spacer(1, 0.2 * inch))

    if not poc_list:
        pdf.story.append(Paragraph("No PoC entries.", pdf.styles['Normal']))
        pdf.story.append(PageBreak())
        return

    for i, poc in enumerate(poc_list, 1):
        # === 7.1 Titlu ===
        pdf.story.append(Paragraph(f"7.{i} {poc.get('title', 'PoC')}", pdf.styles['Heading2']))
        pdf.story.append(Spacer(1, 0.15 * inch))

        # === Descriere ===
        desc = poc.get("description", "").strip()
        if desc:
            pdf.story.append(Paragraph(f"<b>Description:</b> {desc}", pdf.styles['Normal']))
            pdf.story.append(Spacer(1, 0.1 * inch))

        # === Cod ===
        code = poc.get("code", "").strip()
        if code:
            pdf.story.append(Paragraph("<b>Code:</b>", pdf.styles['Normal']))
            code_block = f"<pre><font name='Courier'>{escape_html(code)}</font></pre>"
            pdf.story.append(Paragraph(code_block, pdf.styles['Normal']))
            pdf.story.append(Spacer(1, 0.1 * inch))

        # === Imagini ===
        images = poc.get("images", [])
        if images:
            pdf.story.append(Paragraph("<b>Screenshots:</b>", pdf.styles['Normal']))
            for img_idx, img_bytes in enumerate(images):
                try:
                    pil_img = PILImage.open(io.BytesIO(img_bytes)).convert("RGB")
                    temp_path = f"temp_poc_{i}_{img_idx}.jpg"
                    pil_img.save(temp_path, "JPEG")
                    img = Image(temp_path, width=6*inch, height=3.5*inch)
                    img.hAlign = TA_CENTER
                    framed = KeepInFrame(maxWidth=6*inch, maxHeight=4*inch, content=[img])
                    pdf.story.append(framed)
                    pdf.story.append(Spacer(1, 0.1 * inch))
                    os.remove(temp_path)
                except Exception as e:
                    pdf.story.append(Paragraph(f"[Image error: {e}]", pdf.styles['Normal']))

        pdf.story.append(Spacer(1, 0.3 * inch))

    pdf.story.append(PageBreak())


def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
