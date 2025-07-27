# Clausemint - Legal SaaS MVP

## Overview

This repository contains the source code and architectural specifications for **Clausemint**, a Legal SaaS MVP. The application is designed to generate legal documents, review uploaded contracts, and provide AI-powered clause analysis using system prompts and modular logic.

### Core Features
- **NDA Generation Tool** - Generate one-way, two-way, or three-way NDA contracts
- **Clause Redlining and RAG Review Tool** - Review contracts with Red-Amber-Green risk assessment
- **Conversational AI Chat Interface** - Summarization, feedback, and query resolution

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | HTML, CSS, JavaScript |
| **UI Framework** | Bootstrap (or Tailwind CSS) |
| **Backend** | Python 3.x, Django 4.x |
| **File Processing** | `pandas`, `pdfplumber`, `python-docx`, `docx2txt` |
| **AI Integration** | OpenAI GPT-4 API (system prompts per feature) |
| **Document Export** | `python-docx`, `reportlab`, optional: Aspose/LibreOffice |
| **Environment** | Docker (optional), Gunicorn + Nginx (for prod) |
| **Deployment** | Any cloud server (DigitalOcean, AWS, Heroku) |
| **Version Control** | Git + GitHub / GitLab |

---

## Project Structure

```
clausemint/
├── backend/
│   ├── core/                      # Django core project
│   ├── documents/                 # Document parsing, RAG logic
│   ├── nda_generator/             # NDA feature logic and prompts
│   ├── redlining/                 # Clause comparison and redline engine
│   ├── prompts/                   # System prompt files (text/JSON)
│   ├── media/                     # Uploaded and processed files
│   ├── static/                    # CSS, JS
│   ├── templates/                 # HTML templates
│   └── manage.py
├── frontend/
│   ├── js/                        # UI interactions
│   ├── css/
│   └── index.html
├── README.md
└── requirements.txt
```

---

## Features Breakdown

### 1. NDA Generator

**Objective**: Generate one-way, two-way, or three-way NDA contracts from user-provided information.

#### Inputs
- Parties involved
- Type of NDA
- Confidentiality duration
- Purpose
- Jurisdiction (optional)

#### Flow
1. User selects NDA Generator from sidebar
2. Form inputs are collected
3. If required fields are missing, the system asks follow-up questions via chat or form logic
4. Inputs are inserted into a **predefined system prompt**
5. Prompt is sent to OpenAI's API
6. Resulting NDA is displayed in the document viewer (center panel)
7. Option to edit and export (DOCX)

#### Prompt Sample
`prompts/nda/base_prompt.txt`
```txt
You are a legal assistant generating an NDA agreement. Format the output in legal English. Use the following inputs to construct the NDA:
- Parties: {{party_a}}, {{party_b}}, {{party_c}}
- Type: {{nda_type}}
- Purpose: {{purpose}}
- Duration: {{confidentiality_period}}
- Jurisdiction: {{jurisdiction}}
```

---

### 2. Clause Redlining + RAG Review

**Objective**: Allow users to upload legal documents and receive flagged clause reviews (Red/Amber/Green) with suggested improvements.

#### Flow
1. User uploads a document (PDF or DOCX)
2. File is parsed using:
   - `pdfplumber` or `PyMuPDF` (for PDFs)
   - `python-docx` (for DOCX)
3. Each clause is passed through a clause-type-specific system prompt
4. Each clause is scored and classified as:
   - **Red**: High risk
   - **Amber**: Needs review
   - **Green**: Standard/acceptable
5. Suggestions are generated using GPT
6. Document is rendered in viewer with RAG tags and optionally redlined

#### Prompt Sample
`prompts/redlining/ip_clause.txt`
```txt
You are a legal reviewer specializing in IP ownership clauses. Analyze the following clause and classify it:
- Red: Unfair or risky
- Amber: Ambiguous or unusual
- Green: Standard and fair

Then suggest a revised version if it is Red or Amber.
Clause: {{clause_text}}
```

#### Output
- Highlighted document in viewer
- Optional DOCX output with redlined text using `python-docx`
- Summary in right-side chat

---

### 3. Chat Assistant (Right Panel)

**Objective**: Respond to user questions about uploaded documents or generated content.

#### Capabilities
- Summarize uploaded NDA or legal document
- Explain clauses (e.g., "What does indemnity mean here?")
- Suggest alternative wordings
- Clarify flagged RAG sections

#### Implementation
- User messages passed with current document context to OpenAI API
- System prompt defines "Legal AI Assistant" behavior
- Chat session history optionally stored per user/document

---

## System Prompt Management

### Storage
- `prompts/` folder (text or JSON)
- Later version: database with admin UI

### Structure
```
/prompts/
├── nda/
│   ├── base_prompt.txt
│   └── followup_prompts.json
└── redlining/
    ├── ip_clause.txt
    ├── indemnity_clause.txt
    └── sla_clause.txt
```

- Prompts are inserted with Jinja-style variables using backend substitution

---

## Developer Setup

### Requirements
- Python 3.9+
- pip / venv
- Django 4.x
- OpenAI API Key

### Setup Instructions

```bash
git clone https://github.com/your-repo/clausemint.git
cd clausemint
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Add your OpenAI key to .env or Django settings
python manage.py migrate
python manage.py runserver
```

### API Key Configuration
Add your OpenAI key in the Django settings file or use `python-dotenv`:

```bash
OPENAI_API_KEY=your-key-here
```

---

## Testing Scenarios

| Test Case | Input | Expected Output |
|-----------|-------|-----------------|
| NDA Gen – Two-party | Basic form filled | Formatted NDA in viewer |
| NDA Gen – Missing party | Partial info | Tool asks for missing fields |
| Redline – IP clause | Docx upload | RAG mark + suggestion shown |
| RAG Summary | Large agreement | Clause summary + risks |
| Chat – Clause explain | Select clause + ask "Explain" | Simple legal definition |
| Export | Reviewed doc | DOCX with highlights or changes |

---

## Optional Libraries for Advanced Features

| Feature | Library |
|---------|---------|
| Tracked changes in DOCX | Aspose.Words, LibreOffice CLI |
| Clause similarity scoring | `scikit-learn`, `spacy`, `sentence-transformers` |
| Redline diffing | `diff-match-patch`, `difflib` |
| PDF markup | `PyMuPDF`, `pdf-annotate` |

---

## Future Enhancements

- Prompt tuning based on user feedback
- Feedback capture system per clause
- Clause classification model (fine-tuned legal BERT)
- Admin panel for prompt editing
- Clause suggestion history per user
- Multi-user collaboration
- Workspace & team management

---

## Document Export Strategy

- **DOCX**: All generated and reviewed documents exported via `python-docx`
- **Redlining**:
  - Initial MVP: inline colored suggestions
  - Later: tracked changes with full markup
- Optional watermark for drafts
- Option to export as PDF using `reportlab` or browser print

---

## Disclaimers and Legal Notices

Display non-advisory disclaimer on all generated documents:

> "This document is AI-generated and does not constitute legal advice. Please consult a qualified legal professional before using this in binding agreements."

---

## Contributor Guidelines

- Use feature branches per module
- PRs must include prompt version updates (if edited)
- Maintain clear prompt-to-feature mapping
- Log prompt test inputs and outputs in `/prompt_logs/`

---

## Contact and Collaboration

To collaborate, request access, or suggest feature improvements, contact:

- **Technical Lead**: Akshay [insert email/contact]
- **Legal Advisor**: Mandar

