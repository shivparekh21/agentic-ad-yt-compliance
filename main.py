"""
Main Execution Entry Point for Brand Guardian AI.

This file is the "control center" that starts and manages the entire 
compliance audit workflow. Think of it as the master switch that:
1. Sets up the audit request
2. Runs the AI workflow
3. Displays the final compliance report
"""

# Standard library imports for basic Python functionality
import uuid      # Generates unique IDs (like session tracking numbers)
import json      # Handles JSON data formatting (converts Python dicts to readable text)
import logging   # Records what happens during execution (like a flight recorder)
from pprint import pprint  # Pretty-prints data structures (unused here, but available)


# Load environment variables from .env file
# This reads API keys, database credentials, etc. without hardcoding them
from dotenv import load_dotenv
load_dotenv(override=True)  # override=True means .env values take priority over system variables

# Import the main workflow graph (the "brain" of your compliance system)
from backend.src.graph.workflow import app

# Configure logging - sets up the "flight recorder" for your application
logging.basicConfig(
    level=logging.INFO,        # INFO = show important events (DEBUG would show everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  
    # Format: timestamp - logger_name - severity - message
    # Example: "2024-01-15 10:30:45 - brand-guardian - INFO - Starting audit"
)
logger = logging.getLogger("brand-guardian-runner")  # Creates a named logger for this module


def run_cli_simulation():
    """
    Simulates a Video Compliance Audit request.
    
    This function orchestrates the entire audit process:
    - Creates a unique session ID
    - Prepares the video URL and metadata
    - Runs it through the AI workflow
    - Displays the compliance results
    """
    
    session_id = str(uuid.uuid4())  # uuid4() generates random UUID
    logger.info(f"Starting Audit Session: {session_id}")

    # This dictionary contains all the input data for the workflow
    initial_inputs = {
        # The YouTube video to audit
        "video_url": "https://youtu.be/dT7S75eYhcQ",
        
        # Shortened video ID for easier tracking (first 8 chars of session ID)
        "video_id": f"vid_{session_id[:8]}",
        
        # Empty list that will store compliance violations found
        # Will be populated by the Auditor node
        "compliance_results": [],
        
        # Empty list for any errors during processing
        # Example: ["Download failed", "Transcript unavailable"]
        "errors": []
    }

    # ========== DISPLAY SECTION: INPUT SUMMARY ==========
    print("\n--- 1.nput Payload: INITIALIZING WORKFLOW ---")
    # json.dumps() converts Python dict to formatted JSON string
    print(f"I {json.dumps(initial_inputs, indent=2)}")

    try:
        # app.invoke() triggers the LangGraph workflow
        # It passes through: START → Indexer → Auditor → END
        # Returns the final state with all results
        final_state = app.invoke(initial_inputs)
        
        print("\n--- 2. WORKFLOW EXECUTION COMPLETE ---")
        
        # ========== STEP 4: OUTPUT RESULTS ========== 
        print("\n=== COMPLIANCE AUDIT REPORT ===")
        
        # .get() safely retrieves values (returns None if key doesn't exist)
        print(f"Video ID:    {final_state.get('video_id')}")
        
        # Shows PASS or FAIL status
        print(f"Status:      {final_state.get('final_status')}")
        
        # ========== VIOLATIONS SECTION ==========
        print("\n[ VIOLATIONS DETECTED ]")
        
        # Extract the list of compliance violations | Default to empty list if no results
        results = final_state.get('compliance_results', [])
        
        if results:
            for issue in results:
                # Each issue is a dict with: severity, category, description
                # Example output: "- [CRITICAL] Misleading Claims: Absolute guarantee detected"
                print(f"- [{issue.get('severity')}] {issue.get('category')}: {issue.get('description')}")
        else:
            # No violations found (clean video)
            print("No violations found.")

        # ========== SUMMARY SECTION ==========
        print("\n[ FINAL SUMMARY ]")
        # Displays the AI-generated natural language summary
        print(final_state.get('final_report'))

    except Exception as e:
        logger.error(f"Workflow Execution Failed: {str(e)}")
        raise e


if __name__ == "__main__":
    run_cli_simulation()  # Start the compliance audit simulation
