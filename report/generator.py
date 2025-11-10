# report/generator.py
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

# Import secțiuni
from .sections.cover import add_cover
from .sections.toc import add_toc
from .sections.legal import add_legal
from .sections.overview import add_overview
from .sections.scope import add_scope
from .sections.severity import add_severity_ratings
from .sections.executive import add_executive_summary
from .sections.findings import add_technical_findings
from .sections.poc import add_poc

class PDFReport:
    def __init__(self):
        self.buffer = BytesIO()
        self.doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            topMargin=0.8*inch,
            bottomMargin=0.8*inch,
            leftMargin=0.7*inch,
            rightMargin=0.7*inch
        )
        self.styles = self._create_styles()
        self.story = []

    def _create_styles(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CorporateTitle',
            fontSize=24,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#003366")
        ))
        styles.add(ParagraphStyle(
            name='CorporateSubtitle',
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#555555")
        ))
        styles.add(ParagraphStyle(
            name='Confidential',
            fontSize=10,
            textColor=colors.red,
            alignment=TA_CENTER
        ))
        styles.add(ParagraphStyle(
            'Code',
            fontName='DejaVu',
            fontSize=9,
            leading=12,
            backColor=colors.HexColor("#0d1117"),
            textColor=colors.HexColor("#c9d1d9"),
            leftIndent=15,
            rightIndent=15,
            spaceBefore=12,
            spaceAfter=12,
            borderPadding=10,
            borderColor=colors.HexColor("#30363d"),
            borderWidth=1,
            borderRadius=6
        )
        return styles

    def generate(self, findings, client, project, pocs=None, 
                 executive_text=None, tester=None, date=None, 
                 scope=None, overview_text=None, poc_list=None, **kwargs):
        
        # PAGINA 1 – COVER
        add_cover(self, client=client, project=project, tester=tester, date=date)
        self.story.append(PageBreak())
        # PAGINA 2 – TOC
        add_toc(self, findings=findings, poc_list=poc_list or [])
        self.story.append(PageBreak())
        # PAGINA 3 – LEGAL
        add_legal_and_contact(self, client=client)

        # PAGINA 4 – OVERVIEW + SCOPE + SEVERITY
        add_assessment_overview(self, overview=overview_text or "No overview provided.")
        add_scope(self, scope=scope or "No scope defined.")
        add_severity_ratings(self, **kwargs)

        # PAGINA 5 – EXECUTIVE
        self.story.append(PageBreak())
        add_executive_summary(self, findings=findings, executive_text=executive_text or "No summary.")

        # PAGINA 6+ – FINDINGS
        self.story.append(PageBreak())
        add_technical_findings(self, findings=findings)

        # POC
        # PAGINA 7 – POC INDEPENDENT
        self.story.append(PageBreak())
        add_poc(self, poc_list=poc_list)
        #if pocs:
         #   self.story.append(PageBreak())
          #  add_poc(self, pocs=pocs)

        self.doc.build(self.story)
        return self.buffer.getvalue()
