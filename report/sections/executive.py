# report/sections/executive.py
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib import colors
from reportlab.lib.units import inch
import streamlit as st
import pandas as pd
import plotly.express as px

# ================================================================
# PDF – EXECUTIVE SUMMARY (PIE CHART + TABEL + TEXT)
# ================================================================
def add_executive_summary(pdf, findings, executive_text="", **kwargs):
    pdf.story.append(Paragraph("Executive Summary", pdf.styles['Heading1']))
    pdf.story.append(Spacer(1, 0.4 * inch))

    # === PIE CHART ===
    levels = ["Critical", "High", "Moderate", "Low", "Informational"]
    counts = [sum(1 for f in findings if f.get("severity") == sev) for sev in levels]
    
    d = Drawing(450, 250)
    pc = Pie()
    pc.x = 150
    pc.y = 30
    pc.width = pc.height = 180
    pc.data = counts
    pc.labels = levels
    pc.slices.strokeWidth = 1
    pc.slices.strokeColor = colors.white
    pc.slices.fontName = "DejaVu"
    pc.slices.fontSize = 10

    # Culori exact ca în Streamlit
    pc.slices[0].fillColor = colors.HexColor("#dc2626")  # Critical
    pc.slices[1].fillColor = colors.HexColor("#f97316")  # High
    pc.slices[2].fillColor = colors.HexColor("#facc15")  # Moderate
    pc.slices[3].fillColor = colors.HexColor("#10b981")  # Low
    pc.slices[4].fillColor = colors.HexColor("#6366f1")  # Informational

    d.add(pc)
    pdf.story-append(d)
    pdf.story.append(Spacer(1, 0.3 * inch))

    # === TABEL SUB GRAFIC ===
    data = [["Severity", "Count"]]
    for i, sev in enumerate(levels):
        data.append([sev, str(counts[i])])

    table = Table(data, colWidths=[3.2 * inch, 1.3 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8f9fa")),
    ]))
    pdf.story.append(table)
    pdf.story.append(Spacer(1, 0.4 * inch))

    # === TEXT EXECUTIVE (DIACRITICE PERFECTE) ===
    if executive_text:
        # Suportă \n ca paragraf nou
        paragraphs = [p.strip() for p in executive_text.split("\n") if p.strip()]
        for para in paragraphs:
            pdf.story.append(Paragraph(para, pdf.styles['Normal']))
            pdf.story.append(Spacer(1, 0.15 * inch))
    else:
        pdf.story.append(Paragraph("No executive summary provided.", pdf.styles['Normal']))

    pdf.story.append(Spacer(1, 0.5 * inch))


# ================================================================
# STREAMLIT – UI EXECUTIVE SUMMARY
# ================================================================
def render():
    st.subheader("Executive Summary")
    
    if not st.session_state.get("findings"):
        st.info("No findings yet.")
        return

    # === PIE CHART INTERACTIV ===
    levels = ["Critical", "High", "Moderate", "Low", "Informational"]
    counts = {sev: sum(1 for f in st.session_state.findings if f.get("severity") == sev) for sev in levels}
    df = pd.DataFrame(list(counts.items()), columns=["Severity", "Count"])
    
    fig = px.pie(
        df, values="Count", names="Severity",
        color_discrete_sequence=["#dc2626", "#f97316", "#facc15", "#10b981", "#6366f1"],
        hole=0.4
    )
    fig.update_layout(
        title="Vulnerability Distribution",
        title_x=0.5,
        font=dict(size=14)
    )
    st.plotly_chart(fig, use_container_width=True)

    # === TABEL ===
    st.markdown("#### Severity Breakdown")
    st.table(df.style.format({"Count": "{:.0f}"}))

    # === TEXT AREA ===
    current_text = st.session_state.get("executive_summary_text", "")
    new_text = st.text_area(
        "Write Executive Summary (supports line breaks)",
        value=current_text,
        height=200,
        key="exec_summary_text_area",
        help="Textul introdus aici va apărea în PDF sub grafic."
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Save Text", type="primary", key="save_exec_text"):
            st.session_state.executive_summary_text = new_text
            st.success("Executive Summary saved!")
            st.rerun()
    with col2:
        if st.button("Clear Text"):
            st.session_state.executive_summary_text = ""
            st.rerun()
