import operator
from token import OP
from typing import Annotated, List, Dict, Any, Optional, TypedDict

# Error Report 
# Defining schema for single compliance result
class ComplianceResult(TypedDict):
    category: str
    description: str # description of violation
    severity: str # severity of violation    CRITICAL, HIGH, MEDIUM, LOW
    timestamp: Optional[str] 


# Defining GLOBAL STATE for the graph
# this defines the state that gets passed between nodes in the graph
class VideoAuditState(TypedDict):
    '''
    Define the data structure for langgraph execution state
    Main container that holds all the data for the video audit process
    right from URL input to the final compliance results
    '''
    #input parameters
    video_url: str
    video_id: str

    # ingestion and extraction data
    local_video_path: Optional[str]
    video_metadata: Dict[str, Any]   # {"duration":15, "resolution":"1080p", "fps":30}
    transcript: Optional[str]  # fully extracted speech to text
    ocr_text: List[str]

    # analysis output
    # Stores the list of all compliance violations found in the video by AI
    compliance_results: Annotated[List[ComplianceResult], operator.add] # cumulative list of compliance results

    # final deliverables
    final_status: str  # PASS | FAIL
    final_report: str  # markdown formatted report of all compliance violations

    # system observability
    # Errors : API timeout, system level error
    # list of system level crashes e.g. azure mount 
    errors : Annotated[List[str], operator.add]
     


