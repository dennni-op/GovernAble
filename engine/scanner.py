
# GovernAble Core Detection Engine
import re
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Any

# 1. Pattern Loading from YAML
def load_patterns(yaml_path: Optional[str] = None) -> Dict[str, str]:
	"""
	Load regex patterns from a YAML file. Default is engine/rules/base_patterns.yml.
	"""
	if yaml_path is None:
		yaml_path = Path(__file__).parent / "rules" / "base_patterns.yml"
	with open(yaml_path, "r", encoding="utf-8") as f:
		patterns = yaml.safe_load(f) or {}
	return patterns

# 2. Regex-based Detection
def regex_scan(text: str, patterns: Dict[str, str]) -> List[str]:
	"""
	Scan text using regex patterns. Returns a list of detected pattern labels.
	"""
	findings = []
	for label, pattern in patterns.items():
		if re.search(pattern, text):
			findings.append(label)
	return findings

# 3. Presidio-based Detection
try:
	from presidio_analyzer import AnalyzerEngine
	analyzer = AnalyzerEngine()
	def presidio_scan(text: str, language: str = "en") -> List[str]:
		"""
		Scan text using Presidio AnalyzerEngine. Returns a list of detected entity types.
		"""
		results = analyzer.analyze(text=text, language=language)
		return [r.entity_type for r in results]
except ImportError:
	def presidio_scan(text: str, language: str = "en") -> List[str]:
		"""
		Dummy function if Presidio is not installed.
		"""
		return []

# 4. Utility Functions for Scanning
def scan_text(text: str, patterns: Optional[Dict[str, str]] = None, use_presidio: bool = True) -> Dict[str, Any]:
	"""
	Scan a string of text using regex and/or Presidio.
	"""
	results = {}
	if patterns:
		results['regex'] = regex_scan(text, patterns)
	if use_presidio:
		results['presidio'] = presidio_scan(text)
	return results

def scan_file(filepath: str, patterns: Optional[Dict[str, str]] = None, use_presidio: bool = True) -> Dict[str, Any]:
	"""
	Scan a file by path.
	"""
	with open(filepath, "r", encoding="utf-8") as f:
		return scan_text(f.read(), patterns, use_presidio)

def scan_stream(stream, patterns: Optional[Dict[str, str]] = None, use_presidio: bool = True) -> Dict[str, Any]:
	"""
	Scan a file-like stream.
	"""
	return scan_text(stream.read(), patterns, use_presidio)

# 5. Expose a Clean Python API
__all__ = [
	"load_patterns",
	"regex_scan",
	"presidio_scan",
	"scan_text",
	"scan_file",
	"scan_stream"
]
