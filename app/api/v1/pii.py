from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from presidio_analyzer import AnalyzerEngine
from pprint import pprint
import json
import re

router = APIRouter()
analyzer = AnalyzerEngine()

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
	custom_patterns = {
		"Credit Card Number ": r"\b(?:\d[ -]*?){16}\b",
		"NI Number": r"\b[A-Z]{2}\d{6}\b[A-Z]{1}",
		"NHS Number": r"\b\d{3}-\d{3}-\d{4}\b",
		"Passport Number": r"\b[A-Z]{2}\d{6,9}\b"
	}
	scorevalue = None  # Default score value for custom patterns
	for label, pattern in custom_patterns.items():
		for match in re.finditer(pattern, text_code):
			findings.append({
				"entity": label,
				"start": match.start(),
				"end": match.end(),
				"score": scorevalue,
				"text": match.group()
			})
	return findings
   
@router.post("/scan")
async def scan_file(file: UploadFile = File(...)):
	content = await file.read()
	findings = []
	count_line = 0
	for line in content.decode().splitlines():
		matches = detect_pattern(line)
		count_line += 1
		if matches:
			for match in matches:
				match["line_number"] = count_line
				findings.append(match)
	return JSONResponse(content={
		"filename": file.filename,
		"pii_found": bool(findings),
		"findings": findings
	})
