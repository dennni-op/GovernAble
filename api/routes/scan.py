from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import re
router = APIRouter()

def detect_pattern(text_code):
	patterns = {
		"Email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
		"Phone": r"\\+?[1-9]\\d{1,14}",
	}
	findings = []
	for label, pattern in patterns.items():
		if re.search(pattern, text_code):
			findings.append(label)
	return findings

@router.post("")
async def scan_file(file: UploadFile = File(...)):
	content = await file.read()
	findings = []
	count_line = 0
	for line in content.decode().splitlines():
		matches = detect_pattern(line)
		count_line += 1
		if matches:
			findings.append({"Line Number": count_line, "Types": matches })
	return JSONResponse(content={
		"filename": file.filename,
		"pii_found": bool(findings),
		"Findings": findings
	})
