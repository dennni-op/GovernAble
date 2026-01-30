# AI Governance Policy Enforcement
# This module is the CORE of the governance system.
# It decides whether AI requests should be BLOCKED, REDACTED, or ALLOWED.

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from api.services.policies import Policy, evaluate_policy, EvalResult

router = APIRouter()

class EnforceRequest(BaseModel):
    """
    AI governance enforcement request.
    
    Typically called by the Governor Proxy (proxy/governor.ts)
    BEFORE forwarding prompts to external AI services.
    """
    text: str = Field(..., description="AI prompt to evaluate")
    policy: Policy = Field(..., description="Governance policy to apply")
    user_id: Optional[str] = Field(None, description="User making AI request (for auditing)")
    ai_service: Optional[str] = Field(None, description="Target AI service (openai, claude, etc.)")
    context: Optional[dict] = Field(None, description="Additional context (department, project, etc.)")

@router.post("/check", response_model=EvalResult)
async def enforce_ai_governance(payload: EnforceRequest):
    """
    Enforce AI governance policy on a prompt.
    
    This is the CRITICAL decision point:
    - BLOCK: Reject request, don't send to AI (high-risk data detected)
    - REDACT: Remove sensitive data, send cleaned version to AI
    - WARN: Allow but log warning for review
    - ALLOW: Safe to send to AI as-is
    
    Examples:
    
    1. BLOCK scenario:
       Input: "My AWS key: AKIAIOSFODNN7EXAMPLE"
       Output: {"action": "BLOCK", "reasons": ["AWS credentials detected"]}
    
    2. REDACT scenario:
       Input: "User john@company.com reported bug #1234"
       Output: {
           "action": "REDACT",
           "redacted_text": "User [REDACTED] reported bug #1234",
           "reasons": ["Email PII detected"]
       }
    
    3. ALLOW scenario:
       Input: "Explain how sorting algorithms work"
       Output: {"action": "ALLOW", "reasons": []}
    """
    result = evaluate_policy(
        text=payload.text,
        policy=payload.policy
    )
    
    # Audit log (for compliance)
    if result.action in ["BLOCK", "REDACT"]:
        await log_governance_event(
            action=result.action,
            user_id=payload.user_id,
            ai_service=payload.ai_service,
            reasons=result.reasons,
            text_hash=hash_text(payload.text)  # Don't log actual sensitive data!
        )
    
    return result

async def log_governance_event(action, user_id, ai_service, reasons, text_hash):
    """Log governance events for compliance auditing"""
    # Implementation: Save to database with timestamp
    pass

def hash_text(text: str) -> str:
    """Create hash of text for logging (don't log actual sensitive data)"""
    import hashlib
    return hashlib.sha256(text.encode()).hexdigest()[:16]