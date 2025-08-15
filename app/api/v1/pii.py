from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from presidio_analyzer import AnalyzerEngine
import re
import csv
from io import StringIO
from docx import Document

# ======================
# 1. Router setup
# ======================
router = APIRouter()

# Create Presidio Analyzer instance
analyzer = AnalyzerEngine()

# Default Presidio entities to scan (can be extended)
DEFAULT_PRESIDIO_ENTITIES = [
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "IP_ADDRESS",
    "PERSON",
    "CREDIT_CARD",
]

# ======================
# 2. Custom regex patterns
# ======================
custom_patterns = {
    "Credit Card Number": {
        "pattern": r"\b(?:\d[ -]*?){16}\b",
        "example": "1234-5678-9012-3456"
    },
    "NI Number": {
        "pattern": r"\b[A-Z]{2}\d{6}[A-Z]{1}\b",
        "example": "AB123456C"
    },
    "NHS Number": {
        "pattern": r"\b\d{3}-\d{3}-\d{4}\b",
        "example": "123-456-7890"
    },
    "Passport Number": {
        "pattern": r"\b[A-Z]{2}\d{6,9}\b",
        "example": "AB1234567"
    }
}

# ======================
# 3. Helper: Score calculation
# ======================
def calc_score(matched, example):
    """
    Compare the matched text to the example format and return a score (0-1)
    """
    matches = sum(1 for a, b in zip(matched, example) if a == b)
    return float((matches / len(example))  / 100) if example else 0

# ======================
# 4. Helper: File content extraction
# ======================
def extract_text_from_file(file: UploadFile) -> str:
    """
    Reads file and returns plain text for scanning.
    Supports: .txt, .csv, .docx
    """
    content = file.file.read()
    filename = file.filename.lower()

    if filename.endswith(".txt"):
        return content.decode()

    elif filename.endswith(".csv"):
        decoded = content.decode()
        csv_reader = csv.reader(StringIO(decoded))
        return "\n".join([", ".join(row) for row in csv_reader])

    elif filename.endswith(".docx"):
        from io import BytesIO
        document = Document(BytesIO(content))
        return "\n".join([p.text for p in document.paragraphs])

    else:
        raise ValueError("Unsupported file format. Use .txt, .csv, or .docx")

# ======================
# 5. Main detection function
# ======================
def detect_pattern(text_code: str, presidio_entities: list[str] = None):
    """
    Runs both Presidio and custom regex patterns to detect PII.
    """
    if presidio_entities is None:
        presidio_entities = DEFAULT_PRESIDIO_ENTITIES

    findings = []

    # --- Presidio detection ---
    presidio_results = analyzer.analyze(
        text=text_code,
        entities=presidio_entities,
        language='en'
    )
    for r in presidio_results:
        findings.append({
            "entity": r.entity_type,
            "start": r.start,
            "end": r.end,
            "score": r.score,
            "text": text_code[r.start:r.end]
        })

    # --- Custom regex detection ---
    for label, info in custom_patterns.items():
        pattern = info["pattern"]
        example = info["example"]
        for match in re.finditer(pattern, text_code):
            matched_text = match.group()
            score = calc_score(matched_text, example)
            findings.append({
                "entity": label,
                "start": match.start(),
                "end": match.end(),
                "score": score,
                "text": matched_text
            })

    return findings

# ======================
# 6. FastAPI endpoint
# ======================
@router.post("/scan")
async def scan_file(
    file: UploadFile = File(...),
    presidio_entities: str = None  # Optional: comma-separated list
):
    """
    Upload a file and scan for PII.
    Optional query param: presidio_entities=EMAIL_ADDRESS,PHONE_NUMBER
    """
    try:
        # Step 1: Read and extract text
        text = extract_text_from_file(file)

        # Step 2: Convert comma-separated entities to list
        entities_list = None
        if presidio_entities:
            entities_list = [e.strip() for e in presidio_entities.split(",")]

        # Step 3: Detect PII
        findings = detect_pattern(text, entities_list)

        # Step 4: Return results
        return JSONResponse(content={
            "filename": file.filename,
            "pii_found": bool(findings),
            "findings": findings
        })

    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
