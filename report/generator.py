# report/generator.py
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import inch
from pathlib import Path
import base64
import io

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
        self.logo_path = logo_path
        self.watermark = watermark
        self.story = []

        # === FONTURI – DOAR LA RULARE (SIGUR!) ===
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont

            fonts_dir = Path(__file__).parent.parent / "assets" / "fonts"
            dejavu = fonts_dir / "DejaVuSans.ttf"
            dejavu_bold = fonts_dir / "DejaVuSans-Bold.ttf"
            dejavu_italic = fonts_dir / "DejaVuSans-Oblique.ttf"
            dejavu_bolditalic = fonts_dir / "DejaVuSans-BoldOblique.ttf"

            # Înregistrăm toate variantele
            pdfmetrics.registerFont(TTFont("DejaVu", str(dejavu)))
            pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(dejavu_bold)))
            pdfmetrics.registerFont(TTFont("DejaVu-Italic", str(dejavu_italic)))
            pdfmetrics.registerFont(TTFont("DejaVu-BoldItalic", str(dejavu_bolditalic)))

            pdfmetrics.registerFontFamily(
                "DejaVu",
                normal="DejaVu",
                bold="DejaVu-Bold",
                italic="DejaVu-Italic",
                boldItalic="DejaVu-BoldItalic"
            )
            self.font_name = "DejaVu"
        except Exception as e:
            print(f"[FALLBACK] Font loading failed: {e}")
            self.font_name = "Helvetica"

        # === STILURI ===
        styles = getSampleStyleSheet()
        self.styles = {
            'Title': ParagraphStyle('Title', fontName=self.font_name, fontSize=42, leading=48, alignment=TA_CENTER, textColor=colors.HexColor("#003366"), spaceAfter=30),
            'Heading1': ParagraphStyle('Heading1', fontName=self.font_name, fontSize=18, leading=24),
            'Heading2': ParagraphStyle('Heading2', fontName=self.font_name, fontSize=14, textColor=colors.HexColor("#2E4057")),
            'Normal': ParagraphStyle('Normal', fontName=self.font_name, fontSize=11, leading=16, alignment=TA_JUSTIFY),
            'Code': ParagraphStyle('Code', fontName='Courier', fontSize=9, backColor=colors.HexColor("#0d1117"), textColor=colors.HexColor("#c9d1d9"), borderPadding=10, borderColor=colors.HexColor("#30363d"), borderWidth=1, borderRadius=6),
        
            # ← ADAUGĂ ACEST STIL NOU
            'Confidential': ParagraphStyle(
                'Confidential',
                fontName=self.font_name,
                fontSize=20,
                leading=28,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#dc2626"),  # roșu intens
                spaceAfter=60,
                fontWeight='bold'
            ),
        }
# report/generator.py – DOAR METODA generate() (înlocuiește complet)
    def generate(self, **kwargs):
        try:
            # === IMPORT STREAMLIT AICI (CRUCIAL!) ===
            import streamlit as st
    
            # === IMPORTURI LENEȘE SECȚIUNI ===
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
    
            # === CONSTRUIRE PDF ===
            add_cover(self, **kwargs)
            self.story.append(PageBreak())
    
          
            add_toc(
                self,
                findings=st.session_state.get("findings", []),
                pocs=st.session_state.get("pocs", [])
            )
    
            add_legal(self)
            add_contact_section(self)
            self.story.append(PageBreak())
    
            add_overview(self, overview_text=st.session_state.get("overview", ""))
            add_scope(self, scope_text=st.session_state.get("scope", ""))
            add_severity_ratings(self)
            self.story.append(PageBreak())
    
            add_executive_summary(
                self,
                findings=st.session_state.get("findings", []),
                executive_text=st.session_state.get("executive_summary_text", "")
            )
            self.story.append(PageBreak())
    
            add_technical_findings(self, findings=st.session_state.get("findings", []))
            self.story.append(PageBreak())
    
            add_poc(self, pocs=st.session_state.get("pocs", []))
            self.story.append(PageBreak()))
    
            # === FINALIZARE ===
            self.doc.build(self.story)
            self.buffer.seek(0)
            return self.buffer.getvalue()
    
        except Exception as e:
            import traceback
            try:
                import streamlit as st
                st.error("PDF generation failed!")
                st.code(traceback.format_exc())
            except:
                pass
            return None
