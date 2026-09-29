import os
from datetime import date

import requests
import streamlit as st
from dotenv import load_dotenv

from utils.exporters import (
    create_docx_bytes,
    create_pdf_bytes,
    create_txt_bytes,
)


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)


st.title("⚖️ LegalEase")
st.caption(
    "AI-powered legal document draft generator"
)


with st.sidebar:

    st.header("About LegalEase")

    st.write(
        "LegalEase helps users create structured "
        "legal-document drafts using Generative AI."
    )

    st.write(
        "Supported exports: TXT • DOCX • PDF"
    )

    st.warning(
        "AI-generated legal documents may contain errors. "
        "Review the document with a qualified legal "
        "professional before signing or relying on it."
    )

    st.caption(
        f"Backend: {BACKEND_URL}"
    )


document_types = [
    "Rental Agreement",
    "Employment Agreement",
    "Non-Disclosure Agreement",
    "Service Agreement",
    "Leave and License Agreement",
    "Affidavit",
    "Loan Agreement",
    "Partnership Agreement",
    "Custom",
]


left, right = st.columns(2)


with left:

    selected_type = st.selectbox(
        "Document Type",
        document_types
    )

    if selected_type == "Custom":

        document_type = st.text_input(
            "Custom Document Type"
        )

    else:

        document_type = selected_type


    parties = st.text_area(
        "Parties",
        placeholder=(
            "Landlord: Arun Kumar\n"
            "Tenant: Priya"
        ),
        height=130,
    )


    terms = st.text_area(
        "Terms and Conditions",
        placeholder=(
            "Enter rent, duration, duties, "
            "payment terms, etc."
        ),
        height=180,
    )


with right:

    effective_date = st.date_input(
        "Effective Date",
        value=date.today()
    )


    jurisdiction = st.text_input(
        "Jurisdiction (Optional)",
        placeholder=(
            "Chennai, Tamil Nadu, India"
        ),
    )


    additional = st.text_area(
        "Additional Instructions (Optional)",
        height=180,
    )


if "document" not in st.session_state:

    st.session_state.document = ""


if "model" not in st.session_state:

    st.session_state.model = ""


if st.button(
    "⚖️ Generate Document",
    type="primary",
    use_container_width=True
):

    if not document_type.strip():

        st.error(
            "Please enter a document type."
        )

    elif not parties.strip():

        st.error(
            "Please enter the parties."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms and conditions."
        )

    else:

        payload = {

            "document_type":
                document_type.strip(),

            "parties":
                parties.strip(),

            "terms":
                terms.strip(),

            "effective_date":
                effective_date.isoformat(),

            "jurisdiction":
                jurisdiction.strip(),

            "additional_instructions":
                additional.strip(),
        }


        with st.spinner(
            "Generating document..."
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120,
                )


                if response.ok:

                    data = response.json()

                    st.session_state.document = (
                        data["content"]
                    )

                    st.session_state.model = (
                        data.get("model", "")
                    )

                    st.success(
                        "Document generated successfully."
                    )


                else:

                    try:

                        detail = response.json().get(
                            "detail",
                            response.text
                        )

                    except Exception:

                        detail = response.text


                    st.error(
                        f"Backend Error: {detail}"
                    )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to the backend. "
                    "Start FastAPI first."
                )


            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. "
                    "Please try again."
                )


            except Exception as exc:

                st.error(
                    f"Frontend error: {exc}"
                )


if st.session_state.document:

    st.divider()

    st.subheader(
        "Generated Document"
    )


    edited = st.text_area(
        "Edit the generated draft",
        value=st.session_state.document,
        height=500,
    )


    st.session_state.document = edited


    content = st.session_state.document


    st.subheader("Download")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.download_button(
            "Download TXT",
            create_txt_bytes(content),
            "legalease_document.txt",
            "text/plain",
            use_container_width=True,
        )


    with col2:

        st.download_button(
            "Download DOCX",
            create_docx_bytes(content),
            "legalease_document.docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )


    with col3:

        st.download_button(
            "Download PDF",
            create_pdf_bytes(content),
            "legalease_document.pdf",
            "application/pdf",
            use_container_width=True,
        )


    if st.session_state.model:

        st.caption(
            f"Model: {st.session_state.model}"
        )


else:

    st.info(
        "Enter your document details above "
        "and click Generate Document."
    )