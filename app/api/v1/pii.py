from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from presidio_analyzer import AnalyzerEngine
from pprint import pprint
import json
import re

router = APIRouter()
analyzer = AnalyzerEngine()

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

def calc_score(matched, example):
    matches = sum(1 for a, b in zip(matched, example) if a == b)
    return int((matches / len(example)) * 100) if example else 0

def detect_pattern(text_code):
    # Presidio detection
    presidio_results = analyzer.analyze(text=text_code, entities=[], language='en')
    findings = [
        {
            "entity": r.entity_type,
            "start": r.start,
            "end": r.end,
            "score": r.score,
            "text": text_code[r.start:r.end]
        }
        for r in presidio_results
    ]
    # Regex detection (custom patterns)
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
   
@router.post("/scan")
async def scan_file(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode()
    findings = detect_pattern(text)
    return JSONResponse(content={
        "filename": file.filename,
        "pii_found": bool(findings),
        "findings": findings
    })
