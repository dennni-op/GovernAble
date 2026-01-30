# 🎓 GovernAble - Junior Developer Learning Guide
## AI Usage Governance & Enforcement Engine

> **Welcome!** This comprehensive guide will walk you through every file in the GovernAble project - an **AI Usage Governance & Enforcement Engine**. You'll learn how the system controls, monitors, and enforces policies on AI service usage, prevents data leaks to AI models, and ensures compliance with organizational security policies.

## 🎯 How to Use This Guide

**For Complete Beginners:**
1. Start with [Project Overview](#project-overview) and [Technology Stack](#technology-stack)
2. Read [Key Programming Concepts](#key-programming-concepts) first
3. Then dive into [File-by-File Walkthrough](#file-by-file-walkthrough)

**For Intermediate Developers:**
1. Jump to specific files in [File-by-File Walkthrough](#file-by-file-walkthrough)
2. Review [Performance & Optimization](#performance--optimization) sections
3. Check [How to Improve Each Component](#how-to-improve-each-component)

**For Quick Reference:**
- Use the [Quick Reference Cheat Sheet](#quick-reference-cheat-sheet)
- Check [Common Patterns](#common-patterns-quick-reference)
- Review [Troubleshooting Guide](#troubleshooting-guide)

---

## 📚 Table of Contents

1. [Project Overview](#project-overview)
2. [Quick Reference Cheat Sheet](#quick-reference-cheat-sheet)
3. [Technology Stack](#technology-stack)
4. [Development Environment Setup](#development-environment-setup)
5. [File-by-File Walkthrough](#file-by-file-walkthrough)
   - [Python Backend (API & Engine)](#python-backend-api--engine)
   - [TypeScript Proxy](#typescript-proxy)
   - [React Frontend](#react-frontend)
   - [Configuration & DevOps](#configuration--devops)
6. [Key Programming Concepts](#key-programming-concepts)
7. [Performance & Optimization](#performance--optimization)
8. [Common Patterns Quick Reference](#common-patterns-quick-reference)
9. [How to Improve Each Component](#how-to-improve-each-component)
10. [Troubleshooting Guide](#troubleshooting-guide)
11. [Testing Strategies](#testing-strategies)
12. [Security Best Practices](#security-best-practices)
13. [Learning Resources](#learning-resources)

---

## 🎯 Project Overview

**GovernAble** is an **AI Usage Governance & Enforcement Engine** that:
- **Controls AI Access**: Acts as a security proxy between users and AI services (OpenAI, Claude, etc.)
- **Prevents Data Leaks**: Scans prompts for sensitive data before they reach AI models
- **Enforces Policies**: Blocks, warns, or redacts content based on organizational rules
- **Ensures Compliance**: Audits and logs all AI interactions for regulatory requirements
- **Manages Shadow AI**: Prevents unauthorized AI tool usage and enforces approved models only

**Architecture:**
```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Client    │─────▶│ Proxy (TS)   │─────▶│ OpenAI API  │
│ (Frontend)  │      │  governor.ts │      │             │
└─────────────┘      └──────────────┘      └─────────────┘
       │                     │
       │                     ▼
       │              ┌──────────────┐
       └─────────────▶│ FastAPI      │
                      │ (Python API) │
                      │              │
                      │ ┌──────────┐ │
                      │ │ Scanner  │ │
                      │ │ Engine   │ │
                      │ └──────────┘ │
                      └──────────────┘
                             │
                             ▼
                      ┌──────────────┐
                      │  SQLite DB   │
                      └──────────────┘
```

**AI Governance Flow:**
1. **User sends prompt** → Governor Proxy intercepts request
2. **Proxy scans prompt** → FastAPI enforcement API checks for sensitive data
3. **Policy evaluation** → Scanner detects secrets/PII, Policy engine decides action
4. **Enforcement** → BLOCK (reject), REDACT (clean), or ALLOW (forward)
5. **Forward to AI** → If allowed, proxy forwards cleaned prompt to OpenAI/Claude
6. **Response filtering** → Check AI response for data leaks
7. **Audit logging** → Record interaction in database for compliance
8. **Dashboard** → Admins monitor violations and trends

**Key Files by Function:**

| Function | File | Language | Purpose |
|----------|------|----------|----------|
| API Entry | `api/main.py` | Python | Initialize FastAPI enforcement service |
| Configuration | `api/config.py` | Python | Security & policy settings |
| Scanning | `api/routes/scan.py` | Python | Scan prompts/files for sensitive data |
| **Enforcement** | `api/routes/enforce.py` | Python | **AI usage policy enforcement** |
| Detection | `engine/scanner.py` | Python | Secret/PII detection engine |
| Rules | `engine/rules/base_patterns.yml` | YAML | Detection patterns (secrets, PII) |
| Database | `api/services/storage.py` | Python | Audit log & violation storage |
| Policies | `api/services/policies.py` | Python | **Governance policy evaluation** |
| **AI Proxy** | `proxy/governor.ts` | TypeScript | **Shadow AI Governor (intercepts LLM requests)** |
| Dashboard | `web/frontend/src/App.tsx` | TypeScript/React | Compliance monitoring UI |

---

## 📋 Quick Reference Cheat Sheet

### Common Commands

**Start AI Governance System:**
```powershell
# Install Python dependencies
pip install -r requirements.txt

# Start Enforcement API (port 8000)
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Start AI Governor Proxy (port 8787) - in separate terminal
cd proxy
npm install
npm start

# Or use Docker Compose (starts both services)
docker-compose up --build
```

**Test the AI Governance System:**
```powershell
# Health check
curl http://localhost:8000/health

# Test prompt scanning (detect secrets in AI prompt)
curl -X POST http://localhost:8000/api/v1/scan/text `
  -H "Content-Type: application/json" `
  -d '{"text":"Analyze this data: AWS key AKIAIOSFODNN7EXAMPLE"}'

# Test policy enforcement (should BLOCK or REDACT)
curl -X POST http://localhost:8000/api/v1/enforce/check `
  -H "Content-Type: application/json" `
  -d '{"text":"My password is secret123", "policy":{"name":"default","mode":"REDACT"}}'

# Test AI proxy (sends request through governance layer)
curl -X POST http://localhost:8787/proxy/llm `
  -H "Content-Type: application/json" `
  -d '{"prompt":"Help me debug this code with API key AKIA..."}'
```

### FastAPI Quick Reference

**Decorator Meanings:**
```python
@app.get("/path")          # Handle GET requests
@app.post("/path")         # Handle POST requests
@app.put("/path")          # Handle PUT requests
@app.delete("/path")       # Handle DELETE requests

async def handler():       # Async function (non-blocking)
    await db.query()       # Wait for async operation
    return result

def dependency():          # Dependency function
    return value

@app.post("/path")
async def handler(dep = Depends(dependency)):  # Inject dependency
    # dep will be the return value of dependency()
```

**Request Parameters:**
```python
# Path parameter
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    pass

# Query parameter
@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    # /items?skip=0&limit=10
    pass

# Request body (JSON)
class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
async def create_item(item: Item):
    # Automatically parses and validates JSON
    pass

# File upload
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    pass

# Form data
@app.post("/submit")
async def submit(username: str = Form(...)):
    pass
```

**Response Status Codes:**
```python
from fastapi import HTTPException, status

# Return error
raise HTTPException(status_code=400, detail="Bad request")
raise HTTPException(status_code=401, detail="Unauthorized")
raise HTTPException(status_code=404, detail="Not found")
raise HTTPException(status_code=500, detail="Internal error")

# Custom status code
from fastapi.responses import JSONResponse

return JSONResponse(
    status_code=status.HTTP_201_CREATED,
    content={"message": "Created"}
)
```

### Pydantic Quick Reference

**Model Definition:**
```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List

class User(BaseModel):
    # Required field
    name: str
    
    # Optional field (can be None)
    email: Optional[str] = None
    
    # Field with default value
    age: int = 0
    
    # Field with validation
    score: int = Field(..., ge=0, le=100)  # 0 <= score <= 100
    
    # List field
    tags: List[str] = Field(default_factory=list)
    
    # Custom validator
    @validator('email')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Invalid email')
        return v

# Usage
user = User(name="Alice", score=95)
print(user.name)  # "Alice"
print(user.dict())  # {"name": "Alice", "email": None, "age": 0, ...}
print(user.json())  # JSON string
```

### SQLAlchemy Quick Reference

**Define Model:**
```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
```

**CRUD Operations:**
```python
# Create
async with AsyncSessionLocal() as session:
    user = User(name="Alice")
    session.add(user)
    await session.commit()

# Read one
user = await session.get(User, user_id)

# Read many
from sqlalchemy import select
stmt = select(User).where(User.name == "Alice")
result = await session.execute(stmt)
users = result.scalars().all()

# Update
user.name = "Bob"
await session.commit()

# Delete
await session.delete(user)
await session.commit()
```

### React Hooks Quick Reference

**useState - Store component state:**
```typescript
const [count, setCount] = useState(0);  // Initial value: 0
setCount(count + 1);  // Update state
setCount(prev => prev + 1);  // Update based on previous value
```

**useEffect - Side effects:**
```typescript
// Run once on mount
useEffect(() => {
  fetchData();
}, []);

// Run when dependency changes
useEffect(() => {
  console.log(count);
}, [count]);

// Cleanup function
useEffect(() => {
  const timer = setInterval(() => {}, 1000);
  return () => clearInterval(timer);  // Cleanup
}, []);
```

**useCallback - Memoize functions:**
```typescript
const handleClick = useCallback(() => {
  console.log(count);
}, [count]);  // Only recreate when count changes
```

**useMemo - Memoize values:**
```typescript
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(a, b);
}, [a, b]);  // Only recompute when a or b changes
```

### Regex Quick Reference

| Pattern | Meaning | Example |
|---------|---------|----------|
| `\d` | Any digit (0-9) | `\d{3}` matches "123" |
| `\w` | Word character (a-z, A-Z, 0-9, _) | `\w+` matches "hello_123" |
| `\s` | Whitespace | `\s+` matches "   " |
| `.` | Any character (except newline) | `a.c` matches "abc", "a1c" |
| `^` | Start of string | `^Hello` matches "Hello world" |
| `$` | End of string | `world$` matches "Hello world" |
| `*` | 0 or more | `a*` matches "", "a", "aaa" |
| `+` | 1 or more | `a+` matches "a", "aaa" |
| `?` | 0 or 1 | `a?` matches "", "a" |
| `{n}` | Exactly n | `\d{3}` matches "123" |
| `{n,m}` | Between n and m | `\d{2,4}` matches "12", "123", "1234" |
| `[abc]` | One of a, b, or c | `[0-9]` matches any digit |
| `[^abc]` | NOT a, b, or c | `[^0-9]` matches non-digits |
| `\|` | OR | `cat\|dog` matches "cat" or "dog" |
| `()` | Capture group | `(\d+)` captures digits |
| `\b` | Word boundary | `\bword\b` matches "word" but not "sword" |

**Common Patterns:**
```regex
# Email
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

# URL
https?://[^\s]+

# Phone (US)
\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}

# IPv4 Address
\b(?:\d{1,3}\.){3}\d{1,3}\b

# Credit Card (basic)
\b\d{4}[-.\s]?\d{4}[-.\s]?\d{4}[-.\s]?\d{4}\b
```

---

## 🛠 Technology Stack

### Backend
- **Python 3.11+**: Main programming language
- **FastAPI**: Modern async web framework for building APIs
- **Pydantic**: Data validation using Python type hints
- **SQLAlchemy**: SQL database toolkit (ORM)
- **PyYAML**: YAML file parsing
- **Presidio** (optional): Microsoft's PII detection library

### Proxy
- **TypeScript/Node.js**: JavaScript runtime for the proxy server
- **Express**: Web framework for Node.js
- **Axios**: HTTP client for making requests

### Frontend
- **React**: UI library for building user interfaces
- **TypeScript**: Type-safe JavaScript

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Uvicorn**: ASGI server for Python

---

## � Development Environment Setup

### Prerequisites

**Required:**
- Python 3.11 or higher
- Node.js 18 or higher (for proxy)
- Git

**Optional:**
- Docker Desktop (for containerized development)
- PostgreSQL (for production database)
- Redis (for caching/rate limiting)

### Initial Setup (Windows PowerShell)

**1. Clone the repository:**
```powershell
git clone https://github.com/your-org/GovernAble.git
cd GovernAble
```

**2. Set up Python environment:**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt
```

**3. Set up environment variables:**
```powershell
# Create .env file
New-Item -Path .env -ItemType File

# Add to .env:
@"
ENV=development
GA_API_KEY=dev_secret_key_change_in_production
CORS_ORIGINS=*
DATABASE_URL=sqlite+aiosqlite:///./governable.db
MAX_SCAN_FILE_BYTES=5000000
"@ | Out-File -FilePath .env -Encoding utf8
```

**4. Initialize the database:**
```powershell
python -c "import asyncio; from api.services.storage import init_db; asyncio.run(init_db())"
```

**5. Start the API server:**
```powershell
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**6. Test the API:**
Open browser to http://localhost:8000/docs for interactive API documentation

### Using Docker (Easier Setup)

**Start everything:**
```powershell
docker-compose up --build
```

**Stop everything:**
```powershell
docker-compose down
```

**View logs:**
```powershell
docker-compose logs -f api
```

**Rebuild after code changes:**
```powershell
docker-compose up --build --force-recreate
```

### IDE Setup (VS Code)

**Recommended Extensions:**
1. Python (Microsoft)
2. Pylance (Microsoft)
3. Python Debugger (Microsoft)
4. SQLite Viewer
5. YAML
6. Docker
7. REST Client (for testing APIs)

**Settings (`.vscode/settings.json`):**
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.analysis.typeCheckingMode": "basic",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

**Launch configuration (`.vscode/launch.json`):**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "api.main:app",
        "--reload"
      ],
      "jinja": true,
      "justMyCode": false
    },
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    }
  ]
}
```

### Testing Your Setup

**Run tests:**
```powershell
pytest tests/ -v
```

**Check code style:**
```powershell
black . --check
flake8 .
```

**Test a scan:**
```powershell
# Create a test file
echo "My AWS key is AKIAIOSFODNN7EXAMPLE" > test.txt

# Scan it
curl -X POST http://localhost:8000/api/v1/scan/file `
  -F "file=@test.txt"
```

### Common Setup Issues

**Issue: `Module not found` error**
```powershell
# Solution: Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Issue: Port 8000 already in use**
```powershell
# Solution: Use a different port
uvicorn api.main:app --reload --port 8001

# Or find and kill the process using port 8000
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
```

**Issue: SQLite database locked**
```powershell
# Solution: Delete the database file and recreate
Remove-Item governable.db
python -c "import asyncio; from api.services.storage import init_db; asyncio.run(init_db())"
```

**Issue: Docker containers won't start**
```powershell
# Solution: Clean up and rebuild
docker-compose down -v
docker-compose up --build
```

---

## �📖 File-by-File Walkthrough

---

## Python Backend (API & Engine)

### 1. `api/config.py` - Configuration Management

**Purpose:** Centralize all application settings in one place.

**Key Concepts:**
```python
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "GovernAble API"
    API_V1_STR: str = "/api/v1"
    API_KEY: str = Field("dev_key", env="GA_API_KEY")
    CORS_ORIGINS: str = Field("*", env="CORS_ORIGINS")
    DATABASE_URL: str = Field("sqlite+aiosqlite:///./governable.db", env="DATABASE_URL")
    MAX_SCAN_FILE_BYTES: int = Field(5_000_000, env="MAX_SCAN_FILE_BYTES")
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**What's happening:**
1. **Pydantic BaseSettings**: Automatically loads settings from environment variables
2. **Field()**: Defines default values and environment variable names
3. **Type hints** (`str`, `int`): Automatic validation and conversion
4. **Singleton pattern**: `settings = Settings()` creates one instance for the whole app

**Junior Dev Lessons:**
- ✅ **DO**: Keep secrets in environment variables, not in code
- ✅ **DO**: Use type hints for validation
- ✅ **DO**: Provide sensible defaults for development
- ❌ **DON'T**: Hard-code passwords or API keys

**How to improve:**
```python
# Add validation
from pydantic import validator

class Settings(BaseSettings):
    API_KEY: str = Field("dev_key", env="GA_API_KEY")
    
    @validator('API_KEY')
    def validate_api_key(cls, v):
        if v == "dev_key":
            print("⚠️  WARNING: Using default API key! Set GA_API_KEY in production!")
        if len(v) < 8:
            raise ValueError("API key must be at least 8 characters")
        return v

# Add environment tracking
ENV: str = Field("development", env="ENV")

@property
def is_production(self) -> bool:
    return self.ENV == "production"
```

---

### 2. `api/main.py` - Application Entry Point

**Purpose:** Initialize the FastAPI app and register all routes.

**Key Concepts:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GovernAble API", version="0.1.0")

# Middleware - code that runs before/after every request
app.add_middleware(
    CORSMiddleware,
    allow_origins=[...],  # Which websites can access this API
    allow_credentials=True,
    allow_methods=["*"],  # Which HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Which HTTP headers
)

# Register routers - organize endpoints into modules
app.include_router(scan.router, prefix="/api/v1/scan", tags=["scan"])

# Simple health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}
```

**Junior Dev Lessons:**
- **Middleware**: Code that intercepts every request (useful for logging, authentication, CORS)
- **CORS**: Security feature that controls which websites can call your API
- **Router pattern**: Split endpoints into separate files for organization
- **Health checks**: Simple endpoint to verify the service is running

**How to improve:**
```python
# Add startup/shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize database, load ML models, etc."""
    from api.services.storage import init_db
    await init_db()
    print("✅ Database initialized")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources"""
    print("👋 Shutting down gracefully")

# Add global exception handler
from fastapi import Request, status
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred", "type": type(exc).__name__}
    )

# Add request logging
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print(f"{request.method} {request.url.path} - {response.status_code} - {duration:.2f}s")
    return response
```

---

### 3. `api/routes/scan.py` - Scanning Endpoints

**Purpose:** HTTP endpoints for scanning text and files.

**Key Concepts:**

#### **Dependency Injection with `Depends()`**
```python
def api_key_auth(request: Request):
    # This function runs BEFORE the endpoint
    return True  # Currently allows everything

@router.post("/text")
async def scan_text(payload: ScanTextRequest, ok: bool = Depends(api_key_auth)):
    # 'ok' will be True only if api_key_auth() returns True
    findings = scanner.scan_text(payload.text)
    return {"count": len(findings), "findings": [f.__dict__ for f in findings]}
```

**What `Depends()` does:**
- Runs the dependency function first
- If it raises an exception, the endpoint never runs
- Perfect for authentication, rate limiting, etc.

#### **File Upload Handling**
```python
@router.post("/file")
async def scan_file(
    file: UploadFile = File(...),      # The uploaded file
    use_presidio: bool = Form(True),   # A form field
    ok: bool = Depends(api_key_auth)
):
    # Validation
    if file.size > settings.MAX_SCAN_FILE_BYTES:
        raise HTTPException(400, "File too large")
    
    # Type checking
    allowed_types = [".txt", ".json", ".pdf", ".yml", ".yaml", ".csv", ".md"]
    if not any(file.filename.endswith(t) for t in allowed_types):
        raise HTTPException(400, f"File type not allowed. Allowed: {allowed_types}")
    
    # Read file
    contents = await file.read()  # Returns bytes
    text = contents.decode("utf-8")  # Convert to string
    
    # Scan
    findings = scanner.scan_text(text)
    return {"filename": file.filename, "count": len(findings), "findings": [f.__dict__ for f in findings]}
```

**Junior Dev Lessons:**
- **`UploadFile`**: FastAPI's wrapper for file uploads (has `.filename`, `.size`, `.read()`)
- **`Form()`**: Extract data from multipart form (not JSON)
- **`any()`**: Returns True if any condition in the iterable is True
- **`.endswith()`**: Check if string ends with a suffix (case-sensitive!)
- **Error handling**: Use try/except for file operations (decoding, reading)

**How to improve:**
```python
# 1. Make filename check case-insensitive
if not any(file.filename.lower().endswith(t.lower()) for t in allowed_types):
    raise HTTPException(400, f"File type not allowed")

# 2. Add proper authentication
def api_key_auth(request: Request):
    api_key = request.headers.get("x-api-key")
    if not api_key:
        raise HTTPException(401, "Missing API key")
    if api_key != settings.API_KEY:
        raise HTTPException(403, "Invalid API key")
    return True

# 3. Add rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/text")
@limiter.limit("10/minute")  # Max 10 requests per minute
async def scan_text(request: Request, payload: ScanTextRequest):
    # ...

# 4. Stream large files instead of loading all at once
async def scan_file(file: UploadFile = File(...)):
    # For large files, read in chunks
    text = ""
    while chunk := await file.read(8192):  # 8KB chunks
        text += chunk.decode("utf-8")
    
# 5. Support more file types
from PyPDF2 import PdfReader
import io

if file.filename.endswith(".pdf"):
    # Read PDF
    pdf_bytes = await file.read()
    pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
elif file.filename.endswith(".docx"):
    # Handle Word documents
    # ...
else:
    # Plain text
    contents = await file.read()
    text = contents.decode("utf-8")
```

---

### 4. `api/routes/enforce.py` - AI Usage Policy Enforcement

**Purpose:** **Core governance endpoint** - validates AI prompts against organizational policies before allowing them to reach AI models. Returns enforcement decision: ALLOW (safe), WARN (log only), REDACT (remove sensitive data), or BLOCK (reject entirely).

**Key Concepts:**
```python
from api.services.policies import Policy, evaluate_policy, EvalResult

class EnforceRequest(BaseModel):
    text: str
    policy: Policy

@router.post("/check", response_model=EvalResult)
async def check(payload: EnforceRequest):
    result = evaluate_policy(payload.text, payload.policy)
    return result
```

**What's happening:**
1. **Pydantic models**: Validate incoming JSON automatically
2. **`response_model`**: FastAPI will serialize the response and validate it
3. **Separation of concerns**: Route just handles HTTP, logic is in `services/policies.py`

**Junior Dev Lessons:**
- **Thin controllers**: Keep route handlers simple, put business logic in services
- **Type safety**: Pydantic ensures data structure matches expectations
- **API design**: Use POST for operations that change state or process data

**How to improve:**
```python
# 1. Add caching for repeated checks
from functools import lru_cache
import hashlib

def hash_request(text: str, policy: Policy) -> str:
    """Create a unique hash for this request"""
    content = f"{text}:{policy.json()}"
    return hashlib.sha256(content.encode()).hexdigest()

# In-memory cache (consider Redis for production)
_cache = {}

@router.post("/check", response_model=EvalResult)
async def check(payload: EnforceRequest):
    cache_key = hash_request(payload.text, payload.policy)
    
    if cache_key in _cache:
        return _cache[cache_key]
    
    result = evaluate_policy(payload.text, payload.policy)
    _cache[cache_key] = result
    return result

# 2. Add async processing for slow checks
from fastapi import BackgroundTasks

@router.post("/check-async")
async def check_async(payload: EnforceRequest, background_tasks: BackgroundTasks):
    # Return immediately with a job ID
    job_id = str(uuid.uuid4())
    background_tasks.add_task(process_enforcement, job_id, payload.text, payload.policy)
    return {"job_id": job_id, "status": "processing"}

# 3. Add batch processing
class BatchEnforceRequest(BaseModel):
    items: List[EnforceRequest]

@router.post("/check-batch")
async def check_batch(payload: BatchEnforceRequest):
    results = [evaluate_policy(item.text, item.policy) for item in payload.items]
    return {"count": len(results), "results": results}
```

---

### 5. `api/services/policies.py` - AI Governance Policy Engine

**Purpose:** **Heart of the governance system** - evaluates AI prompts against organizational policies. Determines whether to allow, block, or redact sensitive information before it reaches external AI services. Protects against data exfiltration and ensures compliance.

**Key Concepts:**

#### **Type Literals for Enums**
```python
from typing import Literal

Action = Literal["ALLOW", "WARN", "REDACT", "BLOCK"]
```
- Instead of a string that could be anything, `Action` can ONLY be one of these four values
- IDE autocomplete works perfectly
- Type checker catches typos

#### **Pydantic Models for Data Structure**
```python
class Rule(BaseModel):
    id: str           # e.g., "AWS_ACCESS_KEY_ID"
    action: Action = "REDACT"

class Policy(BaseModel):
    name: str
    mode: Action = "WARN"           # Default action
    rules: List[Rule] = Field(default_factory=list)  # Specific overrides
```

#### **Business Logic**
```python
def evaluate_policy(text: str, policy: Policy) -> EvalResult:
    # 1. Scan for secrets
    findings = scanner.scan_text(text)
    
    if not findings:
        return EvalResult(action="ALLOW", reasons=[])
    
    # 2. Build a lookup map for quick access
    rule_overrides = {r.id: r.action for r in policy.rules}
    
    # 3. Determine action for each finding
    actions_to_take = []
    redacted_text = text
    
    for f in findings:
        # Use specific rule if exists, otherwise use default mode
        action = rule_overrides.get(f.label, policy.mode)
        actions_to_take.append(action)
        
        if action == "REDACT":
            redacted_text = redacted_text.replace(f.match, "[REDACTED]")
    
    # 4. Return the most severe action
    if "BLOCK" in actions_to_take:
        return EvalResult(action="BLOCK", reasons=reasons)
    if "REDACT" in actions_to_take:
        return EvalResult(action="REDACT", redacted_text=redacted_text, reasons=reasons)
    if "WARN" in actions_to_take:
        return EvalResult(action="WARN", reasons=reasons)
    
    return EvalResult(action="ALLOW", reasons=reasons)
```

**Junior Dev Lessons:**
- **Dictionary comprehension**: `{r.id: r.action for r in policy.rules}` creates a lookup map
- **`.get()` method**: Safe dictionary access with a default value
- **String replacement**: `text.replace(old, new)` - but watch out for overlapping matches!
- **Severity hierarchy**: BLOCK > REDACT > WARN > ALLOW

**Problems in current code:**
1. **String replacement is naive**: Overlapping matches or multiple occurrences might not work correctly
2. **No caching**: Scanning the same text multiple times is wasteful
3. **No logging**: Can't audit what was blocked/redacted

**How to improve:**
```python
# 1. Better redaction (preserve positions)
def redact_findings(text: str, findings: List[Finding]) -> str:
    """Redact findings from highest to lowest position to maintain indices"""
    # Sort by position (descending) so later replacements don't affect earlier ones
    sorted_findings = sorted(findings, key=lambda f: f.start, reverse=True)
    
    for f in sorted_findings:
        # Use exact positions instead of string replacement
        text = text[:f.start] + "[REDACTED]" + text[f.end:]
    
    return text

# 2. Add severity scoring
def calculate_severity_score(findings: List[Finding]) -> int:
    """Calculate a numeric severity score"""
    severity_map = {"LOW": 1, "MEDIUM": 5, "HIGH": 10, "CRITICAL": 20}
    return sum(severity_map.get(f.severity, 0) for f in findings)

# 3. Add detailed audit logging
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def evaluate_policy(text: str, policy: Policy) -> EvalResult:
    start_time = datetime.utcnow()
    findings = scanner.scan_text(text)
    
    # ... evaluation logic ...
    
    # Log the decision
    logger.info({
        "timestamp": start_time.isoformat(),
        "policy": policy.name,
        "action": final_action,
        "finding_count": len(findings),
        "severity_score": calculate_severity_score(findings),
        "text_length": len(text)
    })
    
    return result

# 4. Add custom actions
class CustomAction(BaseModel):
    type: Literal["WEBHOOK", "EMAIL", "SLACK"]
    config: Dict[str, Any]

class Rule(BaseModel):
    id: str
    action: Action = "REDACT"
    custom_actions: List[CustomAction] = []

# Then in evaluation:
if action == "BLOCK":
    for custom_action in rule.custom_actions:
        await send_alert(custom_action, finding)
```

---

### 6. `api/services/storage.py` - Database Layer

**Purpose:** Save scan results to a database for later analysis.

**Key Concepts:**

#### **SQLAlchemy Async ORM**
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column

# Create connection to database
engine = create_async_engine(DATABASE_URL)

# Session factory (creates new database conversations)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Base class for all models
Base = declarative_base()
```

#### **Defining a Table**
```python
class ScanResult(Base):
    __tablename__ = "scan_results"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(256), nullable=True)
    findings: Mapped[str] = mapped_column(Text)  # JSON stored as string
    scanned_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())
```

**What's happening:**
- `Mapped[int]`: Type hint for the column
- `mapped_column()`: Defines the actual database column
- `server_default=func.now()`: Database sets timestamp automatically

#### **CRUD Operations**
```python
async def save_scan(filename: str, findings: dict):
    async with AsyncSessionLocal() as session:
        # Create new record
        record = ScanResult(
            filename=filename,
            findings=json.dumps(findings)  # Convert dict to JSON string
        )
        session.add(record)           # Stage the change
        await session.commit()        # Save to database
        return record.id
```

**Junior Dev Lessons:**
- **ORM**: Object-Relational Mapping - treat database rows as Python objects
- **Async database**: Use `async with` and `await` for non-blocking I/O
- **Session pattern**: Open session → make changes → commit → close
- **JSON storage**: Store complex data as JSON text (better: use JSONB in PostgreSQL)

**How to improve:**
```python
# 1. Add more CRUD operations
async def get_scan_by_id(scan_id: int) -> Optional[ScanResult]:
    async with AsyncSessionLocal() as session:
        result = await session.get(ScanResult, scan_id)
        return result

async def list_recent_scans(limit: int = 10) -> List[ScanResult]:
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        stmt = select(ScanResult).order_by(ScanResult.scanned_at.desc()).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

async def delete_scan(scan_id: int):
    async with AsyncSessionLocal() as session:
        record = await session.get(ScanResult, scan_id)
        if record:
            await session.delete(record)
            await session.commit()

# 2. Add proper models (separate table for findings)
class Finding(Base):
    __tablename__ = "findings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scan_id: Mapped[int] = mapped_column(Integer, ForeignKey("scan_results.id"))
    label: Mapped[str] = mapped_column(String(100))
    match: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(20))
    start_pos: Mapped[int] = mapped_column(Integer)
    end_pos: Mapped[int] = mapped_column(Integer)
    
    # Relationship
    scan: Mapped["ScanResult"] = relationship(back_populates="findings")

class ScanResult(Base):
    __tablename__ = "scan_results"
    # ...
    findings: Mapped[List["Finding"]] = relationship(back_populates="scan")

# 3. Add database migrations (Alembic)
# Install: pip install alembic
# alembic init alembic
# alembic revision --autogenerate -m "Initial schema"
# alembic upgrade head

# 4. Add connection pooling and retry logic
from sqlalchemy.pool import NullPool
from tenacity import retry, stop_after_attempt, wait_exponential

engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Disable pooling for SQLite
    echo=True  # Log all SQL queries (for debugging)
)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
async def save_scan_with_retry(filename: str, findings: dict):
    """Retry failed database operations"""
    return await save_scan(filename, findings)
```

---

### 7. `engine/scanner.py` - Sensitive Data Detection Engine

**Purpose:** **The detection brain** - scans AI prompts and responses for sensitive data (API keys, passwords, PII, confidential information) BEFORE they're sent to external AI models. Prevents accidental data exfiltration through AI interactions. Uses regex patterns and optional ML-based detection (Presidio).

**Key Concepts:**

#### **Data Class for Results**
```python
from dataclasses import dataclass

@dataclass
class Finding:
    label: str       # e.g., "AWS_ACCESS_KEY_ID"
    match: str       # The actual secret found
    start: int       # Character position where it starts
    end: int         # Character position where it ends
    severity: str    # "LOW", "MEDIUM", "HIGH"
    source: str      # "regex" or "presidio"
    context: str     # Surrounding text for context
```

**Why dataclass?**
- Automatic `__init__`, `__repr__`, `__eq__` methods
- Less boilerplate than regular class
- Similar to Pydantic but lighter weight

#### **Loading Rules from YAML**
```python
import yaml
from pathlib import Path

def load_patterns(path: Optional[Path] = None) -> Dict[str, Dict[str, str]]:
    ROOT = Path(__file__).resolve().parent
    DEFAULT_PATTERNS = ROOT / "rules" / "base_patterns.yml"
    
    p = path if path else DEFAULT_PATTERNS
    
    if not p.exists():
        raise FileNotFoundError(f"Reference file not found: {p}")
    
    with p.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}
```

**Junior Dev Lessons:**
- **Path handling**: Use `pathlib.Path` instead of string concatenation
- **`__file__`**: Special variable containing the path to the current Python file
- **`.resolve()`**: Get absolute path
- **YAML**: Human-readable config format

#### **Compiling Regex Patterns**
```python
class Scanner:
    def __init__(self, patterns: Optional[Dict] = None, use_presidio: bool = True):
        self.patterns = patterns or load_patterns()
        
        # Pre-compile regex patterns for speed
        self.compiled = []
        for label, meta in self.patterns.items():
            try:
                regex = re.compile(meta["pattern"])
                self.compiled.append((label, regex))
            except re.error as e:
                continue  # Skip invalid patterns
```

**Why compile regex?**
- `re.compile()` converts the pattern string into a bytecode
- Much faster when you use the same pattern multiple times
- Validates the regex syntax at startup, not during scanning

#### **Scanning Text**
```python
def scan_text(self, text: str, max_len: int = 2_000_000) -> List[Finding]:
    if len(text) > max_len:
        raise ValueError(f"Text too long: {len(text)} > {max_len}")
    
    findings: List[Finding] = []
    
    # Search with each regex pattern
    for label, compiled_regex in self.compiled:
        for match in compiled_regex.finditer(text):
            # Extract context (30 chars before and after)
            start = match.start()
            end = match.end()
            context_start = max(0, start - 30)
            context_end = min(len(text), end + 30)
            context = text[context_start:context_end]
            
            finding = Finding(
                label=label,
                match=match.group(0),
                start=start,
                end=end,
                severity=self.patterns[label].get("severity", "MEDIUM"),
                source="regex",
                context=context
            )
            findings.append(finding)
    
    # Optional: Use Presidio for ML-based PII detection
    if self.use_presidio and self.presidio:
        # ... presidio logic ...
    
    return self._dedupe(findings)
```

**Junior Dev Lessons:**
- **`finditer()`**: Returns an iterator of all matches (better than `findall()` for positions)
- **`match.start()` / `match.end()`**: Get positions in the original string
- **`match.group(0)`**: Get the matched text
- **Context extraction**: Show surrounding text to help users understand the match

**How to improve:**
```python
# 1. Add confidence scoring
@dataclass
class Finding:
    # ... existing fields ...
    confidence: float = 1.0  # 0.0 to 1.0

def scan_text(self, text: str) -> List[Finding]:
    findings = []
    
    for label, regex in self.compiled:
        for match in regex.finditer(text):
            # Calculate confidence based on context
            confidence = self._calculate_confidence(match, text, label)
            
            finding = Finding(
                # ... other fields ...
                confidence=confidence
            )
            findings.append(finding)
    
    return findings

def _calculate_confidence(self, match: re.Match, text: str, label: str) -> float:
    """Heuristics to reduce false positives"""
    matched_text = match.group(0)
    
    # Lower confidence if it looks like an example
    if any(word in text[max(0, match.start()-50):match.end()+50].lower() 
           for word in ["example", "test", "fake", "dummy"]):
        return 0.5
    
    # Higher confidence if it matches checksum (for some secrets)
    if label == "AWS_ACCESS_KEY_ID":
        # AWS keys follow specific patterns
        return 0.95
    
    return 0.8

# 2. Add async scanning for large files
async def scan_text_async(self, text: str) -> List[Finding]:
    """Scan in chunks without blocking"""
    import asyncio
    
    chunk_size = 100_000  # 100KB chunks
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    # Scan chunks in parallel
    tasks = [asyncio.to_thread(self.scan_text, chunk) for chunk in chunks]
    results = await asyncio.gather(*tasks)
    
    # Combine results
    all_findings = []
    offset = 0
    for chunk_findings in results:
        # Adjust positions
        for f in chunk_findings:
            f.start += offset
            f.end += offset
        all_findings.extend(chunk_findings)
        offset += chunk_size
    
    return self._dedupe(all_findings)

# 3. Better deduplication
def _dedupe(self, findings: List[Finding]) -> List[Finding]:
    """Remove duplicate and overlapping findings"""
    if not findings:
        return []
    
    # Sort by start position
    findings.sort(key=lambda f: (f.start, -f.confidence))
    
    deduplicated = []
    last_end = -1
    
    for f in findings:
        # Skip if overlaps with previous finding
        if f.start < last_end:
            # Keep the one with higher confidence
            if deduplicated and f.confidence > deduplicated[-1].confidence:
                deduplicated[-1] = f
                last_end = f.end
            continue
        
        deduplicated.append(f)
        last_end = f.end
    
    return deduplicated

# 4. Add custom validators
class SecretValidator:
    """Validate that detected secrets are real"""
    
    @staticmethod
    def validate_aws_key(key: str) -> bool:
        """Check if AWS key is valid format"""
        if not key.startswith("AKIA"):
            return False
        if len(key) != 20:
            return False
        # Could add checksum validation here
        return True
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

# Use in Scanner:
def scan_text(self, text: str) -> List[Finding]:
    findings = []
    
    for label, regex in self.compiled:
        for match in regex.finditer(text):
            matched_text = match.group(0)
            
            # Validate finding
            if label == "AWS_ACCESS_KEY_ID":
                if not SecretValidator.validate_aws_key(matched_text):
                    continue  # Skip false positive
            
            # ... create finding ...
    
    return findings
```

---

### 8. `engine/rules/base_patterns.yml` - Detection Rules

**Purpose:** Define what secrets to look for and how to find them.

**Structure:**
```yaml
AWS_ACCESS_KEY_ID:
  pattern: 'AKIA[0-9A-Z]{16}'
  severity: HIGH
  description: 'AWS Access Key ID'

PAT_TOKEN:
  pattern: 'ghp_[A-Za-z0-9_]{36}'
  severity: HIGH
  description: 'GitHub Personal Access Token'

NHS_NUMBER:
  pattern: '\b\d{3} \d{3} \d{4}\b'
  severity: HIGH
  description: 'UK National Health Service (NHS) Number'
```

**Junior Dev Lessons:**
- **YAML format**: `key: value`, indentation matters
- **Regex patterns**: Strings that describe text patterns
  - `\b` = word boundary
  - `\d` = any digit (0-9)
  - `{16}` = exactly 16 characters
  - `[0-9A-Z]` = any character in this range
  - `+` = one or more
  - `?` = optional

**Regex Breakdown:**

1. `AKIA[0-9A-Z]{16}` - AWS Access Key
   - Must start with "AKIA"
   - Followed by exactly 16 uppercase letters or digits

2. `ghp_[A-Za-z0-9_]{36}` - GitHub Token
   - Starts with "ghp_"
   - Followed by 36 characters (letters, numbers, underscore)

3. `\b\d{3} \d{3} \d{4}\b` - NHS Number
   - `\b` = word boundary (start/end of word)
   - `\d{3}` = exactly 3 digits
   - Space, then 3 more digits, space, then 4 digits
   - Matches: "123 456 7890"

**How to improve:**
```yaml
# 1. Add more metadata
AWS_ACCESS_KEY_ID:
  pattern: 'AKIA[0-9A-Z]{16}'
  severity: HIGH
  description: 'AWS Access Key ID'
  category: 'cloud-credentials'
  remediation: 'Rotate key immediately in AWS IAM console'
  references:
    - 'https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html'
  tags: ['aws', 'iam', 'credential']
  
# 2. Add entropy checking (for generic secrets)
GENERIC_HIGH_ENTROPY:
  pattern: '[a-zA-Z0-9/+=]{32,}'
  severity: MEDIUM
  description: 'High entropy string (possible secret)'
  requires_entropy_check: true
  min_entropy: 4.5

# 3. Add whitelist patterns (reduce false positives)
AWS_ACCESS_KEY_ID:
  pattern: 'AKIA[0-9A-Z]{16}'
  severity: HIGH
  whitelist_patterns:
    - 'AKIAIOSFODNN7EXAMPLE'  # AWS documentation example
    - 'AKIA[X]{16}'           # Obvious placeholder
    
# 4. Add capture groups for structured data
CREDIT_CARD:
  pattern: '\b(?<brand>visa|mastercard|amex)\s*(?<number>\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4})\b'
  severity: HIGH
  description: 'Credit card number'
  extract_fields: ['brand', 'number']

# 5. Multi-line patterns
PRIVATE_KEY:
  pattern: |
    -----BEGIN (?:RSA |EC )?PRIVATE KEY-----
    [\s\S]+?
    -----END (?:RSA |EC )?PRIVATE KEY-----
  severity: CRITICAL
  description: 'Private encryption key'
  flags: ['MULTILINE', 'DOTALL']
```

---

## TypeScript Proxy

### 9. `proxy/governor.ts` - Shadow AI Governor (Enforcement Proxy)

**Purpose:** **Critical security layer** - intercepts ALL AI requests before they reach external services (OpenAI, Claude, etc.). This "man-in-the-middle" proxy enforces governance policies, preventing employees from accidentally or intentionally leaking sensitive data to AI models. Organizations can't control external AI services, but they CAN control what data leaves their network.

**Key Concepts:**

#### **Express Server Setup**
```typescript
import express from "express";
import bodyParser from "body-parser";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();  // Load .env file

const app = express();
app.use(bodyParser.json({ limit: "1mb" }));
```

**What's happening:**
- **Express**: Minimal web framework for Node.js
- **body-parser**: Middleware to parse JSON request bodies
- **axios**: HTTP client for making requests
- **dotenv**: Loads environment variables from `.env` file

#### **Calling the Python API**
```typescript
async function enforceText(text: string) {
  try {
    const resp = await axios.post(`${API_BASE}/api/v1/enforce/check`, {
      text: text,
      policy: { name: "default", mode: "REDACT", rules: [] }
    });
    return resp.data;
  } catch (e) {
    console.error("Error calling enforcement API:", e.message);
    return { action: "BLOCK", reasons: ["enforce-service-error"] };
  }
}
```

**Junior Dev Lessons:**
- **async/await**: Modern JavaScript for handling asynchronous operations
- **try/catch**: Error handling
- **Fail-safe**: If policy service is down, default to BLOCK (security first!)

#### **AI Governance Proxy Logic**
```typescript
app.post("/proxy/llm", async (req, res) => {
  // 1. Intercept user's AI prompt BEFORE it reaches OpenAI
  const prompt = req.body.prompt || "";
  
  // 2. Enforce governance policy (check for sensitive data)
  const decision = await enforceText(prompt);
  
  // 3. BLOCK: Prevent data leak - don't forward to AI
  if (decision.action === "BLOCK") {
    console.log("⛔ AI request BLOCKED:", decision.reasons);
    return res.status(403).json({ 
      error: "Request blocked by AI governance policy", 
      reasons: decision.reasons,
      remediation: "Remove sensitive data and try again"
    });
  }
  
  // 4. REDACT: Clean sensitive data before forwarding
  const finalPrompt = decision.action === "REDACT" 
    ? decision.redacted_text 
    : prompt;
  
  if (decision.action === "REDACT") {
    console.log("🧹 Sensitive data redacted before sending to AI");
  }
  
  // 5. Forward cleaned/approved prompt to AI service
  try {
    const upstreamResponse = await axios.post(
      `${LLM_TARGET}/v1/chat/completions`,
      { 
        model: "gpt-4",
        messages: [{ role: "user", content: finalPrompt }]
      },
      { headers: { Authorization: `Bearer ${process.env.LLM_KEY}` } }
    );
    
    // 6. Return LLM response
    res.json({ 
      llm_response: upstreamResponse.data, 
      enforcement_action: decision 
    });
  } catch (err: any) {
    res.status(502).json({ 
      error: "Upstream LLM provider error", 
      details: err.message 
    });
  }
});

app.listen(8787, () => {
  console.log("Governor Proxy is running on port 8787");
});
```

**Junior Dev Lessons:**
- **Ternary operator**: `condition ? valueIfTrue : valueIfFalse`
- **Status codes**: 403 = Forbidden, 502 = Bad Gateway
- **Proxy pattern**: Acts as a middleman, can inspect/modify requests
- **TypeScript `any`**: Avoid this! Use proper types

**How to improve:**
```typescript
// 1. Add proper TypeScript types
interface EnforcementDecision {
  action: "ALLOW" | "WARN" | "REDACT" | "BLOCK";
  redacted_text?: string;
  reasons: string[];
}

interface LLMRequest {
  prompt: string;
  model?: string;
  max_tokens?: number;
}

interface LLMResponse {
  id: string;
  choices: Array<{
    message: {
      role: string;
      content: string;
    };
  }>;
}

// 2. Add request logging and auditing
import winston from "winston";

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'proxy.log' })
  ]
});

app.post("/proxy/llm", async (req, res) => {
  const requestId = crypto.randomUUID();
  const startTime = Date.now();
  
  logger.info({
    requestId,
    event: "request_received",
    ip: req.ip,
    prompt_length: req.body.prompt?.length || 0
  });
  
  // ... enforcement and forwarding ...
  
  logger.info({
    requestId,
    event: "request_completed",
    action: decision.action,
    duration_ms: Date.now() - startTime,
    blocked: decision.action === "BLOCK"
  });
});

// 3. Add rate limiting per user
import rateLimit from "express-rate-limit";

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,  // Max 100 requests per window
  message: "Too many requests, please try again later"
});

app.use("/proxy/llm", limiter);

// 4. Add authentication
function authenticateUser(req: express.Request, res: express.Response, next: express.NextFunction) {
  const apiKey = req.headers["x-api-key"];
  
  if (!apiKey || !isValidApiKey(apiKey)) {
    return res.status(401).json({ error: "Invalid or missing API key" });
  }
  
  // Attach user info to request
  req.user = getUserFromApiKey(apiKey);
  next();
}

app.post("/proxy/llm", authenticateUser, async (req, res) => {
  // Now req.user is available
  logger.info({ user: req.user.id, action: "llm_request" });
  // ...
});

// 5. Add response caching
import NodeCache from "node-cache";

const cache = new NodeCache({ stdTTL: 600 }); // Cache for 10 minutes

app.post("/proxy/llm", async (req, res) => {
  const cacheKey = `llm:${hashPrompt(req.body.prompt)}`;
  
  // Check cache first
  const cached = cache.get(cacheKey);
  if (cached) {
    logger.info({ event: "cache_hit", key: cacheKey });
    return res.json(cached);
  }
  
  // ... normal processing ...
  
  // Cache the response
  cache.set(cacheKey, response);
  res.json(response);
});

// 6. Add health checks and metrics
app.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    timestamp: new Date().toISOString()
  });
});

// 7. Add graceful shutdown
process.on("SIGTERM", () => {
  logger.info("SIGTERM received, shutting down gracefully");
  server.close(() => {
    logger.info("Server closed");
    process.exit(0);
  });
});
```

---

## React Frontend

### 10. `web/frontend/src/App.tsx` - Dashboard UI

**Purpose:** Display recent scans in a web interface.

**Key Concepts:**

#### **React Hooks**
```typescript
import React, { useEffect, useState } from "react";

type ScanResult = { 
  id: number; 
  filename: string; 
  scanned_at: string; 
  findings: string 
};

function App() {
  // State: data that can change
  const [rows, setRows] = useState<ScanResult[]>([]);
  
  // Effect: runs after component mounts
  useEffect(() => {
    fetch("http://localhost:8000/api/v1/scan/results")
      .then(r => r.json())
      .then(setRows)
      .catch(console.error);
  }, []);  // Empty array = run once
  
  return (
    <div>
      <h1>GovernAble — Recent scans</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Filename</th>
            <th>When</th>
            <th>Findings</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(r => (
            <tr key={r.id}>
              <td>{r.id}</td>
              <td>{r.filename}</td>
              <td>{new Date(r.scanned_at).toLocaleString()}</td>
              <td>
                <pre>{JSON.stringify(JSON.parse(r.findings || "[]"), null, 2)}</pre>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
```

**Junior Dev Lessons:**
- **useState**: Store component state (data that changes)
- **useEffect**: Run side effects (API calls, subscriptions)
- **Dependency array []**: Controls when effect runs
  - `[]` = run once on mount
  - `[count]` = run when `count` changes
  - No array = run on every render
- **.map()**: Transform array into JSX elements
- **key prop**: React needs unique keys for list items

**How to improve:**
```typescript
// 1. Add loading and error states
function App() {
  const [rows, setRows] = useState<ScanResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    setLoading(true);
    fetch("http://localhost:8000/api/v1/scan/results")
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(data => {
        setRows(data);
        setError(null);
      })
      .catch(err => {
        console.error(err);
        setError(err.message);
      })
      .finally(() => setLoading(false));
  }, []);
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (rows.length === 0) return <div>No scans yet</div>;
  
  return (/* table */);
}

// 2. Extract components
function ScanRow({ scan }: { scan: ScanResult }) {
  const [expanded, setExpanded] = useState(false);
  const findings = JSON.parse(scan.findings || "[]");
  
  return (
    <tr>
      <td>{scan.id}</td>
      <td>{scan.filename}</td>
      <td>{new Date(scan.scanned_at).toLocaleString()}</td>
      <td>
        <button onClick={() => setExpanded(!expanded)}>
          {findings.length} findings
        </button>
        {expanded && (
          <pre>{JSON.stringify(findings, null, 2)}</pre>
        )}
      </td>
    </tr>
  );
}

// 3. Add pagination
function App() {
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  
  useEffect(() => {
    fetch(`http://localhost:8000/api/v1/scan/results?page=${page}&limit=10`)
      .then(/* ... */);
  }, [page]);
  
  return (
    <>
      <table>{/* ... */}</table>
      <div>
        <button 
          disabled={page === 1} 
          onClick={() => setPage(page - 1)}
        >
          Previous
        </button>
        <span>Page {page} of {totalPages}</span>
        <button 
          disabled={page === totalPages} 
          onClick={() => setPage(page + 1)}
        >
          Next
        </button>
      </div>
    </>
  );
}

// 4. Add filtering and sorting
function App() {
  const [rows, setRows] = useState<ScanResult[]>([]);
  const [filter, setFilter] = useState("");
  const [sortBy, setSortBy] = useState<"date" | "filename">("date");
  
  const filteredRows = rows
    .filter(r => r.filename.toLowerCase().includes(filter.toLowerCase()))
    .sort((a, b) => {
      if (sortBy === "date") {
        return new Date(b.scanned_at).getTime() - new Date(a.scanned_at).getTime();
      }
      return a.filename.localeCompare(b.filename);
    });
  
  return (
    <>
      <input 
        placeholder="Filter by filename..." 
        value={filter}
        onChange={e => setFilter(e.target.value)}
      />
      <select value={sortBy} onChange={e => setSortBy(e.target.value as any)}>
        <option value="date">Sort by Date</option>
        <option value="filename">Sort by Filename</option>
      </select>
      <table>
        {/* Use filteredRows instead of rows */}
      </table>
    </>
  );
}

// 5. Add real-time updates with WebSocket
useEffect(() => {
  const ws = new WebSocket("ws://localhost:8000/ws/scans");
  
  ws.onmessage = (event) => {
    const newScan = JSON.parse(event.data);
    setRows(prev => [newScan, ...prev]);
  };
  
  return () => ws.close();  // Cleanup on unmount
}, []);

// 6. Use a proper HTTP client (React Query)
import { useQuery } from "@tanstack/react-query";

function App() {
  const { data: rows, isLoading, error } = useQuery({
    queryKey: ["scans"],
    queryFn: () => 
      fetch("http://localhost:8000/api/v1/scan/results").then(r => r.json()),
    refetchInterval: 5000  // Refresh every 5 seconds
  });
  
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return (/* table */);
}
```

---

## Configuration & DevOps

### 11. `Dockerfile` - Container Definition

**Purpose:** Package the application into a container.

**Key Concepts:**
```dockerfile
# 1. Base image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements first (layer caching)
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy application code
COPY . .

# 5. (Command specified in docker-compose.yml)
```

**Junior Dev Lessons:**
- **FROM**: Choose a base image (starting point)
- **WORKDIR**: Set the current directory inside container
- **COPY**: Copy files from your computer into the container
- **RUN**: Execute commands during build
- **Layer caching**: Docker caches each step; only rebuilds changed layers
- **--no-cache-dir**: Reduces image size by not storing pip cache

**Why copy requirements.txt first?**
- Docker builds in layers
- If requirements.txt doesn't change, Docker reuses the cached layer
- Only reinstalls dependencies when requirements.txt changes
- Saves tons of time!

**How to improve:**
```dockerfile
# 1. Multi-stage build (smaller final image)
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# 2. Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# 3. Run as non-root user (security)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# 4. Add labels for metadata
LABEL maintainer="your-email@example.com"
LABEL version="0.1.0"
LABEL description="GovernAble API"

# 5. Install only production dependencies
RUN pip install --no-cache-dir -r requirements.txt --no-dev

# 6. Use specific base image version (reproducibility)
FROM python:3.11.7-slim
```

---

### 12. `docker-compose.yml` - Multi-Container Setup

**Purpose:** Define and run multiple containers together.

**Key Concepts:**
```yaml
version: "3.8"

services:
  api:
    build: .
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./:/app
    ports:
      - "8000:8000"
  
  proxy:
    image: node:20
    working_dir: /srv
    volumes:
      - ./proxy:/srv
    command: sh -c "npm install && node governor.ts"
    ports:
      - "8787:8787"
    depends_on:
      - api
```

**Junior Dev Lessons:**
- **services**: Each container you want to run
- **build**: Build from Dockerfile in current directory
- **image**: Use a pre-built image
- **volumes**: Mount local folders into container (changes sync automatically)
- **ports**: `"HOST:CONTAINER"` - map port on your computer to port in container
- **depends_on**: Start dependencies first
- **command**: Override the default command

**How to improve:**
```yaml
version: "3.8"

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: development  # Use dev stage in multi-stage build
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./:/app
      - api-cache:/app/__pycache__  # Don't sync cache folders
    ports:
      - "8000:8000"
    environment:
      - ENV=development
      - DATABASE_URL=postgresql://user:pass@db:5432/governable
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    networks:
      - governable-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
  
  db:
    image: postgres:15-alpine
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=governable
    ports:
      - "5432:5432"
    networks:
      - governable-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
  
  proxy:
    image: node:20-alpine
    working_dir: /srv
    volumes:
      - ./proxy:/srv
      - node-modules:/srv/node_modules  # Cache node_modules
    command: sh -c "npm install && npm start"
    ports:
      - "8787:8787"
    environment:
      - API_BASE=http://api:8000
      - LLM_TARGET=https://api.openai.com
    env_file:
      - .env
    depends_on:
      - api
    networks:
      - governable-network
    restart: unless-stopped
  
  frontend:
    build:
      context: ./web/frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    volumes:
      - ./web/frontend/src:/app/src
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - api
    networks:
      - governable-network

networks:
  governable-network:
    driver: bridge

volumes:
  postgres-data:
  api-cache:
  node-modules:
```

---

### 13. `requirements.txt` - Python Dependencies

**Purpose:** List all Python packages needed for the project.

**Current dependencies:**
```
fastapi          # Web framework
uvicorn[standard]  # ASGI server
pydantic         # Data validation
pyyaml           # YAML parsing
sqlalchemy[asyncio]  # Database ORM
aiosqlite        # Async SQLite driver
python-multipart # File upload support
httpx            # HTTP client
presidio-analyzer  # PII detection (optional)
pytest           # Testing framework
```

**How to improve:**
```txt
# Production dependencies
fastapi==0.109.0
uvicorn[standard]==0.25.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0

# Database
sqlalchemy[asyncio]==2.0.25
alembic==1.13.1  # Database migrations
aiosqlite==0.19.0  # For dev
asyncpg==0.29.0  # For production (PostgreSQL)

# Scanning
pyyaml==6.0.1
presidio-analyzer==2.2.33
presidio-anonymizer==2.2.33

# HTTP & Files
httpx==0.26.0
python-multipart==0.0.6
aiofiles==23.2.1

# Monitoring & Logging
sentry-sdk==1.39.0
structlog==24.1.0
prometheus-client==0.19.0

# Security
cryptography==41.0.7
python-jose[cryptography]==3.3.0  # JWT
passlib[bcrypt]==1.7.4  # Password hashing

# Rate limiting
slowapi==0.1.9
redis==5.0.1  # For distributed rate limiting

# Caching
aiocache[redis]==0.12.2

# Dev dependencies (separate file: requirements-dev.txt)
# pytest==7.4.3
# pytest-asyncio==0.21.1
# pytest-cov==4.1.0
# black==23.12.0
# ruff==0.1.8
# mypy==1.7.1
# httpx==0.26.0  # For testing
```

**Best practices:**
```bash
# Pin exact versions for reproducibility
pip freeze > requirements.txt

# Separate dev and prod dependencies
# requirements.txt - production only
# requirements-dev.txt - development tools

# Use pip-tools for better dependency management
pip install pip-tools
pip-compile requirements.in  # Generates requirements.txt with locked versions

# Create requirements.in:
# fastapi
# uvicorn[standard]
# Then run: pip-compile requirements.in
```

---

## 🎓 Key Programming Concepts

### 1. **Async/Await (Asynchronous Programming)**

**Problem:** Traditional code blocks while waiting for I/O (database, network)

**Solution:** Async code can do other work while waiting

```python
# Blocking (bad for web servers)
def slow_function():
    result = database.query()  # Waits here, blocks everything
    return result

# Non-blocking (good!)
async def fast_function():
    result = await database.query()  # Waits, but allows other requests to process
    return result
```

**When to use:**
- ✅ Web servers handling many requests
- ✅ Database queries
- ✅ Network requests (API calls)
- ✅ File I/O
- ❌ CPU-intensive calculations (use multiprocessing instead)

---

### 2. **Dependency Injection**

**Pattern:** Pass dependencies to functions instead of creating them inside

```python
# Bad: hard to test, tightly coupled
def scan_text(text: str):
    scanner = Scanner()  # Created inside, hard to mock
    return scanner.scan(text)

# Good: easy to test, flexible
def scan_text(text: str, scanner: Scanner):
    return scanner.scan(text)

# FastAPI style:
def get_scanner():
    return Scanner()

@app.post("/scan")
async def scan_endpoint(text: str, scanner: Scanner = Depends(get_scanner)):
    return scanner.scan(text)
```

**Benefits:**
- Easy to test (inject mock dependencies)
- Flexible (swap implementations)
- Clear dependencies

---

### 3. **Type Hints & Validation**

**Python with Pydantic:**
```python
from pydantic import BaseModel, Field, validator

class User(BaseModel):
    name: str
    age: int = Field(..., gt=0, lt=150)  # Must be between 0 and 150
    email: str
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()

# Usage
user = User(name="Alice", age=30, email="ALICE@EXAMPLE.COM")
# Automatic validation and conversion!
```

**TypeScript:**
```typescript
interface User {
  name: string;
  age: number;
  email: string;
}

function greet(user: User): string {
  return `Hello, ${user.name}`;
}

// TypeScript catches errors at compile time
greet({ name: "Bob", age: 25 });  // Error: missing 'email'
```

---

### 4. **Error Handling**

**Python:**
```python
try:
    result = risky_operation()
except SpecificException as e:
    # Handle specific error
    logger.error(f"Operation failed: {e}")
    return default_value
except Exception as e:
    # Catch-all (use sparingly)
    logger.exception("Unexpected error")
    raise
finally:
    # Always runs (cleanup)
    close_resources()
```

**Best practices:**
- ✅ Be specific (catch specific exceptions)
- ✅ Log errors
- ✅ Re-raise if you can't handle
- ❌ Empty except blocks
- ❌ Catching `Exception` without logging

---

### 5. **RESTful API Design**

**Good patterns:**
```
GET    /api/v1/scans          # List all scans
GET    /api/v1/scans/123      # Get specific scan
POST   /api/v1/scans          # Create new scan
PUT    /api/v1/scans/123      # Update entire scan
PATCH  /api/v1/scans/123      # Partial update
DELETE /api/v1/scans/123      # Delete scan

POST   /api/v1/scans/123/retry  # Action on resource
```

**HTTP Status Codes:**
- 200 OK - Success
- 201 Created - Resource created
- 400 Bad Request - Invalid input
- 401 Unauthorized - Missing/invalid auth
- 403 Forbidden - Authenticated but not allowed
- 404 Not Found - Resource doesn't exist
- 500 Internal Server Error - Server error

---

## 🚀 How to Improve Each Component

### Backend API
1. **Add authentication**: JWT tokens, OAuth2
2. **Add rate limiting**: Prevent abuse
3. **Add request validation**: More Pydantic models
4. **Add pagination**: For list endpoints
5. **Add filtering & sorting**: Query parameters
6. **Add caching**: Redis for frequently accessed data
7. **Add monitoring**: Prometheus metrics, Sentry errors
8. **Add API versioning**: `/api/v2/` for breaking changes

### Scanner Engine
1. **Improve accuracy**: ML-based detection, confidence scores
2. **Add custom rules**: User-defined patterns
3. **Optimize performance**: Parallel scanning, incremental scanning
4. **Add more secret types**: Database credentials, certificates
5. **Reduce false positives**: Context analysis, entropy checking
6. **Add binary file support**: Scan compiled files, images (OCR)

### Proxy
1. **Add request/response logging**: Audit trail
2. **Add caching**: Cache LLM responses
3. **Add load balancing**: Multiple LLM providers
4. **Add circuit breaker**: Handle downstream failures
5. **Add observability**: OpenTelemetry tracing

### Frontend
1. **Add charts**: Visualize trends over time
2. **Add real-time updates**: WebSocket for live data
3. **Add dark mode**: User preference
4. **Add export**: Download scan results as CSV/PDF
5. **Add search**: Full-text search across scans
6. **Add user management**: Roles, permissions

### DevOps
1. **Add CI/CD**: GitHub Actions, automated testing
2. **Add staging environment**: Test before production
3. **Add monitoring**: Grafana dashboards
4. **Add backups**: Automated database backups
5. **Add secrets management**: Vault, AWS Secrets Manager
6. **Add container scanning**: Check for vulnerabilities

---

## 📚 Learning Resources

### Python & FastAPI
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Real Python**: https://realpython.com/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html
- **Pydantic**: https://docs.pydantic.dev/

### TypeScript & React
- **TypeScript Handbook**: https://www.typescriptlang.org/docs/
- **React Docs**: https://react.dev/
- **React TypeScript Cheatsheet**: https://react-typescript-cheatsheet.netlify.app/

### Databases
- **SQLAlchemy Tutorial**: https://docs.sqlalchemy.org/en/20/tutorial/
- **SQL Teaching**: https://www.sqlteaching.com/
- **Database Design**: https://www.dbdesigner.net/

### DevOps
- **Docker Tutorial**: https://www.docker.com/101-tutorial/
- **Docker Compose**: https://docs.docker.com/compose/
- **Kubernetes Basics**: https://kubernetes.io/docs/tutorials/

### Security
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Web Security Academy**: https://portswigger.net/web-security
- **Secrets Management**: https://www.vaultproject.io/

### Regex
- **Regex101**: https://regex101.com/ (interactive testing)
- **RegexOne Tutorial**: https://regexone.com/
- **Common Regex Patterns**: https://rgxdb.com/

### General
- **MDN Web Docs**: https://developer.mozilla.org/
- **Stack Overflow**: https://stackoverflow.com/
- **GitHub**: Read other projects' code!

---

## ⚡ Performance & Optimization Tips

### Memory Efficiency

**Problem: Loading large AI prompts/responses into memory**
```python
# ❌ Bad: Loads entire AI conversation history (could be GB!)
async def scan_conversation(messages: List[dict]):
    full_text = " ".join([msg["content"] for msg in messages])  # All in memory!
    findings = scanner.scan_text(full_text)

# ✅ Good: Scan messages individually
async def scan_conversation(messages: List[dict]):
    findings = []
    offset = 0
    
    for msg in messages:
        text = msg["content"]
        msg_findings = scanner.scan_text(text)
        
        # Adjust positions for combined context
        for f in msg_findings:
            f.start += offset
            f.end += offset
            f.context = f"Message from {msg['role']}: {f.context}"
        
        findings.extend(msg_findings)
        offset += len(text) + 1
    
    return findings
```

### CPU Efficiency

**Use compiled patterns (already done in Scanner!):**
```python
# ✅ Pattern compiled once at startup
self.compiled = [(label, re.compile(pattern)) for label, pattern in patterns]

# Much faster than:
# ❌ Compiling on every scan
re.findall(pattern, text)  # Compiles pattern each time
```

### Database Efficiency

**Batch operations:**
```python
# ❌ N queries
for finding in findings:
    await save_finding(finding)  # Separate database call

# ✅ 1 query
await save_findings_batch(findings)  # Single transaction
```

**Use indexes on frequently queried columns:**
```python
filename: Mapped[str] = mapped_column(String(256), index=True)
scanned_at: Mapped[datetime] = mapped_column(DateTime, index=True)
```

### API Performance

**Add caching for repeated AI governance checks:**
```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def scan_cached(text_hash: str, text: str):
    """Cache governance decisions for identical prompts"""
    return scanner.scan_text(text)

@router.post("/enforce/check")
async def enforce(payload: EnforceRequest):
    # Same prompt = same decision (no need to re-scan)
    text_hash = hashlib.sha256(payload.text.encode()).hexdigest()
    findings = scan_cached(text_hash, payload.text)
    return evaluate_policy(payload.text, payload.policy)
```

**Use background tasks for AI audit logging:**
```python
@router.post("/proxy/llm")
async def ai_proxy(request: Request, background_tasks: BackgroundTasks):
    decision = await enforce_governance(request.prompt)
    
    # Don't block response to log audit trail
    background_tasks.add_task(
        log_ai_interaction,
        user=request.user,
        prompt=request.prompt,
        decision=decision,
        timestamp=datetime.now()
    )
    
    return forward_to_ai(request.prompt)
```

---

## 🎯 Next Steps for Junior Developers

### Level 1: Understanding (Week 1-2)
1. **Read the code**: Understand one file completely (start with `api/config.py`)
2. **Run the application**: Follow the setup guide and get it running
3. **Test manually**: Try scanning some text files
4. **Read error messages**: When something breaks, understand why

### Level 2: Small Changes (Week 3-4)
5. **Add a regex pattern**: Add detection for a new type of secret
6. **Modify an endpoint**: Change a response format
7. **Add validation**: Add input validation to prevent errors
8. **Write your first test**: Test one function

### Level 3: New Features (Month 2)
9. **Add a new endpoint**: Create a new API route
10. **Add database queries**: Read/write from database
11. **Implement a feature**: Small feature from requirements
12. **Write documentation**: Document what you built

### Level 4: Optimization (Month 3+)
13. **Profile performance**: Find and fix slow code
14. **Add caching**: Speed up repeated operations
15. **Improve error handling**: Better error messages
16. **Security improvements**: Add rate limiting, authentication

**Good First Tasks (AI Governance Focus):**
- ✅ Add detection pattern for confidential company terms (e.g., project codenames)
- ✅ Add endpoint to retrieve governance violation history
- ✅ Add validation to reject prompts over size limit (prevent token abuse)
- ✅ Write tests for policy enforcement scenarios (BLOCK, REDACT, ALLOW)
- ✅ Add logging to track which users trigger most violations
- ✅ Improve error messages to explain WHY a prompt was blocked
- ✅ Add "Violations by User" chart to compliance dashboard
- ✅ Implement different policies for different teams/departments
- ✅ Add webhook notifications when critical data is detected in AI prompts

---

## 💡 Common Pitfalls & Solutions

### 1. Not Handling Errors ❌
```python
# Bad - app crashes if function fails
result = risky_function()

# Good - handle errors gracefully
try:
    result = risky_function()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    return default_value
except Exception as e:
    logger.exception("Unexpected error")
    raise HTTPException(500, "Internal server error")
```

### 2. Blocking the Event Loop ❌
```python
# Bad - blocks all other requests
import time
await async_operation()
time.sleep(5)  # Freezes the whole server!

# Good - non-blocking sleep
import asyncio
await async_operation()
await asyncio.sleep(5)  # Other requests can process
```

### 3. SQL Injection Vulnerability ❌
```python
# Bad - SQL injection vulnerable!
query = f"SELECT * FROM users WHERE name = '{user_input}'"
# user_input = "admin' OR '1'='1" returns all users!

# Good - use parameterized queries
query = "SELECT * FROM users WHERE name = :name"
session.execute(query, {"name": user_input})

# Best - use ORM
stmt = select(User).where(User.name == user_input)
```

### 4. Not Validating Input ❌
```python
# Bad - accepts any file size
@app.post("/scan")
async def scan(file: UploadFile):
    contents = await file.read()  # Could be 10GB!

# Good - validate before processing
@app.post("/scan")
async def scan(file: UploadFile = File(...)):
    if file.size > 10_000_000:  # 10MB limit
        raise HTTPException(400, "File too large")
    
    if not file.filename.endswith(('.txt', '.json')):
        raise HTTPException(400, "Invalid file type")
    
    contents = await file.read()
```

### 5. Exposing Sensitive Data ❌
```python
# Bad - leaks password hash
return {"user": user.__dict__}

# Good - only return safe fields
return {"username": user.username, "email": user.email}

# Best - use response model
class UserResponse(BaseModel):
    username: str
    email: str

@app.get("/user", response_model=UserResponse)
async def get_user():
    return user  # Only fields in UserResponse are returned
```

### 6. Not Using Async Properly ❌
```python
# Bad - mixing sync and async incorrectly
async def handler():
    result = regular_function()  # Blocks if it's slow
    return result

# Good - use asyncio.to_thread for sync functions
async def handler():
    result = await asyncio.to_thread(slow_sync_function)
    return result
```

### 7. Forgetting to Close Resources ❌
```python
# Bad - file handle leaks
file = open('data.txt')
data = file.read()
# Forgot to close!

# Good - automatically closes
with open('data.txt') as file:
    data = file.read()

# For async:
async with aiofiles.open('data.txt') as file:
    data = await file.read()
```

---

## 📚 Extended Learning Resources

### Interactive Practice
- **Python Practice**: https://www.hackerrank.com/domains/python
- **SQL Practice**: https://sqlbolt.com/
- **Regex Practice**: https://regexone.com/
- **Git Practice**: https://learngitbranching.js.org/

### Video Tutorials
- **FastAPI Full Course**: https://www.youtube.com/watch?v=7t2alSnE2-I
- **Async Python**: https://www.youtube.com/watch?v=t5Bo1Je9EmE
- **Docker Tutorial**: https://www.youtube.com/watch?v=fqMOX6JJhGo

### Books (Free)
- **Automate the Boring Stuff**: https://automatetheboringstuff.com/
- **Python for Everybody**: https://www.py4e.com/
- **Clean Code (Summary)**: https://gist.github.com/wojteklu/73c6914cc446146b8b533c0988cf8d29

### Reference Documentation
- **FastAPI Docs**: https://fastapi.tiangolo.com/ (⭐ Excellent docs!)
- **Pydantic Docs**: https://docs.pydantic.dev/
- **SQLAlchemy Tutorial**: https://docs.sqlalchemy.org/en/20/tutorial/
- **React Docs**: https://react.dev/
- **TypeScript Handbook**: https://www.typescriptlang.org/docs/

---

## ✅ Daily Development Checklist

**Before Starting Work:**
- [ ] Pull latest changes: `git pull origin main`
- [ ] Activate virtual environment: `.\\venv\\Scripts\\Activate.ps1`
- [ ] Update dependencies if needed: `pip install -r requirements.txt`
- [ ] Check if tests pass: `pytest tests/`

**While Coding:**
- [ ] Write code in small, testable chunks
- [ ] Add comments for complex logic
- [ ] Test as you go (don't wait until the end)
- [ ] Use meaningful variable names
- [ ] Handle errors appropriately

**Before Committing:**
- [ ] Run tests: `pytest tests/`
- [ ] Check code style: `black . && flake8 .`
- [ ] Remove debug print statements
- [ ] Update documentation if needed
- [ ] Review your own changes

**Git Workflow:**
```powershell
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes and commit
git add .
git commit -m "Add feature: description"

# 3. Push to remote
git push origin feature/my-feature

# 4. Create Pull Request on GitHub
```

---

**Happy Coding! 🚀**

Remember: 
- **Every expert was once a beginner** - Don't be discouraged by challenges
- **Mistakes are learning opportunities** - Break things, that's how you learn
- **Ask questions** - No question is too basic
- **Read error messages carefully** - They usually tell you exactly what's wrong
- **Use the debugger** - Step through code to understand it
- **Practice regularly** - Consistency beats intensity

**Questions or stuck on something?**
- Check error messages first (they're trying to help!)
- Search Stack Overflow: https://stackoverflow.com/
- Read the documentation
- Ask your team for help
- Check this guide's troubleshooting section

**Keep practicing, keep building, keep learning! 💪**
