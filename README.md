LEGAL EASE LOGO

If you have a project/company logo, place it in this folder.

Filename:

logo.png

Example:

assets/logo.png

The application will automatically use the logo
in the DOCX and PDF documents.

The project also works without a logo.
# LegalEase

## AI-Powered Legal Document Generator

LegalEase is an AI-powered application that helps users generate structured legal-document drafts.

The project uses:

- Streamlit
- FastAPI
- Google Gemini
- Python
- python-docx
- fpdf2

## Main Features

1. Legal document generation
2. Gemini AI integration
3. Editable document preview
4. TXT export
5. DOCX export
6. PDF export
7. Optional logo branding
8. FastAPI REST API
9. API documentation
10. Health-check endpoint

---

# Project Structure

```text
LegalEase/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── document_service.py
│       └── gemini_generator.py
│
├── frontend/
│   ├── __init__.py
│   └── app.py
│
├── utils/
│   ├── __init__.py
│   ├── exporters.py
│   └── text_utils.py
│
├── assets/
│   └── README.txt
│
├── tests/
│   ├── __init__.py
│   ├── test_health.py
│   └── test_exports.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md