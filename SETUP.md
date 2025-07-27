# Clausemint - Setup Guide

## Project Overview
Clausemint is a Legal SaaS MVP that provides AI-powered legal document generation and analysis. The application features:

- **NDA Generator**: Create professional NDA agreements with AI assistance
- **Document Review**: Analyze legal documents with Red-Amber-Green risk assessment
- **Chat Assistant**: AI-powered legal document Q&A and insights

## Tech Stack
- **Backend**: Django 4.2.7, Python 3.x
- **Frontend**: HTML, CSS, JavaScript with Bootstrap 5
- **AI**: OpenAI GPT-4 API
- **Database**: SQLite (development)
- **File Processing**: python-docx, docx2txt

## Installation & Setup

### 1. Prerequisites
- Python 3.9+
- OpenAI API Key

### 2. Clone and Setup
```bash
# Navigate to the project directory
cd clausemint

# Create virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r ../requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the backend directory:
```bash
# Django Settings
SECRET_KEY=django-insecure-clausemint-dev-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# OpenAI API Key (replace with your actual key)
OPENAI_API_KEY=your-openai-api-key-here
```

### 4. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### 5. Start Development Server
```bash
python manage.py runserver
```

The application will be available at: http://localhost:8000

## Features

### NDA Generator
- Generate one-way, two-way, or three-way NDA agreements
- Customizable parameters (parties, purpose, duration, jurisdiction)
- AI-powered document generation
- Export to DOCX format

### Document Review
- Upload DOCX documents for analysis
- AI-powered clause analysis with RAG (Red-Amber-Green) risk assessment
- Detailed explanations and improvement suggestions
- Risk summary and statistics

### Chat Assistant
- Ask questions about uploaded documents
- Get AI-powered legal insights and explanations
- Interactive chat interface
- Document context awareness

## File Structure
```
clausemint/
├── backend/
│   ├── core/                 # Django project settings
│   ├── documents/           # Document upload and chat
│   ├── nda_generator/       # NDA generation logic
│   ├── redlining/          # Document analysis
│   ├── prompts/            # AI prompt templates
│   ├── static/             # CSS, JS files
│   ├── templates/          # HTML templates
│   └── manage.py
├── requirements.txt
├── README.md
└── SETUP.md
```

## API Endpoints

### Documents
- `POST /api/upload/` - Upload document
- `GET /api/documents/` - List documents
- `POST /api/chat/` - Send chat message
- `GET /api/chat/<id>/` - Get chat history

### NDA Generator
- `POST /api/nda/generate/` - Generate NDA
- `POST /api/nda/export/` - Export NDA

### Document Analysis
- `POST /api/redlining/analyze/` - Analyze document
- `POST /api/redlining/analyze-clause/` - Analyze single clause

## Usage

### 1. NDA Generation
1. Navigate to the NDA Generator tab
2. Fill in the required fields (Party A, Party B, Purpose)
3. Select NDA type and other parameters
4. Click "Generate NDA"
5. Review and export the generated document

### 2. Document Review
1. Upload a DOCX document using the sidebar
2. Switch to Document Review tab
3. View the analysis results with risk assessment
4. Review individual clause analysis and suggestions

### 3. Chat Assistant
1. Upload a document first
2. Switch to Chat Assistant tab
3. Ask questions about the document
4. Get AI-powered responses and insights

## Customization

### Adding New Prompts
Add new prompt files in `backend/prompts/`:
```
prompts/
├── nda/
│   └── base_prompt.txt
└── redlining/
    ├── ip_clause.txt
    └── indemnity_clause.txt
```

### Styling
The application uses a modern dark theme. Customize colors in `backend/static/css/main.css`:
- Primary colors: `--accent-primary: #6366f1`
- Background: `--bg-primary: #0a0a0a`
- Text: `--text-primary: #ffffff`

## Troubleshooting

### Common Issues
1. **OpenAI API Error**: Ensure your API key is set in the .env file
2. **File Upload Error**: Only DOCX files are supported
3. **Database Error**: Run `python manage.py migrate`

### Development
- Enable DEBUG=True for detailed error messages
- Check Django logs for API errors
- Use browser developer tools for frontend debugging

## Production Deployment

### Requirements
- Production database (PostgreSQL recommended)
- Static file serving (Nginx)
- WSGI server (Gunicorn)
- Environment variables for production settings

### Security
- Change SECRET_KEY in production
- Set DEBUG=False
- Configure proper ALLOWED_HOSTS
- Use HTTPS in production

## Support
For technical support or feature requests, contact the development team.

---

**Note**: This is an MVP version. For production use, additional security, testing, and scalability features should be implemented. 