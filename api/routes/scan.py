# AI Prompt Scanning API
# This module provides endpoints for scanning AI prompts and conversations
# for sensitive data BEFORE they're sent to external AI services.

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import Optional
from engine.scanner import Scanner
from api.config import settings

router = APIRouter()

# Global scanner instance (loads detection rules once at startup)
scanner = Scanner()

class ScanTextRequest(BaseModel):
    """
    Request model for scanning AI prompts.
    
    Examples:
    - Scan a ChatGPT prompt before sending
    - Validate AI conversation history for PII
    - Check file contents before AI analysis
    """
    text: str = Field(..., description="AI prompt or text to scan for sensitive data")
    use_presidio: Optional[bool] = Field(True, description="Enable ML-based PII detection")
    context: Optional[str] = Field(None, description="Context (e.g., 'chatgpt-prompt', 'code-review')")

def api_key_auth(request: Request):
    """
    Authentication for AI governance API.
    
    In production, validate API keys to ensure only authorized
    applications can check prompts before sending to AI.
    """
    # TODO: Implement proper API key validation
    # api_key = request.headers.get("x-api-key")
    # if not api_key or api_key != settings.API_KEY:
    #     raise HTTPException(401, "Invalid API key")
    return True
@router.post("/text")
async def scan_ai_prompt(
    payload: ScanTextRequest, 
    ok: bool = Depends(api_key_auth)
):
    """
    Scan AI prompt for sensitive data.
    
@router.post("/file")
async def scan_file_for_ai_analysis(
    file: UploadFile = File(..., description="File to be analyzed by AI"), 
    use_presidio: bool = Form(True),
    ok: bool = Depends(api_key_auth)
):
    """
    Scan file contents before AI analysis.
    
    Common scenario: User uploads document for AI summarization/analysis.
    We scan it first to ensure no sensitive data is included.
    
    Example:
        curl -X POST http://localhost:8000/api/v1/scan/file \
          -F "file=@document.txt"
    """
    # Validate file
    if file.size > settings.MAX_SCAN_FILE_BYTES:
        raise HTTPException(400, f"File too large for AI processing. Max: {settings.MAX_SCAN_FILE_BYTES} bytes")

    if not file.filename:
        raise HTTPException(400, "Filename required")

    # Check allowed types for AI analysis
    allowed_types = [".txt", ".md", ".json", ".csv", ".py", ".js", ".yaml", ".yml"]
    if not any(file.filename.lower().endswith(t) for t in allowed_types):
        raise HTTPException(400, f"File type not supported for AI analysis. Allowed: {allowed_types}")
    
    try:
        contents = await file.read()
        text = contents.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(400, "File must be UTF-8 text for AI analysis")
    except Exception as e:
        raise HTTPException(500, f"Error reading file: {str(e)}")
    
    # Scan for sensitive data
    findings = scanner.scan_text(text)
    risk_score = calculate_risk_score(findings)
    
    return {
        "filename": file.filename,
        "size_bytes": file.size,
        "count": len(findings),
        "findings": [f.__dict__ for f in findings],
        "risk_score": risk_score,
        "safe_for_ai": risk_score < 40,  # Safe to send to AI?
        "recommendation": get_recommendation(risk_score)
    }

def calculate_risk_score(findings) -> int:
    """Calculate risk score 0-100 based on findings severity"""
    if not findings:
        return 0
    
    severity_weights = {"LOW": 10, "MEDIUM": 30, "HIGH": 50, "CRITICAL": 100}
    total_score = sum(severity_weights.get(f.severity, 30) for f in findings)
    return min(100, total_score)

def get_recommendation(risk_score: int) -> str:
    """Get AI governance recommendation based on risk"""
    if risk_score >= 80:
        return "BLOCK - High risk data detected"
    elif risk_score >= 40:
        return "REDACT - Remove sensitive data before sending to AI"
    else:
        return "ALLOW - Safe to send to AI"key_auth)):
    # Validation
    if file.size > settings.MAX_SCAN_FILE_BYTES:
        raise HTTPException(400, f"File too large. Max size is {settings.MAX_SCAN_FILE_BYTES} bytes.")

    if not file.filename:
        raise HTTPException(400, "No filename provided.")

    # Type checking
    allowed_types = [".txt", ".json", ".pdf", ".yml", ".yaml", ".csv", ".md"]
    if not any(file.filename.endswith(t) for t in allowed_types):
        raise HTTPException(400, f"File type not allowed. Allowed types: {allowed_types}")
    try:
        contents = await file.read()
        text = contents.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(400, "File is not a valid UTF-8 text file.")
    except Exception as e:
        raise HTTPException(500, f"Error reading file: {str(e)}")
    # It converts the file content (which is in bytes) into a string
    # It calls the scanner.
    findings = scanner.scan_text(text)
    # It returns the results.
    return {"filename": file.filename, "count": len(findings), "findings": [f.__dict__ for f in findings]}
