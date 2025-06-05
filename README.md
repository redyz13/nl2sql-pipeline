
# NL2SQL Pipeline

This project aims to develop an AI-powered system capable of translating natural language queries into SQL queries, executing them on relational databases, and displaying results in both tabular and graphical formats.

## Features
- Zero-shot SQL generation using OpenAI GPT models
- Dynamic chart visualization
- CSV export functionality
- Interactive user interface via Gradio
- REST API integration using Connexion and Flask
- Safe query execution (only SELECT operations)

## Project Structure
```
nl2sql-pipeline/
├── data/                  # Data files and resources
├── legacy/                # Archived modules (consult the README inside for reference)
├── notebooks/             # Development and exploration notebooks
├── prompts/               # LLM prompt templates
├── src/
│   └── zero_shot/         # Core zero-shot pipeline modules
├── .dockerignore
├── .gitignore
├── Dockerfile
├── Dockerfile.ui
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Quick Setup

### 1. Virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows
```

### 2. Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file:
```ini
DATABASE_URL=postgresql://user:password@host:port/db
OPENAI_API_KEY=your-api-key
APP_ENV=development
API_HOST=localhost
API_PORT=8000
ENTRY_MODULE=zero_shot.api.app
UI_MODULE=zero_shot.ui.app
```

## Usage

Launch API:
```bash
cd src
python -m zero_shot.api.app
```

Launch Gradio UI:
```bash
cd src
python -m zero_shot.ui.app
```

## Legacy Modules
For details on legacy modules such as schema linking, see the dedicated README in `legacy/`.

## Database Overview
- Total tables: 6839
- Average columns per table: ~18.9
- Tables with primary key: ~92%
- High complexity and large schema support

## Acknowledgements
This project builds upon research in NL2SQL solutions including CHESS, PICARD,RED and related literature.
