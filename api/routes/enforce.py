from fastapi import APIRouter
from pydantic import BaseModel
# We import the Policy model and the evaluation function we just created.
from api.services.policies import Policy, evaluate_policy, EvalResult
router = APIRouter()
# Define the data we expect for an enforcement request.
# It needs the text to check and the policy to check it against.
class EnforceRequest(BaseModel):
    text: str
    policy: Policy
# This creates the '/check' endpoint, which listens for POST requests
# at the URL '/api/v1/enforce/check'.
# 'response_model=EvalResult' tells FastAPI to expect a response that looks like our EvalResult model.
@router.post("/check", response_model=EvalResult)
async def check(payload: EnforceRequest):
    # This is super simple! It just calls our 'evaluate_policy' function
    # with the data from the request and returns the result.
    result = evaluate_policy(payload.text, payload.policy)
    return result