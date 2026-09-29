from io import BytesIO

from docx import Document
from docx.shared import Pt
from fpdf import FPDF


def create_txt_bytes(content: str) -> bytes:
    """
    Convert document text into TXT file bytes.
    """
    return content.encode("utf-8")


def create_docx_bytes(
    content: str,
    document_type: str = "Legal Document"
) -> bytes:
    """
    Create a DOCX document from the generated legal content.
    """

    document = Document()

    # Normal text style
    style = document.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(11)

    # Document title
    title = document.add_paragraph()

    title_run = title.add_run(document_type)
    title_run.bold = True
    title_run.font.name = "Times New Roman"
    title_run.font.size = Pt(16)

    # Document content
    for line in content.splitlines():

        text = line.strip()

        if not text:
            document.add_paragraph()
            continue

        paragraph = document.add_paragraph()

        run = paragraph.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)

    # Save into memory
    output = BytesIO()
    document.save(output)

    return output.getvalue()


def create_pdf_bytes(
    content: str,
    document_type: str = "Legal Document"
) -> bytes:
    """
    Create a PDF document from the generated legal content.
    """

    pdf = FPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=18
    )

    pdf.set_margins(
        left=18,
        top=18,
        right=18
    )

    pdf.add_page()

    # Title
    pdf.set_font(
        "Helvetica",
        "B",
        16
    )

    pdf.multi_cell(
        0,
        10,
        document_type
    )

    pdf.ln(5)

    # Content
    for line in content.splitlines():

        text = line.strip()

        if not text:
            pdf.ln(4)
            continue

        # Convert unsupported Unicode characters
        safe_text = (
            text
            .encode("latin-1", "replace")
            .decode("latin-1")
        )

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        pdf.multi_cell(
            0,
            6,
            safe_text
        )

    # Save PDF into memory
    output = BytesIO()

    pdf.output(output)

    return output.getvalue()