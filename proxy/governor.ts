import express from "express";
import bodyParser from "body-parser";
import axios from "axios";
import dotenv from "dotenv";
dotenv.config(); // This loads variables from a .env file in this folder.
const app = express();
// This middleware helps our server understand incoming JSON data.
app.use(bodyParser.json({ limit: "1mb" }));
// --- Configuration ---
// The address of our Python API.
const API_BASE = process.env.API_BASE || "http://localhost:8000";
// The real AI service we are protecting.
const LLM_TARGET = process.env.LLM_TARGET || "https://api.openai.com";
// This helper function calls our Python enforcement API.
async function enforceText(text: string) {
  try {
    // It makes a POST request to our /api/v1/enforce/check endpoint.
    const resp = await axios.post(`${API_BASE}/api/v1/enforce/check`, {
      text: text,
      // For the MVP, we're hard-coding a default policy: "REDACT by default".
      policy: { name: "default", mode: "REDACT", rules: [] }
    });
    // It returns the decision from the API (e.g., { action: "REDACT", ... }).
    return resp.data;
  } catch (e) {
    // If our Python API is down, we should probably block the request for safety.
    console.error("Error calling enforcement API:", e.message);
    return { action: "BLOCK", reasons: ["enforce-service-error"] };
  }
}
// --- The Main Proxy Endpoint ---
// We create an endpoint at '/proxy/llm' that listens for POST requests.
app.post("/proxy/llm", async (req, res) => {
  // 1. Get the user's prompt from the incoming request body.
  const prompt = req.body.prompt || "";
  // 2. Get a decision from our enforcement service.
  const decision = await enforceText(prompt);
  // 3. Act on the decision.
  if (decision.action === "BLOCK") {
    console.log("Request BLOCKED. Reasons:", decision.reasons);
    // If blocked, send an error back to the user and stop.
    return res.status(403).json({ error: "Blocked by security policy", reasons: decision.reasons });
  }
  // 4. Prepare the final prompt. If the decision was to REDACT, use the redacted text.
  // Otherwise, use the original prompt.
  const finalPrompt = decision.action === "REDACT" ? decision.redacted_text : prompt;
  if (decision.action === "REDACT") {
    console.log("Request REDACTED. Sending cleaned prompt to LLM.");
  }
  // 5. Forward the (possibly cleaned) request to the real LLM provider.
  try {
    const upstreamResponse = await axios.post(`${LLM_TARGET}/v1/chat/completions`,
      { /* ... The actual LLM request body would go here, using finalPrompt ... */ },
      { headers: { Authorization: `Bearer ${process.env.LLM_KEY}` } }
    );
    // 6. Send the LLM's response back to the original user.
    res.json({ llm_response: upstreamResponse.data, enforcement_action: decision });
  } catch (err: any) {
    // If the real LLM API gives an error, pass that error back.
    res.status(502).json({ error: "Upstream LLM provider error", details: err.message });
  }
});
// --- Start the Server ---
app.listen(process.env.PORT || 8787, () => {
  console.log("Governor Proxy is running on port 8787");
});