# Import Pydantic for creating our data models and the Scanner to find secrets.
from pydantic import BaseModel, Field
from typing import List, Literal
from engine.scanner import Scanner
# This defines the four possible actions our policy can take.
# 'Literal' means the 'Action' type can only be one of these four strings.
Action = Literal["ALLOW", "WARN", "REDACT", "BLOCK"]
# This defines a single rule for a specific type of secret.
class Rule(BaseModel):
    id: str      # The name of the secret, e.g., "AWS_ACCESS_KEY_ID"
    action: Action = "REDACT" # What to do if we find this specific secret.
# This defines the overall policy.
class Policy(BaseModel):
    name: str
    # This is the default action to take if a secret is found that doesn't have a specific rule.
    mode: Action = "WARN"
    # A list of specific rules that can override the default mode.
    rules: List[Rule] = Field(default_factory=list)
# We create another scanner instance here, just for this service.
scanner = Scanner()
# A simple data class to hold the result of our evaluation.
class EvalResult(BaseModel):
    action: Action
    redacted_text: Optional[str] = None
    reasons: List[str] = []
# This is the core logic function! It takes text and a policy and returns a decision.
def evaluate_policy(text: str, policy: Policy) -> EvalResult:
    # First, scan the text to find any secrets.
    findings = scanner.scan_text(text)
    # If no secrets are found, we can just ALLOW it and stop.
    if not findings:
        return EvalResult(action="ALLOW", reasons=[])
    # Prepare to make a decision.
    actions_to_take = []
    redacted_text = text
    reasons_for_decision = []
    # Create a quick lookup map of specific rules from the policy.
    rule_overrides = {r.id: r.action for r in policy.rules}
    # Loop through every secret we found.
    for f in findings:
        # Decide which action to take: the specific rule's action, or the policy's default mode.
        action = rule_overrides.get(f.label, policy.mode)
        actions_to_take.append(action)
        reasons_for_decision.append(f"Found '{f.label}'")
        # If the action is to REDACT, we replace the secret in the text with "[REDACTED]".
        if action == "REDACT":
            redacted_text = redacted_text.replace(f.match, "[REDACTED]")
    # Now, figure out the final, most severe action to take.
    # The order of severity is BLOCK > REDACT > WARN.
    if "BLOCK" in actions_to_take:
        return EvalResult(action="BLOCK", reasons=reasons_for_decision)
    if "REDACT" in actions_to_take:
        return EvalResult(action="REDACT", redacted_text=redacted_text, reasons=reasons_for_decision)
    if "WARN" in actions_to_take:
        return EvalResult(action="WARN", reasons=reasons_for_decision)
    
    # If for some reason no action was chosen, just allow it.
    return EvalResult(action="ALLOW", reasons=reasons_for_decision)
