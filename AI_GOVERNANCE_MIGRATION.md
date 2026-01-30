# 🔄 Migration Guide: AI Usage Governance & Enforcement Engine

This document outlines all the changes needed to align your codebase with the **AI Usage Governance & Enforcement Engine** focus.

---

## 📋 Overview of Changes

Your current code is functional but the **comments, documentation, and naming** need to reflect the AI governance purpose. The core logic stays mostly the same, but the **context and terminology** shift to emphasize:

- **AI prompt interception** (not just file scanning)
- **Governance enforcement** (preventing data leaks to AI models)
- **Compliance auditing** (tracking AI usage)
- **Shadow AI prevention** (controlling which AI services are used)

---

## 📁 File-by-File Changes Required

### 1. ✏️ `README.md` - Project Documentation

**Current Focus:** Generic scanning platform  
**New Focus:** AI governance platform

```markdown
# GovernAble - AI Usage Governance & Enforcement Engine

**Prevent sensitive data leaks to AI models. Control and monitor organizational AI usage.**

GovernAble is an **AI governance platform** that sits between your users and external AI services (OpenAI, Claude, etc.), ensuring:

✅ **No Sensitive Data Leaks**: Automatically detects and blocks API keys, passwords, PII, and confidential information before they reach AI models
✅ **Policy Enforcement**: Define rules (BLOCK, REDACT, WARN) for what can be sent to AI services
✅ **Shadow AI Prevention**: Control which AI services employees can access
✅ **Compliance Auditing**: Complete audit trail of all AI interactions for regulatory requirements (SOC2, GDPR, HIPAA)
✅ **Real-time Monitoring**: Dashboard showing violations, trends, and user behavior

## 🎯 The Problem We Solve

**Scenario:** An employee uses ChatGPT to debug code:
```
"Help me fix this API connection: 
server: prod-db.company.com
username: admin
password: P@ssw0rd123
API_KEY: sk-1234567890abcdef"
```

**Without GovernAble:** ❌ All credentials are now in OpenAI's systems  
**With GovernAble:** ✅ Request is BLOCKED or credentials are REDACTED before reaching OpenAI

## 🏗️ Architecture

```
┌─────────────────┐
│  Employee Uses  │
│  ChatGPT / AI   │
└────────┬────────┘
         │ All AI requests intercepted
         ▼
┌─────────────────────────────┐
│   GovernAble AI Governor    │  ◄─── YOU ARE HERE
│   (Enforcement Proxy)       │
├─────────────────────────────┤
│ 1. Scan prompt for secrets  │
│ 2. Apply governance policy  │
│ 3. BLOCK / REDACT / ALLOW   │
│ 4. Log for compliance       │
└────────┬────────────────────┘
         │ Only safe requests forwarded
         ▼
┌─────────────────┐
│   OpenAI API    │
│   (External)    │
└─────────────────┘
```

## ✨ Features

### 🔓 Open Source Core
- **Prompt Scanning**: Detect secrets (API keys, passwords, tokens) and PII in AI prompts
- **Policy Engine**: BLOCK, REDACT, or WARN based on configurable rules
- **Multiple Detection Methods**: Regex patterns + ML-based detection (Presidio)
- **REST API**: Integrate governance checks into your apps
- **Audit Logging**: SQLite database of all AI interactions

### 💡 Pro (SaaS)
- **Governance Dashboard**: Visualize violations, trends, and user behavior
- **Team Policies**: Different rules for different departments
- **Webhook Alerts**: Real-time notifications (Slack, Teams, email)
- **Advanced Analytics**: Risk scoring, user behavior patterns

### 🏢 Enterprise
- **Shadow AI Governor Proxy**: Enforce governance on ALL AI traffic (transparent proxy)
- **SSO Integration**: Azure AD, Okta, SAML
- **Compliance Packs**: Pre-configured rules for GDPR, HIPAA, SOC2, ISO27001
- **Advanced Integrations**: SIEM (Splunk, ELK), Ticketing (Jira, ServiceNow)
- **Custom ML Models**: Train on your specific sensitive terms

## 🚀 Quick Start

### 1. Start the Governance System
```bash
# Clone repository
git clone https://github.com/your-org/GovernAble.git
cd GovernAble

# Start with Docker (recommended)
docker-compose up --build

# Or manually:
pip install -r requirements.txt
uvicorn api.main:app --reload &  # Enforcement API (port 8000)
cd proxy && npm install && npm start  # AI Governor Proxy (port 8787)
```

### 2. Configure Your AI Client to Use Governance Proxy
```python
# Instead of calling OpenAI directly:
# import openai
# openai.api_base = "https://api.openai.com/v1"

# Route through GovernAble:
import openai
openai.api_base = "http://localhost:8787/proxy/llm"  # Governance enforced!
```

### 3. Test the Governance
```bash
# Try to send sensitive data to AI (should be BLOCKED or REDACTED)
curl -X POST http://localhost:8787/proxy/llm \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Debug this: API_KEY=AKIAIOSFODNN7EXAMPLE",
    "model": "gpt-4"
  }'

# Response: {"error": "Blocked by AI governance policy", "reasons": ["AWS_ACCESS_KEY_ID detected"]}
```

### 4. View Governance Dashboard
Open http://localhost:3000 to see:
- Recent AI interactions
- Blocked requests
- Policy violations by user/department
- Compliance audit trail

## 📊 Use Cases

### 1. Developer Using AI for Coding
**Risk:** Accidentally sharing proprietary code, credentials, or internal APIs with external AI  
**Solution:** GovernAble detects and redacts sensitive information before it leaves your network

### 2. Customer Support Using AI
**Risk:** Sharing customer PII (emails, phone numbers, SSNs) with AI for response suggestions  
**Solution:** GDPR/HIPAA compliance by blocking PII in AI prompts

### 3. Shadow AI Prevention
**Risk:** Employees using unapproved AI services (ChatGPT free tier, random AI sites)  
**Solution:** Force all AI traffic through approved, governed channels

### 4. Compliance & Auditing
**Risk:** No visibility into what data employees share with AI vendors  
**Solution:** Complete audit trail for SOC2, ISO27001 compliance

## 🛡️ Security Model

**Zero Trust Approach:**
1. **Assume all AI services are untrusted** (even OpenAI, Google, etc.)
2. **Never send sensitive data** to external services
3. **Log everything** for forensics and compliance
4. **Enforce at the network level** (users can't bypass)

## 📚 Documentation
- **[Junior Developer Guide](./JUNIOR_DEV_GUIDE.md)**: Complete learning resource
- **[API Documentation](http://localhost:8000/docs)**: Interactive API docs (Swagger)
- **[Policy Configuration](./docs/policies.md)**: How to define governance rules
- **[Deployment Guide](./docs/deployment.md)**: Production deployment

## 🤝 Contributing
See [CONTRIBUTING.md](./CONTRIBUTING.md)

## 📜 License
- **Open Source Core** (engine/ & api/): AGPL v3
- **Enterprise Features** (proxy/, web/): Commercial License

## 🆘 Support
- **Community**: GitHub Discussions
- **Enterprise**: enterprise@governable.ai
- **Security Issues**: security@governable.ai (GPG key available)
```

---

### 2. ✏️ `api/routes/scan.py` - Scanning Endpoints

**Changes:** Update comments to reflect AI prompt scanning

```python
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
    
    Use this endpoint BEFORE sending text to any AI service (OpenAI, Claude, etc.)
    to detect:
    - API keys and credentials
    - Personal Identifiable Information (PII)
    - Confidential company data
    - Internal URLs and endpoints
    
    Returns:
        count: Number of findings
        findings: List of detected sensitive data
        risk_score: Overall risk level (0-100)
    """
    findings = scanner.scan_text(payload.text)
    
    # Calculate risk score based on findings
    risk_score = calculate_risk_score(findings)
    
    return {
        "count": len(findings),
        "findings": [f.__dict__ for f in findings],
        "risk_score": risk_score,
        "recommendation": "BLOCK" if risk_score > 80 else "REDACT" if risk_score > 40 else "ALLOW"
    }

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

@router.post("/conversation")
async def scan_ai_conversation(
    messages: list[dict],
    ok: bool = Depends(api_key_auth)
):
    """
    Scan entire AI conversation history.
    
    Use this to validate chat histories before:
    - Sending conversation context to AI
    - Sharing chat logs with team members
    - Exporting conversations for training
    
    Request body:
    {
        "messages": [
            {"role": "user", "content": "My API key is..."},
            {"role": "assistant", "content": "..."},
            {"role": "user", "content": "..."}
        ]
    }
    """
    all_findings = []
    
    for idx, msg in enumerate(messages):
        findings = scanner.scan_text(msg.get("content", ""))
        for f in findings:
            f.context = f"Message {idx+1} ({msg['role']}): {f.context}"
        all_findings.extend(findings)
    
    risk_score = calculate_risk_score(all_findings)
    
    return {
        "messages_scanned": len(messages),
        "total_findings": len(all_findings),
        "findings_by_message": group_findings_by_message(all_findings),
        "risk_score": risk_score,
        "safe_to_share": risk_score < 40
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
        return "ALLOW - Safe to send to AI"

def group_findings_by_message(findings):
    """Group findings by message for conversation scanning"""
    # Implementation details...
    pass
```

---

### 3. ✏️ `api/routes/enforce.py` - Policy Enforcement

**Changes:** Emphasize AI governance context

```python
# AI Governance Policy Enforcement
# This module is the CORE of the governance system.
# It decides whether AI requests should be BLOCKED, REDACTED, or ALLOWED.

from fastapi import APIRouter, HTTPException
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

@router.post("/batch")
async def enforce_batch(requests: list[EnforceRequest]):
    """
    Enforce policies on multiple prompts at once.
    
    Useful for:
    - Validating conversation history before continuing
    - Bulk scanning of AI interaction logs
    - Pre-validating multiple prompt variations
    """
    results = []
    for req in requests:
        result = evaluate_policy(req.text, req.policy)
        results.append({
            "text_preview": req.text[:50] + "..." if len(req.text) > 50 else req.text,
            "action": result.action,
            "risk_level": calculate_risk_level(result)
        })
    
    return {
        "total": len(results),
        "blocked": sum(1 for r in results if r["action"] == "BLOCK"),
        "redacted": sum(1 for r in results if r["action"] == "REDACT"),
        "allowed": sum(1 for r in results if r["action"] == "ALLOW"),
        "results": results
    }

@router.get("/policies")
async def list_available_policies():
    """
    Get list of available AI governance policies.
    
    Examples:
    - "strict": BLOCK any sensitive data
    - "redact-pii": REDACT personal information, allow everything else
    - "log-only": WARN on sensitive data but allow (for training/testing)
    """
    return {
        "policies": [
            {
                "name": "strict",
                "mode": "BLOCK",
                "description": "Block any prompt with sensitive data",
                "use_cases": ["Production AI usage", "Customer-facing AI"]
            },
            {
                "name": "redact-pii",
                "mode": "REDACT",
                "description": "Remove PII, allow other content",
                "use_cases": ["Internal AI tools", "Development environments"]
            },
            {
                "name": "log-only",
                "mode": "WARN",
                "description": "Allow everything but log violations",
                "use_cases": ["Testing", "Training period"]
            }
        ]
    }

async def log_governance_event(action, user_id, ai_service, reasons, text_hash):
    """Log governance events for compliance auditing"""
    # Implementation: Save to database with timestamp
    pass

def calculate_risk_level(result: EvalResult) -> str:
    """Calculate risk level: LOW, MEDIUM, HIGH, CRITICAL"""
    if result.action == "BLOCK":
        return "CRITICAL"
    elif result.action == "REDACT":
        return "HIGH" if len(result.reasons) > 2 else "MEDIUM"
    else:
        return "LOW"

def hash_text(text: str) -> str:
    """Create hash of text for logging (don't log actual sensitive data)"""
    import hashlib
    return hashlib.sha256(text.encode()).hexdigest()[:16]
```

---

### 4. ✏️ `proxy/governor.ts` - AI Governor Proxy

**Changes:** Better comments emphasizing the "Shadow AI Governor" role

```typescript
/**
 * GovernAble AI Governor Proxy
 * 
 * This is the ENFORCEMENT LAYER that sits between users and AI services.
 * 
 * Purpose: Prevent sensitive data leaks to external AI models
 * 
 * How it works:
 * 1. Intercepts ALL AI requests (OpenAI, Claude, etc.)
 * 2. Scans prompts for sensitive data using enforcement API
 * 3. Applies governance policy (BLOCK / REDACT / ALLOW)
 * 4. Only forwards SAFE prompts to AI services
 * 5. Logs everything for compliance auditing
 * 
 * Deployment:
 * - Transparent proxy: Users point AI clients here instead of api.openai.com
 * - Network enforcement: Can be deployed at network edge (all AI traffic flows through)
 * - No client changes needed: Works with existing OpenAI SDKs
 */

import express from "express";
import bodyParser from "body-parser";
import axios from "axios";
import dotenv from "dotenv";
import winston from "winston";

dotenv.config();

const app = express();
app.use(bodyParser.json({ limit: "1mb" }));

// Configure logging for audit trail
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'ai-governance.log' }),
    new winston.transports.Console()
  ]
});

// --- Configuration ---
const API_BASE = process.env.API_BASE || "http://localhost:8000";
const LLM_TARGET = process.env.LLM_TARGET || "https://api.openai.com";
const GOVERNANCE_POLICY = process.env.GOVERNANCE_POLICY || "strict";

/**
 * Enforce AI governance policy on text
 * 
 * Calls the Python enforcement API to check if prompt is safe
 * 
 * @param text - The AI prompt to validate
 * @param userId - User making the request (for auditing)
 * @returns Decision object: { action: "BLOCK" | "REDACT" | "ALLOW", redacted_text?, reasons }
 */
async function enforceGovernancePolicy(
  text: string, 
  userId?: string
): Promise<any> {
  try {
    logger.info({
      event: "governance_check_started",
      userId,
      promptLength: text.length,
      timestamp: new Date().toISOString()
    });

    const resp = await axios.post(`${API_BASE}/api/v1/enforce/check`, {
      text: text,
      policy: { 
        name: GOVERNANCE_POLICY, 
        mode: "BLOCK",  // Default to strict for security
        rules: [] 
      },
      user_id: userId,
      ai_service: "openai"
    });

    logger.info({
      event: "governance_check_completed",
      action: resp.data.action,
      userId
    });

    return resp.data;
  } catch (e: any) {
    // FAIL SECURE: If governance API is down, BLOCK the request
    logger.error({
      event: "governance_check_failed",
      error: e.message,
      userId
    });
    
    return { 
      action: "BLOCK", 
      reasons: ["Governance service unavailable - failing secure"] 
    };
  }
}

/**
 * Main AI Governance Endpoint
 * 
 * This endpoint receives AI requests and enforces governance BEFORE
 * forwarding to the actual AI service.
 * 
 * Setup: Point your AI client here instead of api.openai.com
 * Example: openai.api_base = "http://localhost:8787/proxy/llm"
 */
app.post("/proxy/llm", async (req, res) => {
  const startTime = Date.now();
  const userId = req.headers["x-user-id"] as string || "anonymous";
  
  // Extract AI prompt from request
  const prompt = req.body.prompt || req.body.messages?.[req.body.messages.length - 1]?.content || "";
  
  if (!prompt) {
    return res.status(400).json({ error: "No prompt provided" });
  }

  logger.info({
    event: "ai_request_received",
    userId,
    promptLength: prompt.length,
    model: req.body.model,
    timestamp: new Date().toISOString()
  });

  // STEP 1: Enforce governance policy
  const decision = await enforceGovernancePolicy(prompt, userId);

  // STEP 2: Handle BLOCK decision
  if (decision.action === "BLOCK") {
    logger.warn({
      event: "ai_request_blocked",
      userId,
      reasons: decision.reasons,
      promptHash: hashString(prompt).substring(0, 16)
    });

    return res.status(403).json({
      error: "⛔ Request blocked by AI governance policy",
      reasons: decision.reasons,
      message: "Your prompt contains sensitive data that cannot be sent to external AI services.",
      remediation: "Remove sensitive information (credentials, PII, confidential data) and try again.",
      support: "Contact security@yourcompany.com if you believe this is an error"
    });
  }

  // STEP 3: Handle REDACT decision
  let finalPrompt = prompt;
  if (decision.action === "REDACT") {
    finalPrompt = decision.redacted_text || prompt;
    
    logger.info({
      event: "ai_request_redacted",
      userId,
      redactedCount: decision.reasons.length,
      reasons: decision.reasons
    });
  }

  // STEP 4: Forward to actual AI service (only if ALLOWED or REDACTED)
  try {
    logger.info({
      event: "forwarding_to_ai_service",
      userId,
      service: "openai",
      model: req.body.model
    });

    const upstreamResponse = await axios.post(
      `${LLM_TARGET}/v1/chat/completions`,
      {
        model: req.body.model || "gpt-4",
        messages: [
          { role: "user", content: finalPrompt }
        ],
        ...req.body  // Pass through other parameters
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );

    const duration = Date.now() - startTime;

    logger.info({
      event: "ai_request_completed",
      userId,
      duration_ms: duration,
      governance_action: decision.action,
      success: true
    });

    // Return AI response + governance info
    res.json({
      ...upstreamResponse.data,
      governance: {
        action: decision.action,
        was_redacted: decision.action === "REDACT",
        redacted_items: decision.action === "REDACT" ? decision.reasons : []
      }
    });

  } catch (err: any) {
    logger.error({
      event: "ai_service_error",
      userId,
      error: err.message,
      status: err.response?.status
    });

    res.status(502).json({
      error: "AI service error",
      details: err.message,
      governance_action: decision.action
    });
  }
});

/**
 * Health check endpoint
 */
app.get("/health", async (req, res) => {
  // Check if enforcement API is reachable
  try {
    await axios.get(`${API_BASE}/health`);
    res.json({ 
      status: "healthy",
      governance_api: "connected",
      ai_service: LLM_TARGET
    });
  } catch (e) {
    res.status(503).json({ 
      status: "degraded",
      governance_api: "disconnected",
      message: "Governance enforcement unavailable - all requests will be BLOCKED"
    });
  }
});

/**
 * Governance statistics endpoint
 */
app.get("/stats", async (req, res) => {
  // Return statistics about blocked/allowed requests
  res.json({
    total_requests: 0,  // TODO: Implement metrics
    blocked: 0,
    redacted: 0,
    allowed: 0,
    top_violations: []
  });
});

// Helper function
function hashString(str: string): string {
  const crypto = require('crypto');
  return crypto.createHash('sha256').update(str).digest('hex');
}

// Start the AI Governor
const PORT = process.env.PORT || 8787;
app.listen(PORT, () => {
  logger.info({
    event: "governor_started",
    port: PORT,
    enforcement_api: API_BASE,
    ai_service: LLM_TARGET,
    policy: GOVERNANCE_POLICY,
    message: "🛡️  AI Governor Proxy is running - All AI traffic will be governed"
  });
  console.log(`\n🛡️  GovernAble AI Governor running on port ${PORT}`);
  console.log(`📋 Enforcement API: ${API_BASE}`);
  console.log(`🤖 AI Service: ${LLM_TARGET}`);
  console.log(`🔒 Policy: ${GOVERNANCE_POLICY}\n`);
});
```

---

### 5. ✏️ `web/frontend/src/App.tsx` - Dashboard

**Changes:** Rename to "AI Governance Dashboard"

```typescript
/**
 * GovernAble AI Governance Dashboard
 * 
 * Shows:
 * - Recent AI interactions (allowed, blocked, redacted)
 * - Policy violations by user/department
 * - Compliance audit trail
 * - Trends and risk analytics
 */

import React, { useEffect, useState } from "react";
import "./App.css";

type AIInteraction = {
  id: number;
  user_id: string;
  timestamp: string;
  action: "ALLOW" | "BLOCK" | "REDACT";
  ai_service: string;
  findings_count: number;
  risk_score: number;
  prompt_preview: string;
};

function App() {
  const [interactions, setInteractions] = useState<AIInteraction[]>([]);
  const [stats, setStats] = useState({
    total: 0,
    blocked: 0,
    redacted: 0,
    allowed: 0
  });

  useEffect(() => {
    // Fetch AI governance interactions
    fetch("http://localhost:8000/api/v1/governance/interactions")
      .then(r => r.json())
      .then(data => {
        setInteractions(data.interactions || []);
        setStats(data.stats || stats);
      })
      .catch(console.error);
  }, []);

  const getActionBadge = (action: string) => {
    const styles = {
      BLOCK: { bg: "#fee", color: "#c00", label: "🚫 BLOCKED" },
      REDACT: { bg: "#ffc", color: "#860", label: "🧹 REDACTED" },
      ALLOW: { bg: "#efe", color: "#060", label: "✅ ALLOWED" }
    };
    const style = styles[action as keyof typeof styles] || styles.ALLOW;
    return (
      <span style={{
        background: style.bg,
        color: style.color,
        padding: "4px 8px",
        borderRadius: "4px",
        fontWeight: "bold"
      }}>
        {style.label}
      </span>
    );
  };

  return (
    <div className="App">
      <header style={{ background: "#1a1a1a", color: "#fff", padding: "20px" }}>
        <h1>🛡️ GovernAble - AI Governance Dashboard</h1>
        <p>Monitoring AI usage and enforcing security policies</p>
      </header>

      {/* Statistics */}
      <div style={{ display: "flex", gap: "20px", padding: "20px" }}>
        <StatCard title="Total Requests" value={stats.total} color="#333" />
        <StatCard title="Blocked" value={stats.blocked} color="#c00" />
        <StatCard title="Redacted" value={stats.redacted} color="#f80" />
        <StatCard title="Allowed" value={stats.allowed} color="#0a0" />
      </div>

      {/* Recent AI Interactions */}
      <div style={{ padding: "20px" }}>
        <h2>Recent AI Interactions</h2>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#f5f5f5", textAlign: "left" }}>
              <th style={{ padding: "10px" }}>Time</th>
              <th style={{ padding: "10px" }}>User</th>
              <th style={{ padding: "10px" }}>AI Service</th>
              <th style={{ padding: "10px" }}>Action</th>
              <th style={{ padding: "10px" }}>Risk Score</th>
              <th style={{ padding: "10px" }}>Prompt Preview</th>
            </tr>
          </thead>
          <tbody>
            {interactions.length === 0 ? (
              <tr>
                <td colSpan={6} style={{ padding: "20px", textAlign: "center", color: "#999" }}>
                  No AI interactions yet. Try sending a request through the Governor Proxy.
                </td>
              </tr>
            ) : (
              interactions.map(interaction => (
                <tr key={interaction.id} style={{ borderBottom: "1px solid #eee" }}>
                  <td style={{ padding: "10px" }}>
                    {new Date(interaction.timestamp).toLocaleString()}
                  </td>
                  <td style={{ padding: "10px" }}>{interaction.user_id}</td>
                  <td style={{ padding: "10px" }}>{interaction.ai_service}</td>
                  <td style={{ padding: "10px" }}>{getActionBadge(interaction.action)}</td>
                  <td style={{ padding: "10px" }}>
                    <RiskScoreBadge score={interaction.risk_score} />
                  </td>
                  <td style={{ padding: "10px", maxWidth: "300px", overflow: "hidden", textOverflow: "ellipsis" }}>
                    {interaction.prompt_preview}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Compliance Export */}
      <div style={{ padding: "20px" }}>
        <button onClick={() => window.location.href = '/api/v1/governance/export?format=csv'}>
          📊 Export Compliance Report (CSV)
        </button>
      </div>
    </div>
  );
}

function StatCard({ title, value, color }: { title: string; value: number; color: string }) {
  return (
    <div style={{
      flex: 1,
      padding: "20px",
      background: "#fff",
      border: `2px solid ${color}`,
      borderRadius: "8px",
      textAlign: "center"
    }}>
      <h3 style={{ margin: 0, color: color }}>{value}</h3>
      <p style={{ margin: "5px 0 0", color: "#666" }}>{title}</p>
    </div>
  );
}

function RiskScoreBadge({ score }: { score: number }) {
  const color = score >= 80 ? "#c00" : score >= 40 ? "#f80" : "#0a0";
  return (
    <span style={{
      background: color,
      color: "#fff",
      padding: "4px 8px",
      borderRadius: "4px",
      fontWeight: "bold"
    }}>
      {score}
    </span>
  );
}

export default App;
```

---

### 6. ✏️ `api/config.py` - Add AI Governance Settings

**Changes:** Add governance-specific configuration

```python
# api/config.py
from pydantic import BaseSettings, Field
from typing import Literal

class Settings(BaseSettings):
    # --- Project Info ---
    PROJECT_NAME: str = "GovernAble AI Governance Engine"
    API_V1_STR: str = "/api/v1"
    ENV: Literal["development", "staging", "production"] = Field("development", env="ENV")
    
    # --- Security & Authentication ---
    API_KEY: str = Field("dev_key", env="GA_API_KEY")
    CORS_ORIGINS: str = Field("*", env="CORS_ORIGINS")
    
    # --- AI Governance Settings ---
    DEFAULT_GOVERNANCE_POLICY: Literal["strict", "redact", "warn"] = Field(
        "strict", 
        env="DEFAULT_POLICY",
        description="Default policy for AI governance: strict=BLOCK, redact=REDACT, warn=WARN"
    )
    
    ALLOWED_AI_SERVICES: str = Field(
        "openai,anthropic", 
        env="ALLOWED_AI_SERVICES",
        description="Comma-separated list of approved AI services"
    )
    
    # --- Database ---
    DATABASE_URL: str = Field("sqlite+aiosqlite:///./governable.db", env="DATABASE_URL")
    
    # --- Scanning Limits ---
    MAX_SCAN_FILE_BYTES: int = Field(5_000_000, env="MAX_SCAN_FILE_BYTES")
    MAX_PROMPT_LENGTH: int = Field(100_000, env="MAX_PROMPT_LENGTH", description="Max AI prompt length")
    
    # --- Audit & Compliance ---
    ENABLE_AUDIT_LOGGING: bool = Field(True, env="ENABLE_AUDIT_LOGGING")
    AUDIT_LOG_RETENTION_DAYS: int = Field(90, env="AUDIT_LOG_RETENTION_DAYS")
    
    # --- Alerts & Notifications ---
    SLACK_WEBHOOK_URL: str = Field("", env="SLACK_WEBHOOK_URL")
    ALERT_ON_BLOCKED_REQUESTS: bool = Field(True, env="ALERT_ON_BLOCKED")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    def is_ai_service_allowed(self, service: str) -> bool:
        """Check if AI service is in the allowlist"""
        allowed = [s.strip().lower() for s in self.ALLOWED_AI_SERVICES.split(",")]
        return service.lower() in allowed

settings = Settings()
```

---

### 7. ✏️ `.env.example` - Environment Variables Template

**New file** to document configuration:

```bash
# GovernAble AI Governance Engine Configuration

# Environment
ENV=development  # development | staging | production

# API Security
GA_API_KEY=your_secret_api_key_here

# AI Governance Policy
DEFAULT_POLICY=strict  # strict (BLOCK) | redact (REDACT) | warn (WARN)
ALLOWED_AI_SERVICES=openai,anthropic,cohere  # Comma-separated approved AI services

# Database
DATABASE_URL=sqlite+aiosqlite:///./governable.db
# Production: postgresql+asyncpg://user:pass@host:5432/governable

# Scanning Limits
MAX_SCAN_FILE_BYTES=5000000  # 5MB
MAX_PROMPT_LENGTH=100000     # 100KB

# Audit & Compliance
ENABLE_AUDIT_LOGGING=true
AUDIT_LOG_RETENTION_DAYS=90  # Keep logs for 90 days

# External AI Services
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Proxy Configuration
API_BASE=http://localhost:8000
LLM_TARGET=https://api.openai.com
GOVERNANCE_POLICY=strict

# Alerts (optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
ALERT_ON_BLOCKED=true  # Send alert when requests are blocked

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8787
```

---

## 📊 Summary of Changes

| File | Change Type | Description |
|------|-------------|-------------|
| `README.md` | **Major rewrite** | Emphasize AI governance, show architecture, use cases |
| `api/routes/scan.py` | **Comments + functions** | Rename functions, add AI context, risk scoring |
| `api/routes/enforce.py` | **Comments + endpoints** | Better governance terminology, audit logging |
| `api/services/policies.py` | **Comments** | Emphasize governance policy engine role |
| `engine/scanner.py` | **Comments** | Emphasize AI prompt scanning |
| `proxy/governor.ts` | **Major refactor** | Complete rewrite with logging, better error handling |
| `web/frontend/src/App.tsx` | **UI redesign** | "AI Governance Dashboard" with compliance focus |
| `api/config.py` | **New settings** | Add governance-specific configuration |
| `.env.example` | **New file** | Document all configuration options |
| `docker-compose.yml` | **Service descriptions** | Update descriptions to emphasize governance |

---

## ✅ Implementation Checklist

- [ ] Update `README.md` with AI governance focus
- [ ] Add comments to `api/routes/scan.py` explaining AI prompt scanning
- [ ] Enhance `api/routes/enforce.py` with governance terminology
- [ ] Refactor `proxy/governor.ts` with logging and better error messages
- [ ] Update `web/frontend/src/App.tsx` to show "AI Governance Dashboard"
- [ ] Add AI governance settings to `api/config.py`
- [ ] Create `.env.example` with all configuration options
- [ ] Add governance-focused tests in `tests/`
- [ ] Create `docs/` folder with:
  - `docs/policies.md` - How to configure governance policies
  - `docs/deployment.md` - Production deployment guide
  - `docs/compliance.md` - Audit and compliance features
- [ ] Update Docker container labels/descriptions

---

## 🎯 Key Messaging Changes

### Before (Generic Scanning)
- "Scan files for secrets"
- "Detect PII in text"
- "Find API keys"

### After (AI Governance)
- "Prevent data leaks to AI models"
- "Enforce governance on AI prompts"
- "Control organizational AI usage"
- "Ensure compliance with security policies"
- "Block Shadow AI"

---

## 🚀 Next Steps

1. **Start with README.md** - This is what users see first
2. **Update proxy/governor.ts** - Core enforcement component
3. **Enhance API comments** - Help developers understand the purpose
4. **Build governance dashboard** - Visualize AI interactions
5. **Add audit logging** - Track everything for compliance
6. **Create documentation** - Deployment, policies, compliance guides

---

## 💻 Performance & Resource Optimization for Low-End Laptops

**Running GovernAble on low-spec hardware?** Here are optimization strategies to reduce CPU, RAM, and disk usage while maintaining functionality.

### 📊 Resource Requirements

**Minimum specs:**
- **CPU**: 2 cores (Intel i3 or equivalent)
- **RAM**: 4GB (6GB recommended)
- **Storage**: 5GB free space
- **OS**: Windows 10/11, Linux, macOS

**What uses the most resources:**
1. **Python API (FastAPI + Presidio)**: 300-500MB RAM, moderate CPU
2. **TypeScript Proxy (Node.js)**: 150-250MB RAM, low CPU
3. **React Dashboard**: 100-200MB RAM (when running dev server)
4. **Database**: 50-100MB RAM for SQLite, more for PostgreSQL

### 🔧 Optimization Strategy 1: Disable Heavy Components

**For development on low-end laptops, you can run in "lightweight mode":**

#### Option A: API Only (No Proxy, No Dashboard)
```powershell
# Just run the enforcement API
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000

# Test with curl/Postman - no frontend needed
curl -X POST http://localhost:8000/api/v1/scan/text `
  -H "Content-Type: application/json" `
  -d '{"text":"Test prompt with API key AKIAIOSFODNN7"}'
```

**Resources saved:** ~400MB RAM, 1 CPU core

#### Option B: Disable Presidio (ML-based PII Detection)
```python
# In api/config.py, add:
USE_PRESIDIO: bool = Field(False, env="USE_PRESIDIO")

# In engine/scanner.py:
class Scanner:
    def __init__(self, patterns: Optional[Dict] = None, use_presidio: bool = False):
        # Default to False instead of True
        self.use_presidio = use_presidio and settings.USE_PRESIDIO
```

**Resources saved:** ~200-300MB RAM (Presidio loads ML models)

#### Option C: Use SQLite Instead of PostgreSQL
```bash
# In .env file:
DATABASE_URL=sqlite+aiosqlite:///./governable.db

# NOT:
# DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/governable
```

**Resources saved:** ~100-200MB RAM (no PostgreSQL process)

### 🚀 Optimization Strategy 2: Reduce Docker Overhead

**If using Docker Compose, limit resource usage:**

Update `docker-compose.yml`:
```yaml
version: '3.8'

services:
  api:
    build: .
    # Limit CPU and memory
    deploy:
      resources:
        limits:
          cpus: '1.0'      # Max 1 CPU core
          memory: 512M     # Max 512MB RAM
        reservations:
          cpus: '0.5'      # Guaranteed 0.5 CPU
          memory: 256M     # Guaranteed 256MB RAM
    environment:
      - USE_PRESIDIO=false  # Disable heavy ML
      - WORKERS=1           # Single worker process

  proxy:
    build: ./proxy
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
```

**Alternative: Skip Docker entirely**
```powershell
# Run natively (uses less RAM than Docker)
# Terminal 1: Python API
.\venv\Scripts\Activate.ps1
uvicorn api.main:app --reload --workers 1

# Terminal 2: TypeScript Proxy (optional)
cd proxy
npm start
```

### ⚡ Optimization Strategy 3: Reduce Python Worker Processes

**By default, Uvicorn might spawn multiple workers. For low-end laptops:**

```powershell
# Single worker (less RAM, but slower under load)
uvicorn api.main:app --reload --workers 1 --limit-concurrency 10

# Production mode (no auto-reload = less CPU)
uvicorn api.main:app --workers 1 --host 0.0.0.0 --port 8000
```

**Trade-off:**
- ✅ **Saves**: 200-300MB RAM per worker
- ❌ **Cost**: Can only handle 1 request at a time

### 🗃️ Optimization Strategy 4: Database Tuning

#### SQLite Optimizations
```python
# In api/services/storage.py
from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Optimize SQLite for low memory"""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")      # Write-Ahead Logging (faster)
    cursor.execute("PRAGMA synchronous=NORMAL")    # Balance safety/speed
    cursor.execute("PRAGMA cache_size=-32000")     # 32MB cache (reduce if needed)
    cursor.execute("PRAGMA temp_store=MEMORY")     # Use RAM for temp tables
    cursor.close()
```

#### Limit Query Results
```python
# In api/routes/scan.py
@router.get("/results")
async def get_scan_results(limit: int = 10, skip: int = 0):
    """Always paginate - never return all results"""
    if limit > 100:
        limit = 100  # Cap at 100 to prevent memory issues
    
    async with AsyncSessionLocal() as session:
        stmt = select(ScanResult).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()
```

### 📝 Optimization Strategy 5: Logging & File I/O

**Excessive logging can slow down low-end systems:**

```python
# In api/config.py
LOG_LEVEL: str = Field("WARNING", env="LOG_LEVEL")  # INFO, DEBUG, WARNING, ERROR

# In api/main.py
import logging

if settings.LOG_LEVEL == "WARNING":
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.INFO)
```

**For proxy/governor.ts:**
```typescript
// Disable winston file logging on low-end systems
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'error',  // Only log errors
  transports: [
    // Comment out file transport to reduce disk I/O
    // new winston.transports.File({ filename: 'ai-governance.log' }),
    new winston.transports.Console({ 
      format: winston.format.simple()  // Simple format = faster
    })
  ]
});
```

### 🧪 Optimization Strategy 6: Reduce Frontend Resource Usage

**React dev server can be heavy. Alternatives:**

#### Option A: Build for Production (Faster)
```powershell
cd web/frontend
npm run build

# Serve static files (much lighter than dev server)
npx serve -s build -p 3000
```

**Resources saved:** ~150MB RAM, less CPU usage

#### Option B: Skip Frontend Entirely
```powershell
# Use API documentation UI instead
# Open http://localhost:8000/docs

# Or use curl/Postman for testing
```

### 🔍 Optimization Strategy 7: Monitor Resource Usage

**Track what's using resources:**

#### Windows PowerShell
```powershell
# Check memory usage
Get-Process python | Select-Object Name, CPU, WorkingSet
Get-Process node | Select-Object Name, CPU, WorkingSet

# Continuous monitoring
while ($true) {
    Clear-Host
    Get-Process python,node | Format-Table Name, 
        @{Label="CPU(%)";Expression={$_.CPU}}, 
        @{Label="RAM(MB)";Expression={[math]::Round($_.WorkingSet/1MB,2)}}
    Start-Sleep -Seconds 2
}
```

#### Linux/Mac
```bash
# Monitor with htop (install: sudo apt install htop)
htop

# Or use ps
watch -n 2 'ps aux | grep -E "python|node" | grep -v grep'
```

### 📊 Optimization Results: Expected Performance

| Configuration | RAM Usage | CPU Usage | Startup Time |
|---------------|-----------|-----------|--------------|
| **Full Stack (All services)** | ~1.2GB | High | 15-20s |
| **API Only** | ~400MB | Medium | 5-8s |
| **API without Presidio** | ~200MB | Low | 3-5s |
| **Minimal (API + SQLite, no logs)** | ~150MB | Very Low | 2-3s |

### 🎯 Recommended Setup for Low-End Laptops

**For daily development:**
```powershell
# 1. Disable Presidio
# In .env:
USE_PRESIDIO=false

# 2. Run API only (no proxy, no frontend)
uvicorn api.main:app --reload --workers 1 --port 8000

# 3. Test with FastAPI docs
# Open http://localhost:8000/docs
```

**When you need to test the full stack:**
```powershell
# 1. Build frontend once
cd web/frontend
npm run build

# 2. Run API + Proxy (skip dashboard dev server)
# Terminal 1:
uvicorn api.main:app --workers 1 --port 8000

# Terminal 2:
cd proxy
npm start

# 3. Serve built frontend
cd web/frontend
npx serve -s build -p 3000
```

### 🛠️ Troubleshooting Low-End Performance

**Problem: "Python process using too much RAM"**
```powershell
# Solution 1: Disable Presidio
# Set USE_PRESIDIO=false in .env

# Solution 2: Reduce worker count
uvicorn api.main:app --workers 1

# Solution 3: Add garbage collection
# In api/main.py:
import gc
@app.middleware("http")
async def cleanup_middleware(request, call_next):
    response = await call_next(request)
    gc.collect()  # Force garbage collection
    return response
```

**Problem: "Node.js proxy using too much RAM"**
```powershell
# Solution: Limit Node.js heap size
$env:NODE_OPTIONS="--max-old-space-size=256"  # Limit to 256MB
npm start
```

**Problem: "System freezes when running all services"**
```powershell
# Solution: Run services one at a time
# 1. Start API, wait for it to be ready
uvicorn api.main:app --reload --port 8000

# 2. Wait 10 seconds, then start proxy
Start-Sleep -Seconds 10
cd proxy; npm start

# 3. Skip dashboard or build it statically
```

**Problem: "SQLite database locked errors"**
```powershell
# Solution: Enable WAL mode (see Database Tuning above)
# Or delete and recreate database:
Remove-Item governable.db
python -c "import asyncio; from api.services.storage import init_db; asyncio.run(init_db())"
```

### 💡 Pro Tips for Low-End Development

1. **Close other applications**: Browser tabs, IDE extensions, background apps
2. **Use lightweight IDE**: VS Code with minimal extensions, or Notepad++/Vim
3. **Disable antivirus scanning**: Add project folder to exclusions (be careful!)
4. **Use SSD if possible**: Much faster than HDD for database operations
5. **Clean temp files regularly**: `python -m pip cache purge`
6. **Consider Linux**: Often uses less RAM than Windows for development

---

## 📚 Learning Resources & Further Reading

### 🎓 Beginner-Friendly Tutorials

#### FastAPI
- **Official Tutorial**: https://fastapi.tiangolo.com/tutorial/
  - ⭐ Best place to start, very beginner-friendly
  - Covers routing, request handling, validation
- **Video Course**: [FastAPI - The Complete Course (YouTube)](https://www.youtube.com/watch?v=tLKKmouUams)
  - 7+ hours of hands-on coding
- **Interactive Course**: [Test-Driven Development with FastAPI and Docker](https://testdriven.io/courses/tdd-fastapi/)

#### Pydantic
- **Official Docs**: https://docs.pydantic.dev/latest/
  - Start with "Why Use Pydantic?" section
- **Tutorial**: [Pydantic is All You Need](https://www.youtube.com/watch?v=Vj-iU-8_xLs)
  - 30-minute video, covers all basics

#### TypeScript/Node.js
- **TypeScript Handbook**: https://www.typescriptlang.org/docs/handbook/intro.html
  - Official guide, very comprehensive
- **Node.js Express Tutorial**: https://expressjs.com/en/starter/hello-world.html
  - Learn Express in 30 minutes
- **Proxy Pattern**: [Understanding Reverse Proxies](https://www.cloudflare.com/learning/cdn/glossary/reverse-proxy/)

#### React
- **Official Tutorial**: https://react.dev/learn
  - Interactive, builds a tic-tac-toe game
- **React Hooks**: https://react.dev/reference/react
  - Deep dive into useState, useEffect, etc.
- **Video**: [React Course for Beginners](https://www.youtube.com/watch?v=bMknfKXIFA8)
  - 12 hours, but you can skip to relevant sections

### 🔐 AI Governance & Security

#### AI Security
- **OWASP Top 10 for LLMs**: https://owasp.org/www-project-top-10-for-large-language-model-applications/
  - ⭐ Essential reading for AI security
  - Covers prompt injection, data leakage, etc.
- **NIST AI Risk Management**: https://www.nist.gov/itl/ai-risk-management-framework
  - Government framework for AI governance
- **Article**: ["Shadow AI: The Hidden Threat"](https://www.microsoft.com/en-us/security/blog/2023/12/07/shadow-ai/)

#### Data Protection & PII Detection
- **Presidio Documentation**: https://microsoft.github.io/presidio/
  - Microsoft's PII detection library
- **GDPR Compliance Guide**: https://gdpr.eu/
  - Understand EU data protection regulations
- **Regex Tutorial**: https://regexone.com/
  - Interactive lessons for pattern matching

### 🛠️ Performance & Optimization

#### Python Performance
- **Article**: ["Making Python Code 10x Faster"](https://martinheinz.dev/blog/64)
- **Video**: [Python Performance Tips](https://www.youtube.com/watch?v=YY7yJHo0M5I)
- **Tool**: [memory-profiler](https://github.com/pythonprofilers/memory_profiler)
  - Profile Python memory usage line-by-line

#### Database Optimization
- **SQLAlchemy Performance**: https://docs.sqlalchemy.org/en/20/faq/performance.html
  - Official performance tips
- **SQLite Optimization**: https://www.sqlite.org/optoverview.html
  - Understand query planning and indexes
- **Video**: [Database Indexing Explained](https://www.youtube.com/watch?v=fsG1XaZEa78)

#### Node.js Performance
- **Article**: ["Node.js Memory Management"](https://blog.appsignal.com/2020/05/06/nodejs-memory-management-guide.html)
- **Tool**: [clinic.js](https://clinicjs.org/)
  - Performance profiling for Node.js apps

### 🧪 Testing & Quality

#### Python Testing
- **pytest Documentation**: https://docs.pytest.org/en/stable/
  - Best testing framework for Python
- **Video**: [Python Testing with pytest](https://www.youtube.com/watch?v=bbp_849-RZ4)
- **Book**: [Test-Driven Development with Python](https://www.obeythetestinggoat.com/)
  - Free online book

#### API Testing
- **Postman Learning**: https://learning.postman.com/
  - Official tutorials for API testing
- **Article**: ["API Testing Best Practices"](https://blog.postman.com/api-testing-best-practices/)

### 🐳 DevOps & Deployment

#### Docker
- **Docker Tutorial**: https://docker-curriculum.com/
  - Beginner-friendly, hands-on
- **Video**: [Docker Crash Course](https://www.youtube.com/watch?v=pg19Z8LL06w)
  - 1 hour overview
- **Compose Guide**: https://docs.docker.com/compose/gettingstarted/

#### Production Deployment
- **Article**: ["Deploying FastAPI on AWS"](https://aws.amazon.com/blogs/compute/deploying-machine-learning-models-with-serverless-templates/)
- **Guide**: ["Production-Ready FastAPI"](https://testdriven.io/blog/fastapi-production/)
  - Covers logging, monitoring, security

### 📖 Books (Free & Paid)

#### Free
- **"Automate the Boring Stuff with Python"**: https://automatetheboringstuff.com/
  - Great for Python basics
- **"The Python Tutorial"**: https://docs.python.org/3/tutorial/
  - Official Python documentation
- **"You Don't Know JS"**: https://github.com/getify/You-Dont-Know-JS
  - Deep dive into JavaScript

#### Paid (Worth It)
- **"Fluent Python" by Luciano Ramalho**
  - Advanced Python patterns
- **"Designing Data-Intensive Applications" by Martin Kleppmann**
  - Database and system design
- **"Release It!" by Michael Nygard**
  - Production systems and resilience

### 🎥 YouTube Channels

- **[Corey Schafer](https://www.youtube.com/c/Coreyms)**: Python, Django, Flask tutorials
- **[Fireship](https://www.youtube.com/c/Fireship)**: Quick tech explanations (100 seconds series)
- **[TechWorld with Nana](https://www.youtube.com/c/TechWorldwithNana)**: DevOps, Docker, Kubernetes
- **[Traversy Media](https://www.youtube.com/c/TraversyMedia)**: Web development tutorials
- **[Academind](https://www.youtube.com/c/Academind)**: React, TypeScript, Node.js

### 🤝 Community & Help

- **Stack Overflow**: https://stackoverflow.com/
  - Search before asking, use tags like `[fastapi]`, `[python]`
- **FastAPI Discord**: https://discord.gg/VQjSZaeJmf
  - Very active community, helpful maintainers
- **Reddit**: r/Python, r/learnprogramming, r/webdev
- **GitHub Discussions**: Your own repo!
  - Enable "Discussions" tab for community support

### 🔧 Tools & Extensions

#### VS Code Extensions
- **Python** (Microsoft): Linting, debugging, IntelliSense
- **Pylance**: Fast Python language server
- **REST Client**: Test APIs without leaving VS Code
- **SQLite Viewer**: Browse database files
- **Docker**: Manage containers from IDE
- **GitLens**: Enhanced Git integration

#### Productivity Tools
- **[HTTPie](https://httpie.io/)**: Beautiful command-line HTTP client
  - `http POST localhost:8000/api/v1/scan/text text="test"`
- **[jq](https://stedolan.github.io/jq/)**: JSON processor for terminal
  - `curl localhost:8000/api/v1/scan/text | jq`
- **[Bruno](https://www.usebruno.com/)**: Open-source Postman alternative

### 📝 Cheat Sheets & Quick References

- **FastAPI Cheat Sheet**: https://gist.github.com/bgalvao/5c8e0cc3ea3c7a5ec37fac36e8c0e40c
- **Python Type Hints**: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
- **SQL Cheat Sheet**: https://www.sqltutorial.org/sql-cheat-sheet/
- **Regex Cheat Sheet**: https://regexr.com/
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf

### 🎯 Practice Projects

**After learning the basics, try building:**

1. **URL Shortener**: Practice FastAPI routing and database
2. **Todo API**: CRUD operations, authentication
3. **File Upload Service**: Handle multipart forms, storage
4. **Chat Application**: WebSockets, real-time communication
5. **Rate Limiter**: Middleware, performance optimization

---

## 🆘 Getting Help

**Stuck? Here's how to get unblocked:**

1. **Read error messages carefully**: They usually tell you exactly what's wrong
2. **Check logs**: `docker-compose logs api` or terminal output
3. **Search GitHub Issues**: Someone probably had the same problem
4. **Ask specific questions**: 
   - ❌ "It doesn't work"
   - ✅ "Getting 422 error when posting to /scan/text with payload {...}"
5. **Share minimal reproducible example**: Simplify until you find the root cause

**Good luck and happy coding!** 🚀

---

**Questions?** Review this guide and start implementing changes file by file. The core logic stays the same - we're just reframing it as an AI governance platform!
