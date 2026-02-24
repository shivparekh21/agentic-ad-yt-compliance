import uuid
import logging
import threading
import webbrowser
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional

from dotenv import load_dotenv
load_dotenv(override=True)

from backend.src.api.telemetry import setup_telemetry
setup_telemetry()

from backend.src.graph.workflow import app as compliance_graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api-server")

app = FastAPI(
    title="Brand Guardian AI API",
    description="API for auditing video content against brand compliance rules.",
    version="1.0.0"
)

@app.on_event("startup")
async def open_browser():
    def _open():
        import time
        time.sleep(1.5)  # Wait for server to fully start
        webbrowser.open("http://127.0.0.1:8000/docs")
    threading.Thread(target=_open, daemon=True).start()

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")



class AuditRequest(BaseModel):
    video_url: str


class ComplianceIssue(BaseModel):
    category: str
    severity: str
    description: str


class AuditResponse(BaseModel):
    session_id: str
    video_id: str
    status: str
    final_report: str
    compliance_results: List[ComplianceIssue]


@app.post("/audit", response_model=AuditResponse)
async def audit_video(request: AuditRequest):
    session_id = str(uuid.uuid4())
    video_id_short = f"vid_{session_id[:8]}"

    logger.info(f"Received Audit Request: {request.video_url} (Session: {session_id})")

    initial_inputs = {
        "video_url": request.video_url,
        "video_id": video_id_short,
        "compliance_results": [],
        "errors": []
    }

    try:
        final_state = compliance_graph.invoke(initial_inputs)

        return AuditResponse(
            session_id=session_id,
            video_id=final_state.get("video_id"),
            status=final_state.get("final_status", "UNKNOWN"),
            final_report=final_state.get("final_report", "No report generated."),
            compliance_results=final_state.get("compliance_results", [])
        )

    except Exception as e:
        logger.error(f"Audit Failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Workflow Execution Failed: {str(e)}"
        )


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Brand Guardian AI"}

    
'''
To run:
uv run uvicorn backend.src.api.server:app --reload
'''