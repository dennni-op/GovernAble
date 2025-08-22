# GovernAble
GovernAble is an open-core platform for AI governance, policy enforcement, and sensitive data protection.
It helps teams prevent Shadow AI risks by scanning data, enforcing branch/LLM policies, and ensuring compliance with security standards

GovernAble is an open-core platform for:
✅ AI governance
✅ Policy enforcement
✅ Sensitive data & secret protection

It helps teams prevent Shadow AI risks, enforce branch/LLM usage policies, and stay compliant with security regulations.

## ✨ Features
### 🔓 Free (Open Source)

Secret & PII scanning (API keys, passwords, personal data)

CLI + API (FastAPI) for local or service-based scanning

Customizable regex/NLP rule packs

### 💡 Pro (SaaS)

Web dashboard for policy violations & trends

Custom policy editor (YAML/JSON-based)

Team accounts + basic RBAC

### 🏢 Enterprise

Shadow AI Governor Proxy (LLM usage enforcement)

Compliance packs (GDPR, HIPAA, ISO27001)

Advanced integrations (Slack, Jira, Splunk, ELK)

SSO & advanced RBAC

## 🏗 Project Structure
GovernAble/
├── engine/        # Core detection logic (open source)
├── api/           # FastAPI API for scanning
├── proxy/         # Shadow AI Governor proxy (enterprise)
├── web/           # Web dashboard (Pro/Enterprise)
├── enterprise/    # Enterprise-only features (licensed)
├── tests/         # Unit and integration tests
├── docker-compose.yml
└── README.md

## 🚀 Quick Start
1. Clone
git clone https://github.com/dennni-op/GovernAble.git
cd GovernAble

2. Install deps
pip install -r requirements.txt

3. Run scanner (CLI)
python engine/cli.py scan ./my_project

4. Start API
uvicorn api.main:app --reload


Docs: http://localhost:8000/docs

## 🛠 Roadmap

 Core secret & PII scanner

 FastAPI scanning service

 Basic web dashboard (Pro)

 Shadow AI Governor proxy

 Compliance packs (Enterprise)

👉 Check GitHub Projects for progress.

## 🤝 Contributing

We ❤️ contributions!

Fork the repo

Create a branch (feature/my-feature)

Commit changes

Open a PR

Please see CONTRIBUTING.md.

## 📜 License

Open Source (AGPL/SSPL) → engine/ & api/

Commercial License → web/, proxy/, enterprise/

## 🌍 Why GovernAble?

🚨 Enterprises face Shadow AI risks

🛡 Developers need easy tools to enforce policies

📜 Compliance teams require audit-ready governance

GovernAble bridges open-source security tools with enterprise governance needs.

⚡ Protect data. Govern AI. Stay compliant. ⚡
