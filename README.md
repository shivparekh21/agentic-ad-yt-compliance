**One line summary:
**
Built an agentic AI pipeline that automatically audits video advertisements for brand compliance violations using LLMs and Azure cloud services.

**Bullet points:
**

Designed a multi-node LangGraph workflow that downloads YouTube videos, extracts transcripts via Azure Video Indexer, and analyzes content against brand compliance rules using GPT-4o
Built a REST API with FastAPI exposing an /audit endpoint that returns structured compliance violations with category, severity, and descriptions
Implemented a RAG pipeline using Azure AI Search as a vector knowledge base, indexing brand guideline PDFs with Azure OpenAI embeddings for context-aware compliance checking
Integrated end-to-end observability with Azure Application Insights for telemetry and LangSmith for LLM tracing and debugging
Deployed with Azure identity-based authentication (DefaultAzureCredential) following production security best practices


**Skills it demonstrates for recruiters:
**
Agentic AI / LangGraph
RAG pipelines
Azure cloud services
API development
LLMOps / observability

