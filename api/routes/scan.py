# Import tools from FastAPI for creating routers, handling file uploads, and more.
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Request
# Import the Scanner we built earlier. This is how the API talks to the engine.
from engine.scanner import Scanner
# Create a new router. This is like setting up a new section in the restaurant.
router = APIRouter()
# Create a single, reusable instance of our Scanner.
# This is efficient because it loads the rules from the YAML file only once when the API starts.
scanner = Scanner()
# This defines the data we expect for a "scan text" request.
# It must be a JSON object with a key named "text".
class ScanTextRequest(BaseModel):
    text: str
    use_presidio: Optional[bool] = True
# This is a simple authentication function. For now, it's not very secure.
# It just checks if a special header 'x-api-key' is present in the request.
# We'll make this better later.
def api_key_auth(request: Request):
    # MVP: simple header check, tighten for prod
    # key = request.headers.get("x-api-key", "")
    # if settings.API_KEY and key != settings.API_KEY: raise HTTPException(401)
    return True # For now, we always allow the request.
# This creates the '/text' endpoint. The '@router.post' means it listens for POST requests
# at the URL '/api/v1/scan/text'.
@router.post("/text")
async def scan_text(payload: ScanTextRequest, ok: bool = Depends(api_key_auth)):
    # It calls our scanner's scan_text method with the text from the request.
    findings = scanner.scan_text(payload.text)
    # It returns the findings as a JSON response.
    return {"count": len(findings), "findings": [f.__dict__ for f in findings]}
# This creates the '/file' endpoint for file uploads.
@router.post("/file")
async def scan_file(file: UploadFile = File(...), use_presidio: bool = Form(True), ok: bool = Depends(api_key_auth)):
    # It reads the content of the uploaded file.
    contents = await file.read()
    # It converts the file content (which is in bytes) into a string.
    text = contents.decode("utf-8", errors="ignore")
    # It calls the scanner.
    findings = scanner.scan_text(text)
    # It returns the results.
    return {"filename": file.filename, "count": len(findings), "findings": [f.__dict__ for f in findings]}
