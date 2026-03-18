import json
from fpdf import FPDF

def json_to_pdf(json_file, output_pdf):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for item in data:
        pdf.multi_cell(0, 10, f"Issue: {item['issue']}\nSolution: {item['solution']}\n" + "-"*20 + "\n")
    
    pdf.output(output_pdf)
    print(f"Successfully created {output_pdf}")

if __name__ == "__main__":
    json_to_pdf("ingest_data.json", "it_docs.pdf")