
import streamlit as st
import pdfplumber
import fitz  # PyMuPDF
from PIL import Image
import tempfile

st.title("📄 Table Highlighter in PDF")

pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

def highlight_tables(input_path, output_path):
    doc = fitz.open(input_path)
    with pdfplumber.open(input_path) as pdf:
        for i, (page_plumber, page_fitz) in enumerate(zip(pdf.pages, doc)):
            tables = page_plumber.find_tables()
            for table in tables:
                x0, y0, x1, y1 = table.bbox
                rect = fitz.Rect(x0, y0, x1, y1)
                page_fitz.draw_rect(rect, color=(1, 0, 0), width=2)
    doc.save(output_path)

def show_first_page(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=150)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    st.image(img, caption="First Page with Highlighted Tables", use_column_width=True)

if pdf_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_input:
        tmp_input.write(pdf_file.read())
        input_path = tmp_input.name

    output_path = input_path.replace(".pdf", "_highlighted.pdf")
    highlight_tables(input_path, output_path)

    st.success("✅ Tables have been highlighted successfully!")
    show_first_page(output_path)

    with open(output_path, "rb") as out_pdf:
        st.download_button("📥 Download Highlighted PDF", out_pdf, file_name="highlighted_output.pdf")
