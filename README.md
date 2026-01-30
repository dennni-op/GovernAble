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
git clone https://github.com/dennni-op/GovernAble.git
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

## 🏗 Project Structure
```
GovernAble/
├── engine/        # Core detection logic (open source)
├── api/           # FastAPI enforcement API for scanning
├── proxy/         # Shadow AI Governor proxy (enterprise)
├── web/           # Governance dashboard (Pro/Enterprise)
├── enterprise/    # Enterprise-only features (licensed)
├── tests/         # Unit and integration tests
├── docker-compose.yml
└── README.md
```

## 📚 Documentation
- **[Junior Developer Guide](./JUNIOR_DEV_GUIDE.md)**: Complete learning resource
- **[API Documentation](http://localhost:8000/docs)**: Interactive API docs (Swagger)
- **[Migration Guide](./AI_GOVERNANCE_MIGRATION.md)**: Detailed implementation guide

## 🤝 Contributing
See [CONTRIBUTING.md](./CONTRIBUTING.md)

## 📜 License
- **Open Source Core** (engine/ & api/): AGPL v3
- **Enterprise Features** (proxy/, web/): Commercial License

## 🆘 Support
- **Community**: GitHub Discussions
- **Enterprise**: enterprise@governable.ai
- **Security Issues**: security@governable.ai

⚡ Protect data. Govern AI. Stay compliant. ⚡
