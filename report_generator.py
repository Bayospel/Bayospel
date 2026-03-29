from fpdf import FPDF
from datetime import datetime

class BayospelReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Bayospel Security Intelligence Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(target, scan_data, dns_data):
    pdf = BayospelReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # 1. Add Summary Section
    pdf.set_text_color(0, 0, 255) # Blue color for headers
    pdf.cell(200, 10, txt=f"Target: {target}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(10)

    # 2. Add Port Scan Results
    pdf.set_text_color(0, 0, 0) # Black color
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Port Scan Findings:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, txt=scan_data)
    pdf.ln(10)

    # 3. Add DNS Results
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="DNS Intelligence:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, txt=dns_data)

    # Save the file
    filename = f"Bayospel_Report_{target}.pdf"
    pdf.output(filename)
    return filename
