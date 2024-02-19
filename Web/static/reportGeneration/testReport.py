from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import utils
from reportlab.lib.units import inch

# Create a PDF document
pdf_filename = "blood_report_with_header.pdf"
document = SimpleDocTemplate(pdf_filename, pagesize=letter)

# Sample data - replace this with your own patient and blood test information
patient_name = "John Doe"
blood_type = "AB+"
results = {
    "Hemoglobin": "15.2 g/dL",
    "White Blood Cells (WBC)": "8,000/mm³",
    "Platelet Count": "250,000/mm³"
}
date = "2024-02-19"  # Replace with the actual date

# Sample image path - replace this with the path to your hospital logo
hospital_logo_path = "CraniumCryptics_Logo.png"

# Styles for the document
styles = getSampleStyleSheet()

# Custom styles for the report
title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=18, spaceAfter=12)
subtitle_style = ParagraphStyle('Subtitle', parent=styles['Title'], fontSize=14, textColor=colors.gray)
body_style = ParagraphStyle('BodyText', parent=styles['BodyText'], spaceAfter=12)

# Content to be added to the PDF
content = []

# Create a table for the header
header_table_data = [
    [Image(hospital_logo_path, width=150, height=50), Paragraph(f"Patient: {patient_name}<br/>Blood Type: {blood_type}<br/>Date: {date}", subtitle_style)],
]

header_table_style = [
    ('ALIGN', (0, 0), (0, 0), 'LEFT')
    # ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
]

header_table = Table(header_table_data, colWidths=[300, 200])
header_table.setStyle(header_table_style)

content.append(header_table)

# Add a line break after the header
content.append(Spacer(1, 24))

# Add title
title = Paragraph("Blood Test Report", title_style)
content.append(title)

# Add space
content.append(Spacer(1, 12))

# Add blood test results
results_title = Paragraph("Blood Test Results", subtitle_style)
content.append(results_title)

# Add individual test results
for test, result in results.items():
    result_info = Paragraph(f"<b>{test}:</b> {result}", body_style)
    content.append(result_info)

# Build the PDF document
document.build(content)
