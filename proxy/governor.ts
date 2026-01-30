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

dotenv.config();

const app = express();
app.use(bodyParser.json({ limit: "1mb" }));

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
async function enforceGovernancePolicy(text: string, userId?: string): Promise<any> {
  try {
    console.log(`[GOVERNANCE] Checking prompt for user: ${userId || 'anonymous'}`);
    
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

    console.log(`[GOVERNANCE] Decision: ${resp.data.action}`);
    return resp.data;
  } catch (e: any) {
    // FAIL SECURE: If governance API is down, BLOCK the request
    console.error("[GOVERNANCE] API error - failing secure:", e.message);
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

  console.log(`[AI REQUEST] User: ${userId}, Prompt length: ${prompt.length} chars`);

  // STEP 1: Enforce governance policy
  const decision = await enforceGovernancePolicy(prompt, userId);

  // STEP 2: Handle BLOCK decision
  if (decision.action === "BLOCK") {
    console.warn(`[BLOCKED] User: ${userId}, Reasons:`, decision.reasons);

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
    console.log(`[REDACTED] User: ${userId}, Items redacted:`, decision.reasons);
  }

  // STEP 4: Forward to actual AI service (only if ALLOWED or REDACTED)
  try {
    console.log(`[FORWARDING] Sending to ${LLM_TARGET}`);

    const upstreamResponse = await axios.post(
      `${LLM_TARGET}/v1/chat/completions`,
      {
        model: req.body.model || "gpt-4",
        messages: [
          { role: "user", content: finalPrompt }
        ],
        ...req.body
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );

    const duration = Date.now() - startTime;
    console.log(`[SUCCESS] Completed in ${duration}ms, Action: ${decision.action}`);

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
    console.error("[ERROR] AI service error:", err.message);
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

// Start the AI Governor
const PORT = process.env.PORT || 8787;
app.listen(PORT, () => {
  console.log(`\n🛡️  GovernAble AI Governor running on port ${PORT}`);
  console.log(`📋 Enforcement API: ${API_BASE}`);
  console.log(`🤖 AI Service: ${LLM_TARGET}`);
  console.log(`🔒 Policy: ${GOVERNANCE_POLICY}\n`);
});