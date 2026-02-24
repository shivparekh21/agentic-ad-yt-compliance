# 🛡️ Agentic Youtube Ad - Compliance 

An agentic AI pipeline that automatically audits video advertisements for brand compliance violations using LLMs and Azure cloud services.

## 🎯 What It Does

Submit a YouTube video URL → get back a full compliance report detailing violations, severity levels, and recommendations — all powered by GPT-4o and Azure AI.

```json
{
  "session_id": "24cf0ffa-bfa5-466f-bdb6-486669772d88",
  "video_id": "vid_24cf0ffa",
  "status": "FAIL",
  "final_report": "The video contains two critical compliance violations...",
  "compliance_results": [
    {
      "category": "Claim Violation",
      "severity": "CRITICAL",
      "description": "The claim 'invisible finish' could be misleading..."
    },
    {
      "category": "Trademark Violation",
      "severity": "CRITICAL",
      "description": "The phrase 'You can't see me' is a registered trademark..."
    }
  ]
}
```

## 🏗️ Architecture

```
YouTube URL
    │
    ▼
┌─────────────┐
│   Indexer   │  ← Downloads video, extracts transcript via Azure Video Indexer
└─────────────┘
    │
    ▼
┌─────────────┐
│   Auditor   │  ← Queries knowledge base + analyzes with GPT-4o
└─────────────┘
    │
    ▼
Compliance Report (JSON)
```

Built with **LangGraph** for agentic workflow orchestration.

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI |
| Workflow | LangGraph |
| LLM | Azure OpenAI (GPT-4o) |
| Transcription | Azure Video Indexer |
| Knowledge Base | Azure AI Search (RAG) |
| Embeddings | Azure OpenAI (text-embedding-3-small) |
| Video Download | yt-dlp |
| Observability | Azure Application Insights |
| LLM Tracing | LangSmith |
| Auth | Azure DefaultAzureCredential |

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- Azure subscription with the following services:
  - Azure OpenAI
  - Azure Video Indexer
  - Azure AI Search
  - Azure Storage
  - Azure Application Insights (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/brand-guardian-ai.git
cd brand-guardian-ai

# Install dependencies
uv sync
```

### Configuration

Create a `.env` file in the project root:

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_VERSION=
AZURE_OPENAI_CHAT_DEPLOYMENT=
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=

# Azure AI Search
AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_API_KEY=
AZURE_SEARCH_INDEX_NAME=

# Azure Video Indexer
AZURE_VI_NAME=
AZURE_VI_LOCATION=
AZURE_VI_ACCOUNT_ID=
AZURE_SUBSCRIPTION_ID=
AZURE_RESOURCE_GROUP=

# Azure Storage
AZURE_STORAGE_CONNECTION_STRING=

# Azure Identity (for Video Indexer auth)
AZURE_TENANT_ID=
AZURE_CLIENT_ID=
AZURE_CLIENT_SECRET=

# Observability (optional)
APPLICATIONINSIGHTS_CONNECTION_STRING=

# LangSmith (optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=agentic-ai-yt
```

### Index Your Compliance Documents

Add your brand guideline PDFs to `backend/data/` then run:

```bash
uv run python backend/scripts/index_documents.py
```

### Run the Server

```bash
uv run uvicorn backend.src.api.server:app --reload
```

Server starts at `http://127.0.0.1:8000` and opens Swagger UI automatically.

## 📡 API Endpoints

### `POST /audit`
Audit a video for brand compliance.

**Request:**
```json
{
  "video_url": "https://youtu.be/your-video-id"
}
```

**Response:**
```json
{
  "session_id": "uuid",
  "video_id": "vid_xxxxxxxx",
  "status": "PASS | FAIL",
  "final_report": "Summary of compliance analysis...",
  "compliance_results": [
    {
      "category": "Claim Violation",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "description": "Detailed description of the violation..."
    }
  ]
}
```

### `GET /health`
Health check endpoint.

```json
{
  "status": "healthy",
  "service": "Brand Guardian AI"
}
```

## 📊 Observability

- **Azure Application Insights** — request traces, failures, performance metrics
- **LangSmith** — LLM call traces, token usage, node-level debugging

## 📁 Project Structure

```
brand-guardian-ai/
├── backend/
│   ├── data/                    # Brand guideline PDFs
│   ├── scripts/
│   │   └── index_documents.py   # Knowledge base indexer
│   └── src/
│       ├── api/
│       │   ├── server.py        # FastAPI app
│       │   └── telemetry.py     # Azure Monitor setup
│       └── graph/
│           ├── workflow.py      # LangGraph definition
│           └── nodes/
│               ├── indexer.py   # Video download + transcription
│               └── auditor.py   # Compliance analysis
├── .env                         # Environment variables (not committed)
├── .gitignore
└── README.md
```

## 🔒 Security

- Secrets managed via `.env` (never committed to git)
- Azure identity-based authentication via `DefaultAzureCredential`
- App Registration with scoped Video Indexer permissions

