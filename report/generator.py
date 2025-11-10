# report/generator.py
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from pathlib import Path
import base64
import io

# === FONT ROMÂNESC – CU TRY/EXCEPT + FALLBACK ===
font_path = Path(__file__).parent.parent / "assets" / "fonts" / "DejaVuSans.ttf"

try:
    if font_path.exists():
        pdfmetrics.registerFont(TTFont("DejaVu", str(font_path)))
        FONT_NAME = "DejaVu"
    else:
        FONT_NAME = "Helvetica"  # fallback
except Exception as e:
    print(f"[WARNING] DejaVuSans.ttf nu poate fi încărcat: {e}")
    FONT_NAME = "Helvetica"

class PDFReport:
    def __init__(self, logo_path=None, watermark=False):
        self.buffer = BytesIO()
        self.doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            topMargin=0.8*inch,
            bottomMargin=0.8*inch,
            leftMargin=0.7*inch,
            rightMargin=0.7*inch
        )
        self.logo_path = logo_path      # ← ACCEPTĂM logo_path
        self.watermark = watermark      # ← ACCEPTĂM watermark
        self.story = []

        # === STILURI CU DEJAVU ===
        styles = getSampleStyleSheet()
        self.styles = {
            'Title': ParagraphStyle('Title', parent=styles['Title'], fontName='DejaVu', fontSize=24, alignment=TA_CENTER, textColor=colors.HexColor("#003366")),
            'Heading1': ParagraphStyle('Heading1', parent=styles['Heading1'], fontName='DejaVu', fontSize=18),
            'Heading2': ParagraphStyle('Heading2', parent=styles['Heading2'], fontName='DejaVu', fontSize=14, textColor=colors.HexColor("#2E4057")),
            'Normal': ParagraphStyle('Normal', parent=styles['Normal'], fontName='DejaVu', fontSize=11, leading=16, alignment=TA_JUSTIFY),
            'Code': ParagraphStyle('Code', fontName='DejaVu', fontSize=9, leading=12, backColor=colors.HexColor("#0d1117"), textColor=colors.HexColor("#c9d1d9"), leftIndent=15, rightIndent=15, spaceBefore=12, spaceAfter=12, borderPadding=10, borderColor=colors.HexColor("#30363d"), borderWidth=1, borderRadius=6),
        }

    def add_logo_header(self):
        if self.logo_path:
            try:
                img_data = base64.b64decode(self.logo_path.split(',')[1])
                img = Image(io.BytesIO(img_data), width=1.5*inch, height=1*inch)
                img.hAlign = 'LEFT'
                self.story.append(img)
                self.story.append(Spacer(1, 0.2*inch))
            except:
                pass  # logo invalid → ignoră

    def generate(self, **kwargs):
        # === APELEAZĂ SECȚIUNI ===
        from .sections.cover import add_cover
        from .sections.toc import add_toc
        from .sections.legal import add_legal
        from .sections.contact import add_contact_section
        from .sections.overview import add_overview
        from .sections.scope import add_scope
        from .sections.severity import add_severity_ratings
        from .sections.executive import add_executive_summary
        from .sections.findings import add_technical_findings
        from .sections.poc import add_poc

        # COVER + LOGO
        self.add_logo_header()
        add_cover(self, **kwargs)
        self.story.append(PageBreak())

        # RESTUL SECȚIUNILOR
        add_toc(self, findings=st.session_state.get("findings", []))
        self.story.append(PageBreak())
        add_legal(self)
        add_contact_section(self)
        self.story.append(PageBreak())
        add_overview(self, overview_text=st.session_state.get("overview", ""))
        add_scope(self, scope=st.session_state.get("scope", ""))
        add_severity_ratings(self)
        self.story.append(PageBreak())
        add_executive_summary(self, findings=st.session_state.get("findings", []), executive_text=st.session_state.get("executive_summary_text", ""))
        self.story.append(PageBreak())
        add_technical_findings(self, findings=st.session_state.get("findings", []))
        self.story.append(PageBreak())
        add_poc(self, poc_list=st.session_state.get("pocs", []))

        self.doc.build(self.story)
        return self.buffer.getvalue()
